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

**2. 
