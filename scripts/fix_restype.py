#!/usr/bin/env python3
"""
fix_restype.py

Usage:
    python fix_restype.py <input_pdb> <output_pdb>

Automatically inspects each residue in the PDB and corrects its three-letter code
based on sidechain hydrogen presence. Also updates ANISOU records for consistency.

Detection rules:
- Histidine (HIS/HID/HIE/HIP):
    * HD1+HE2 → HIP
    * HD1 only → HID
    * HE2 only → HIE
    * neither → HIS
- Glutamate (GLU/GLH):
    * presence of HE2 → GLH
    * otherwise → GLU
- Aspartate (ASP/ASH):
    * presence of HD1 or HD2 → ASH
    * otherwise → ASP
- Lysine (LYS/LYN):
    * presence of any HZ1/HZ2/HZ3 → LYS
    * otherwise → LYN

Outputs a new PDB with updated residue names in ATOM, HETATM, and ANISOU lines,
and prints a summary of changes.
"""
import sys
from collections import defaultdict

def detect_his_type(atom_lines):
    has_hd1 = any(L[12:16].strip()=='HD1' for L in atom_lines)
    has_he2 = any(L[12:16].strip()=='HE2' for L in atom_lines)
    if has_hd1 and has_he2:
        return 'HIP'
    if has_hd1:
        return 'HID'
    if has_he2:
        return 'HIE'
    return 'HIS'


def auto_fix_restype(input_pdb, output_pdb):
    # Group all ATOM/HETATM lines by residue key
    residues = defaultdict(list)
    others = []
    with open(input_pdb) as f:
        for L in f:
            if L.startswith(('ATOM  ','HETATM')):
                chain = L[21]
                try:
                    resnum = int(L[22:26])
                except ValueError:
                    resnum = L[22:26]
                key = (chain, resnum)
                residues[key].append(L)
            else:
                others.append(L)

    # Determine new names
    changes = {}
    for key, atom_lines in residues.items():
        # original residue name from first atom line
        orig = atom_lines[0][17:20]
        resname = orig.strip()
        new = resname  # default
        if resname in ('HIS','HID','HIE','HIP'):
            new = detect_his_type(atom_lines)
        elif resname == 'GLU':
            # look for HE2
            if any(L[12:16].strip()=='HE2' for L in atom_lines):
                new = 'GLH'
        elif resname == 'ASP':
            if any(L[12:16].strip() in ('HD1','HD2') for L in atom_lines):
                new = 'ASH'
        elif resname == 'LYS':
            if any(L[12:16].strip() in ('HZ1','HZ2','HZ3') for L in atom_lines):
                new = 'LYS'
            else:
                new = 'LYN'
        # record change if different
        if new != resname:
            changes[key] = new

    # Rewrite file
    with open(input_pdb) as inp, open(output_pdb,'w') as out:
        for L in inp:
            if L.startswith(('ATOM  ','HETATM','ANISOU')):
                chain = L[21]
                try:
                    resnum = int(L[22:26])
                except ValueError:
                    resnum = L[22:26]
                key = (chain, resnum)
                if key in changes:
                    new = changes[key].ljust(3)
                    L = L[:17] + new + L[20:]
            out.write(L)

    # Summary
    if changes:
        print('Residues updated:')
        for (chain, resnum), new in sorted(changes.items()):
            print(f"  Chain {chain.strip() or ' '}, Residue {resnum}: {new}")
    else:
        print('No residues needed updating.')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    auto_fix_restype(sys.argv[1], sys.argv[2])
