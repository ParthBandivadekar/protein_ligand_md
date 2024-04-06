# protein_ligand_md
Guide for setting up a protein ligand system for Amber23
The basic steps in this guide are identical to the tutorial found [here](https://ambermd.org/tutorials/basic/tutorial4b/index.php)

However this guide is context for the troubleshooting tips posted below the guide.
For this example we will use the enzyme pdb [8dq8](https://www.rcsb.org/structure/8dq8)

Check pdb file of the complex in Maestro or any other viewing software. For this example we will use Schrodinger Maestro.
- Import pdb in Maestro. Inspect the structure and note the ligands and protein chains.
- Delete any waters or ions which may be present in the pdb file.
- Prepare Protein structure. Double check to make sure the Ligands match the one in literature.
- Copy Ligands to new entries in Maestro.
- Cross check protonation states of each atom with literature. Make sure to protonate/deprotonate each atom correctly with the right number of H.
- Export the ligands as .mol2 files
- Run antechamber
 ```antechamber -i Ligand_h.mol2 -fi mol2 -o Ligand.mol2 -fo mol2 -c bcc -s 2```
Add `at gaff2` flag if you want to use gaff2 
- If Antechamber runs without errors, tail the sqm.out which will be generated and check if the calculation is complete.
- Repeat these steps for NCT and any more ligands you have.
- The generated mol2 files will contain information about the parametrization of the ligands
- To check if there are any missing parameters run the following command
```parmchk2 -i Ligand.mol2 -f mol2 -o Ligand.frcmod```
- Inspect the frcmod file and make sure all the missing parameters are covered.
- Use the [tleap.in](tleap.in) script to generate lib files for each ligand.
```tleap -f tleap.in```
- Use the [tleap2.in](tleap2.in) script to generate prmtop and rst7 files for the MD simulation.
```tleap -f tleap2.in```

You will find the input files for the MD simulation on [Dr. Ahn's Github](https://github.com/shirleyahn/amber_scripts/tree/main)
The [troubleshooting guide](Troubleshooting) will help you with any errors you encounter during this process and will be a repository for any future Amber errors which I resolve.
