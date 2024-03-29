# protein_ligand_md
Troubleshooting and guide for setting up a protein ligand system for Amber

For this guide we will use the enzyme pdb 8dq8
Link to the [pdb file](https://www.rcsb.org/structure/8dq8)

Check pdb file of the complex in Maestro or other viewing software. For this example we will use Schrodinger Maestro.
- Import pdb in Maestro. Inspect the structure and note the ligands and protein chains.
- Delete any waters or ions which may be present in the pdb file.
- Prepare Protein structure. Double check to make sure the Ligands match the one in literature.
- Copy Ligands to new entries.
- Check protonation states of each atom with literature. Make sure to protonate each atom correctly with the right number of H.
- Export as .mol2 files
- Run antechamber -at gaff2 if you wanna run with gaff2
   ```antechamber -i input.mol2 -fi mol2 -o output.mol2 -fo mol2 -c bcc -s 2```
  Add `at gaff2` flag if you want to use gaff2 
  If you get `Weird atomic valence (5) for atom (ID: 24, Name: C2).
   `Possible open valence.  
   then open FDA_h.mol2 and manually edit bond orders to be valence 4 for the affected bond. [Changed bond order of 24 - 26 from ar to 1 and 26 - 27 from ar to 1]
  tail sqm.out and check if the calculation is complete.
  Repeat for NCT and any more ligands you have
  [For NCT changed the prepared structure from N+H to N]
  if you get sqm error that means you have unaccounted charge problems
  Antechamber reassigns charges to the mol2 file generated from maestro. In the event that you get a sqm error regarding odd number of electrons, generate your pdb structure from maestro before protein preparation and manually protonate it.
  parmchk2 -i FDA.mol2 -f mol2 -o FDA.frcmod
  tleap script
  generate lib files
  generate prmtop and rst7
  check atom names to see if they match, use maestro as reference
  If atom name is wrong in the lib file change it to match the pdb naming
