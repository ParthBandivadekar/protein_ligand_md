This guide is for setting up a protein ligand system with solvents other than Na+, Cl- and Water which are solvated using tleap.
For this purpose we will use [packmol](https://m3g.github.io/packmol/) which is a software package used to create custom simulation boxes for MD simulations.
Packmol can also be used to solvate the protein similar to tleap, however we want to keep most of the native functions of tleap.
To understand how to use packmol properly, I recommend going through the [user guide](https://m3g.github.io/packmol/userguide.shtml) on the packmol website.
This guide will focus on how to combine a packmol simulation box with tleap and Amber simulations.
In this guide we will learn to create a simulation box of 100 Oxygen molecules randomly distributed around a protein.
