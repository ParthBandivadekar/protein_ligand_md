This section is a list of common and uncommon errors one might face while trying to set up a Protein-Ligand MD simulation in Amber23

There are various errors that can occur when you run Antechamber

**1. Resolving Weird Valence State error**

- If you get `Weird atomic valence. Possible open valence.` that means your structure has missing Hydrogens. Recheck the entire structure.
- In the off chance that the structure is correct and you are still getting this error you have an issue with bond order.
- You need to manually edit the bond order of the offending carbon by opening the input mol2 file and finding the corresponding atom numbering.

For the example in [README](README.MD) 

![](https://github.com/ParthBandivadekar/protein_ligand_md/blob/c5a83e67fed205e9c3b600b4d703b7c315feb399/Screenshot%20from%202024-03-18%2016-04-38.png)

The valence state of the carbon between the two Nitrogens is being reported as 5. In this scenario the bond order of one of the Nitrogens was changed from 1.5 to 1 to fix the error. 
[Link](https://chemicbook.com/2021/02/20/mol2-file-format-explained-for-beginners-part-2.html) to learn how to edit mol2 files.

**2. Fatal Atom Error**

- There are multiple possible reasons for a fatal atom error.
- The first kind: If its a custom ligand you made, check the lib and frcmod files to make sure the name of the ligand is consistent
- For e.g. Here is a .lib file describing oxygen
- ![image](https://github.com/ParthBandivadekar/protein_ligand_md/assets/159869420/192278a5-9d7b-4ae7-bfcb-c76b075328c3)
- And here's the error from tleap
- ![image](https://github.com/ParthBandivadekar/protein_ligand_md/assets/159869420/d6e550e0-2451-4a7c-b8b6-9e9a7b74d86a)
- As you can see, tleap cannot find the parameters for the ligand OXY even though they are stated in the O2.lib file.
- This is because the parameters are saved under the name O2 and not OXY in the lib file. Changing these to OXY leads to the error disappearing
- ![image](https://github.com/ParthBandivadekar/protein_ligand_md/assets/159869420/01aba3f7-1869-4e3b-a80c-7fb41062c52b)
- ![image](https://github.com/ParthBandivadekar/protein_ligand_md/assets/159869420/fedf3653-572e-4fbd-9fa3-2cb92d7e5cc7)
- Now here is the second kind of Fatal Atom error, one for a particular standard residue. The most common residue which shows this error is Histidine.
- This error occurs because Histidine can be found in one of 3 protonation states
- ![image](https://github.com/ParthBandivadekar/protein_ligand_md/assets/159869420/30665205-89a5-4623-969a-4d818d4a26f0)
- By default the pdb file will have all of them listed as HIS. In Amber, HIS defaults to HIE state.
- However if the Histidine is in another state then there is a mismatch of atom numbers due to the extra hydrogens on the epsilon and delta nitrogens.
- The best way to resolve this issue is to manually change the residue name in the pdb file to either HID or HIP for the residues which show the error.
- You can find the protonation state by checking the residue in a visualisation software like Maestro.
- Another easy way is to check if any Nitrogens have a positive charge, if they do then the residue should be HIP since it has a +1 charge.
- Let us go through one example of this
- Checking the protonation state of HIE 115 since that is the first Residue error in the above screenshot
- ![image](https://github.com/ParthBandivadekar/protein_ligand_md/assets/159869420/aad8405d-70f8-4359-8580-e366de9937cd)
- As we can see Atom 963 corresponds to a nitrogen with a positive atom type (last column N1+)
- This means this residue should be HIP not HIE.
- If we rerun the tleap script we can see that HIE 115 is no longer showing an error.
- ![image](https://github.com/ParthBandivadekar/protein_ligand_md/assets/159869420/39392c93-7c7f-4571-8d64-9c06b238dd58)
- Thus we have to go through the rest of the Histidines and fix their residue names.
- This problem can happen for other residues as well.
- Here is a table of residues that can have different protonation states

|         Non-standard Protonation Form      | AMBER Resname |
| ------------------------------------------ | ------------- |      
| Protonated/uncharged Asp                   | ASH           |
| Protonated/uncharged Glu                   | GLH           |
| Deprotonated/uncharged Lys                 | LYN           |
| His protonated at epsilon position         | HIE           |
| His protonated at delta position           | HID           |
| Charged His (protonated at both positions) | HIP           |
| Deprotonated Cys or Cys bound to a metal   | CYM           |
| Cys involved in disulfide bridge           | CYX           |








