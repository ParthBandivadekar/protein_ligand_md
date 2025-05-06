#!/usr/bin/env python3
"""
fix_protonation.py

Usage:
    python fix_protonation.py <input_pdb> <leap_log> <output_pdb>

Automatically renames problem residues (HIS, GLU, ASP, LYS, CYS) based
on Amber's leap.log FATAL errors and disulfide bonds read from CONECT.
Includes sanity check: only SG–SG bonds within CYS residues become CYX.
"""
import re, sys, argparse
from collections import defaultdict

def parse_pdb_atoms(pdb_path):
    atom_info, seen, order = {}, set(), []
    with open(pdb_path) as f:
        for L in f:
            if L.startswith(("ATOM  ","HETATM")):
                serial = int(L[6:11])
                atom_name = L[12:16].strip()
                resname   = L[17:20].strip()
                chain     = L[21].strip()
                resnum    = int(L[22:26])
                atom_info[serial] = (chain, resnum, atom_name, resname)
                key = (chain, resnum)
                if key not in seen:
                    seen.add(key)
                    order.append(key)
    return atom_info, order


def parse_conect_disulfides(pdb_path, atom_info):
    """
    Scan CONECT records by fixed-width fields. Whenever both src and tgt
    atoms are 'SG' _and_ both residues are named 'CYS', mark those residues 'CYX'.
    """
    disulfides = set()
    with open(pdb_path) as f:
        for L in f:
            if not L.startswith("CONECT"):
                continue
            # fixed-width cols: 7–11 source, 12–16,17–21,22–26,27–31 targets
            try:
                src = int(L[6:11].strip())
            except ValueError:
                continue
            for (a,b) in ((11,16),(16,21),(21,26),(26,31)):
                fld = L[a:b].strip()
                if not fld:
                    continue
                try:
                    tgt = int(fld)
                except ValueError:
                    continue
                ainfo = atom_info.get(src)
                binfo = atom_info.get(tgt)
                # Sanity check: both atoms SG and both residues CYS
                if (ainfo and binfo
                    and ainfo[2] == "SG" and binfo[2] == "SG"
                    and ainfo[3] == "CYS" and binfo[3] == "CYS"):
                    disulfides.add((ainfo[0], ainfo[1]))
                    disulfides.add((binfo[0], binfo[1]))
    return disulfides


def parse_leap_errors(log_path):
    amber_map = {}
    pat = re.compile(r"FATAL:\s+Atom\s+\.R<(\w+)\s+(\d+)>" )
    with open(log_path) as f:
        for L in f:
            m = pat.search(L)
            if m:
                orig, idx = m.group(1), int(m.group(2))
                amber_map[idx] = orig
    return amber_map


def build_pdb_mapping(res_order, amber_map):
    pdb_map = {}
    for idx, orig in amber_map.items():
        i = idx - 1
        if 0 <= i < len(res_order):
            pdb_map[res_order[i]] = orig
        else:
            print(f"⚠️ Amber index {idx} out of range (1–{len(res_order)})")
    return pdb_map


def determine_histidine_type(lines):
    has_hd1 = any(L[12:16].strip() == "HD1" for L in lines)
    has_he2 = any(L[12:16].strip() == "HE2" for L in lines)
    if has_hd1 and has_he2:
        return "HIP"
    if has_hd1:
        return "HID"
    if has_he2:
        return "HIE"
    return "HIS"


def rewrite_pdb(in_pdb, out_pdb, pdb_map, disulfides):
    # bucket ATOM/HETATM lines by residue
    residues = defaultdict(list)
    with open(in_pdb) as f:
        for L in f:
            if L.startswith(("ATOM  ","HETATM")):
                chain = L[21].strip()
                try:
                    resnum = int(L[22:26])
                except ValueError:
                    continue
                residues[(chain, resnum)].append(L)

    final_map = {}
    # 1) rename from leap.log
    for key, orig in pdb_map.items():
        if orig in ("HIS","HIE","HID","HIP"):
            new = determine_histidine_type(residues.get(key, []))
        elif orig == "GLU":
            new = "GLH"
        elif orig == "ASP":
            new = "ASH"
        elif orig == "LYS":
            new = "LYN"
        else:
            new = orig
        final_map[key] = new
    # 2) override disulfide CYS
    for key in disulfides:
        final_map[key] = "CYX"

    # write out
    with open(in_pdb) as inp, open(out_pdb, "w") as out:
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
                    new = final_map[key].ljust(3)[:3]
                    L = L[:17] + new + L[20:]
            out.write(L)

    print("📋 Renamed residues:")
    for (chain, res), new in sorted(final_map.items(), key=lambda x: (x[0][0], x[0][1])):
        print(f"  Chain {chain or '<>'}, Residue {res:3d} → {new}")


def main():
    p = argparse.ArgumentParser(
        description="Auto‑fix PDB protonation + disulfides with sanity checks"
    )
    p.add_argument("input_pdb")
    p.add_argument("leap_log")
    p.add_argument("output_pdb")
    args = p.parse_args()

    atom_info, res_order = parse_pdb_atoms(args.input_pdb)
    amber_map = parse_leap_errors(args.leap_log)
    pdb_map   = build_pdb_mapping(res_order, amber_map)
    disulfides = parse_conect_disulfides(args.input_pdb, atom_info)

    if not amber_map and not disulfides:
        print("⚠️ No leap errors or CYS disulfides found—nothing to do.")
        sys.exit(1)

    rewrite_pdb(args.input_pdb, args.output_pdb, pdb_map, disulfides)
    print(f"✅ Wrote fixed PDB to {args.output_pdb}")

if __name__ == "__main__":
    main()

