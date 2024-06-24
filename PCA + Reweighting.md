This guide will detail how to do Principal Component Analysis of your GaMD simulation, Reweighting the Free Energy surface and plotting the principal components to get a free energy diagram
Prerequisites: 
- Basic understanding of running a [GaMD simulation](https://www.med.unc.edu/pharm/miaolab/resources/gamd/)
- prmtop, nc and gamd1.log file from your GaMD simulation
- PyReweighting-2D file from the [Miaolab github](https://github.com/MiaoLab20/pyreweighting)
- Scripts located in this github repo.

Use the [pca.cpptraj](pca.cpptraj) script to get the principal components file pca.dat. Now we need to extract only column 2 and 3 corresponding to the two slowest modes 1 and 2 

```awk '{print $2, $3}' pca.dat > pca12.dat```

Now open pca12.dat and use the command ```:set number``` and press ```Shift + GG```. This will show the number of rows in your file and take you to the bottom of the file respectively.

![image](https://github.com/ParthBandivadekar/protein_ligand_md/assets/159869420/034ef25d-f5d0-47a8-95f0-86b672d6e182)

As you can see the file example here has 1004001 lines.

Before we proceed, lets check the gamd1.log file. Discounting the header rows it should have 1000000 rows checking with :set number.
While we are here we want to extract column 7 and 8 using this command from the GaMD website.

```awk 'NR%1==0' gamd1.log | awk '{print ($8+$7)/(0.001987*300)" "$2" "($8+$7)}' > weights.dat```

This will give us a weights file with 1000000 lines.

Going back to pca12.dat, we want to make sure that this file has the exact number of rows as the weights.dat file. These values might be different depending on how many frames your GaMD simulation has.
For my purpose that means deleting the first 4001 lines.

```tail -n +4001 pca12.dat > pca_final.dat```

Now that these two files have the same amount of rows we can use the PyReweighting file from the Miao Lab website. For this guide we are using the Maclaurin series expansion to reweight. At the current moment cumulant expansion 2nd order reweighting is giving errors for certain tested systems. <br>
We have our weights and pca_final files we can use python to reweight them. In this the most important values are discX and discY which decide the size of your bins. If you find your Free Energy plots are looking too granular you might want to increase your bin sizes to 1 instead of 0.1

```python PyReweighting-2D.py -input pca_final.dat -T 300 -Emax 100 -discX 0.1 -discY 0.1 -job amdweight_MC -order 10 -weight weights.dat | tee -a reweight_variable.log```

This will generate a file called `pmf-pca_final.dat.xvg` which will contain your principal components in column 1 and 2 and your reweighted Free Energies in column 3.
Plotting these using python will get an end result like this.

![free_energy_surface_contour](https://github.com/ParthBandivadekar/protein_ligand_md/assets/159869420/93eb0dd9-507e-49da-b9ac-fe75a59ed373)
