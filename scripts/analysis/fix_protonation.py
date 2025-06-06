#!/usr/bin/env python3
"""
Author: Parth Bandivadekar
Lab: Ahn Lab, UC Davis
Date: 2025-06-05

Purpose:
    Fixes protonation states of residues in a PDB file based on Amber LEaP errors.
    (Originally: “Auto-fix PDB protonation states from Amber leap.log.”)

Usage:
    python fix_protonation.py <input_pdb> <leap_log> <output_pdb>

Dependencies:
    argparse, collections, re, sys

Notes:
    • Before running this, you need a “leap.log” file showing Amber’s FATAL errors.
    • The script will parse those errors, detect which residues must be renamed
      (e.g. ASP → ASH, GLU → GLH, HID/HIE/HIP for histidine, etc.), and then
      rewrite the PDB accordingly.

"""
import re
import sys
import argparse
from collections import defaultdict

def parse_pdb_residue_order(pdb_path):
    seen = set()
    order = []
    with open(pdb_path) as f:
        for L in f:
            if L.startswith(("ATOM  ","HETATM")):
                chain = L[21].strip()
                try:
                    resnum = int(L[22:26])
                except ValueError:
                    continue
                key = (chain, resnum)
                if key not in seen:
                    seen.add(key)
                    order.append(key)
    return order

def parse_leap_errors(log_path):
    """
    Returns amber_map: { amber_index (int) : original_resname (str) }
    for every FATAL error in the LEaP log.
    """
    amber_map = {}
    pat = re.compile(r"FATAL:\s+Atom\s+\.R<(\w+)\s+(\d+)>")
    with open(log_path) as f:
        for L in f:
            m = pat.search(L)
            if not m:
                continue
            orig, idx = m.group(1), int(m.group(2))
            amber_map[idx] = orig
    return amber_map

def build_pdb_mapping(residue_order, amber_map):
    """
    Maps Amber’s continuous index → (chain,resnum),
    then builds pdb_map: (chain,resnum) → original_resname.
    """
    pdb_map = {}
    for idx, orig in amber_map.items():
        i = idx - 1
        if i < 0 or i >= len(residue_order):
            print(f"⚠️  Amber index {idx} out of range (1–{len(residue_order)})")
            continue
        chain, resnum = residue_order[i]
        pdb_map[(chain, resnum)] = orig
    return pdb_map

def determine_histidine_type(atom_lines):
    """
    Look for 'HD1' or 'HE2' in columns 12–16 of each ATOM/HETATM line.
    """
    has_hd1 = any(L[12:16].strip() == "HD1" for L in atom_lines)
    has_he2 = any(L[12:16].strip() == "HE2" for L in atom_lines)
    if has_hd1 and has_he2:
        return "HIP"
    if has_hd1:
        return "HID"
    if has_he2:
        return "HIE"
    return "HIS"

def rewrite_pdb(in_pdb, out_pdb, pdb_map):
    """
    Reads the entire PDB into memory, groups lines by (chain,resnum),
    then writes them out, renaming only those in pdb_map.
    """
    # 1) Load all lines, bucket by residue
    residues = defaultdict(list)
    other_lines = []
    with open(in_pdb) as f:
        for L in f:
            if L.startswith(("ATOM  ","HETATM")):
                chain = L[21].strip()
                try:
                    resnum = int(L[22:26])
                except ValueError:
                    # treat as other
                    other_lines.append(L)
                    continue
                residues[(chain, resnum)].append(L)
            else:
                other_lines.append(L)

    # 2) Prepare the final mapping to what new name to use
    final_map = {}
    for key, orig in pdb_map.items():
        chain, resnum = key
        if orig in ("HIS","HID","HIE","HIP"):
            atomLs = residues.get(key, [])
            new = determine_histidine_type(atomLs)
        elif orig == "GLU":
            new = "GLH"
        elif orig == "ASP":
            new = "ASH"
        elif orig == "LYS":
            new = "LYN"
        elif orig == "CYS":
            new = "CYM"  # or CYX if you detect disulfides
        else:
            new = orig
        final_map[key] = new

    # 3) Write out in original order
    with open(out_pdb, "w") as out:
        with open(in_pdb) as inp:
            for L in inp:
                if L.startswith(("ATOM  ","HETATM")):
                    chain = L[21].strip()
                    try:
                        resnum = int(L[22:26])
                    except ValueError:
                        out.write(L)
                        continue
                    key = (chain, resnum)
                    if key in final_map:
                        newres = final_map[key].ljust(3)[:3]
                        # replace cols 17–20
                        L = L[:17] + newres + L[20:]
                out.write(L)

    # 4) Report
    print("📋 Renamed residues:")
    for (chain, res), new in sorted(final_map.items(), key=lambda x: (x[0][0], x[0][1])):
        print(f"  Chain {chain or '<>'}, Residue {res:4d} → {new}")

def main():
    parser = argparse.ArgumentParser(
        description="Auto-fix PDB protonation states from Amber LEaP log"
    )
    parser.add_argument("input_pdb",  help="Original PDB file")
    parser.add_argument("leap_log",   help="Amber leap.log with FATAL errors")
    parser.add_argument("output_pdb", help="Corrected PDB output path")
    args = parser.parse_args()

    # 1) Amber’s internal numbering:
    residue_order = parse_pdb_residue_order(args.input_pdb)
    if not residue_order:
        print("‼️  No ATOM/HETATM records found in PDB.")
        sys.exit(1)

    # 2) FATAL errors → amber_map:
    amber_map = parse_leap_errors(args.leap_log)
    if not amber_map:
        print("⚠️  No FATAL errors found in", args.leap_log)
        sys.exit(1)

    # 3) amber_map → (chain,resnum) → orig_resname
    pdb_map = build_pdb_mapping(residue_order, amber_map)
    if not pdb_map:
        print("⚠️  Mapping back to PDB failed.")
        sys.exit(1)

    # 4) Rewrite:
    rewrite_pdb(args.input_pdb, args.output_pdb, pdb_map)
    print("✅  Done. Your fixed PDB is:", args.output_pdb)

if __name__ == "__main__":
    main()

