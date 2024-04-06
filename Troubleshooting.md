This section is a list of common and uncommon errors one might face while trying to set up a Protein-Ligand MD simulation in Amber23

There are various errors that can occur when you run Antechamber

**1. Resolving `Weird Valence State` error**

If you get `Weird atomic valence. Possible open valence.` that means your structure has missing Hydrogens. Recheck the entire structure.
In the off chance that the structure is correct and you are still getting this error you have an issue with bond order.
For the example in [README](README.MD) 
![The valence state of the carbon between the two Nitrogens is being reported as 5](Screenshot from 2024-03-18 16-04-38.png) 