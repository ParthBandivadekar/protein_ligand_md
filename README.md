# protein_ligand_md
Troubleshooting and guide for setting up a protein ligand system for Amber

For this guide we will use the enzyme pdb 8dq8
Link to the [pdb file](https://www.rcsb.org/structure/8dq8)

Check pdb file of the complex in Maestro or other viewing software. For this example we will use Schrodinger Maestro.
Import 8dq8.pdb in Maestro


Prepare Protein structure
Copy Ligands NCT and FDA to new entries
Check protonation states of each atom with literature
Export as .mol2 files FDA_h.mol2 NCT_h.mol2
6. Run antechamber [-at gaff2 if you wanna run with gaff2]
7. antechamber -i FDA_h.mol2 -fi mol2 -o FDA.mol2 -fo mol2 -c bcc -s 2 -at gaff2
8. If you get `Weird atomic valence (5) for atom (ID: 24, Name: C2).
   `Possible open valence.  
   then open FDA_h.mol2 and manually edit bond orders to be valence 4 for the affected bond. [Changed bond order of 24 - 26 from ar to 1 and 26 - 27 from ar to 1]
9. tail sqm.out and check if the calculation is complete.
10. Repeat for NCT and any more ligands you have
11. [For NCT changed the prepared structure from N+H to N]
12. if you get sqm error that means you have unaccounted charge problems
13. Antechamber reassigns charges to the mol2 file generated from maestro. In the event that you get a sqm error regarding odd number of electrons, generate your pdb structure from maestro before protein preparation and manually protonate it.
14. parmchk2 -i FDA.mol2 -f mol2 -o FDA.frcmod
15. tleap script
16. generate lib files
17. generate prmtop and rst7
18. check atom names to see if they match, use maestro as reference
19. If atom name is wrong in the lib file change it to match the pdb naming
