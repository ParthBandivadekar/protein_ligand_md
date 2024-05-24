<b> Guide for making good figures using PyMOL3. </b> <br>
This guide assumes that you have installed PyMOL3. If not, follow the instructions on the [PyMOL](https://pymol.org/) website. <br>

Open PyMOL and import your structure. For this tutorial I am using PDB 1GNS. After importing it should look like this. <br>

![image](https://github.com/ParthBandivadekar/protein_ligand_md/assets/159869420/bc4b5f03-c21f-42e3-a76a-32fbe39a8e3c)

There are two ways to interact with your structure. Using the command line or using the drop down menus. I would recommend getting comfortable with both as there are cases where you would use either method. <br>

The two most important menus are Display and Setting as these will control most of the visual options in PyMOL. <br>

Looking at Display first. <br>

1. The first step is to go to Display->Background->White and Display->Background->Opaque. Sometimes you might want a transparent background in which case turn off Opaque. <br>
2. Second we want PyMOL to use all available resources, Display->Quality->Maxmimum Quality. <br>
3. With these set, we want to decide the color space to use. Display->Color Space->CMYK is my preferred color space as it has more muted tones. However the other options are more vivid and can be appreciated for presentations instead. <br>
4. By Default Display->Orthoscopic View is turned off. This option toggles perspective on or off. In my opinion having this on makes a more neutral and balanced scene. However keeping orthoscopic view off and setting the field of view can produce interesting artistic results. To do this you can use `set field_of_view, 70`

| Orthoscopic on | Orthoscopic off, FOV 70 |
| -------------- | ----------------------- |
|![image](https://github.com/ParthBandivadekar/protein_ligand_md/assets/159869420/cf0d4fe7-3631-4caf-b9d0-f82915481c35) | ![image](https://github.com/ParthBandivadekar/protein_ligand_md/assets/159869420/8bedabde-472a-42db-93ff-9e8be17261b6) |

Setting the perspective lets you see the alpha helices more clearly compared to orthoscopic on but it also distorts how the structure looks

5. 




