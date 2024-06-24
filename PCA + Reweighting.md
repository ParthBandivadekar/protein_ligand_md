This guide will detail how to do Principal Component Analysis of your GaMD simulation, Reweighting the Free Energy surface and plotting the principal components to get a free energy diagram
Prerequisites: 
- prmtop, nc and gamd1.log file from the GaMD simulation

Use the pca.cpptraj script to get the principal components file pca.dat
Now we need to extract only column 2 and 3 corresponding to the two slowest modes 1 and 2 

```awk '{print $2, $3}' pca.dat > pca12.dat```

Now open pca12.dat and use the command ```:set number``` and press ```Shift + GG```
This will show the number of rows in your file and take you to the bottom of the file respectively.

![image](https://github.com/ParthBandivadekar/protein_ligand_md/assets/159869420/034ef25d-f5d0-47a8-95f0-86b672d6e182)

As you can see the file example here has 1004001 lines.

Before we proceed, lets check the gamd1.log file.
Discounting the header rows it should have 1000000 rows checking with :
```awk 'NR%1==0' gamd1.log | awk '{print ($8+$7)/(0.001987*300)" "$2" "($8+$7)}' > weights.dat```
