<b> Guide for making good figures using PyMOL3. </b> <br>
This guide assumes that you have installed PyMOL3. If not, follow the instructions on the [PyMOL](https://pymol.org/) website. <br>

Open PyMOL and import your structure. For this tutorial I am using PDB 1GNS. After importing it should look like this. <br>

![image](https://github.com/ParthBandivadekar/protein_ligand_md/assets/159869420/bc4b5f03-c21f-42e3-a76a-32fbe39a8e3c)

You can move the rotate the structure around using the left mouse button, move it using the middle mouse button and zoom in and out by holding the right mouse button and moving the mouse up or down. <br>
You can change how the mouse functions by customising your selection mode in the Mouse drop down menu.
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

5. I personally prefer to turn off Display->Depth Cue Fog as it makes the structure look less clear. However there are certain scenarios you could use it to hide parts of the structure or show which areas are farther away from the camera. <br>

Looking at Setting next. <br>

1. Go to Setting->Rendering and make Antialias(Real Time) is set to SMAA. This option likes to turn itself off occasionally so you should be occasionally checking this to make sure it is on. <br>
2. The rest of the options go hand in hand with how you want your structure to look. Before changing the other options we can look at making the structure more interesting visually. On the right hand side you will see the pdb 1gns with four labels, A (Action) S (Show) H (Hide) L (Label) C (Color).
3. You want to Hide->Waters which will hide all the red water dots around the structure. Then go to Color->by SS-> Pick a color set of your choice.
4. The default options are not always the best color combination. You can manually set the color of each secondary structure using the command line.
5. `color green, ss h` will set the alpha helices to be green. `s` for beta sheets and `l+''` for loops and turns. You can pick any color available in the color drop down menu.

![image](https://github.com/ParthBandivadekar/protein_ligand_md/assets/159869420/8845148c-b714-430a-9eca-9da149edd9a0)

6. The structure should look like this. However if you see the ends of the loops there is some spillover of colors. To prevent this go to Setting->Cartoon->Discrete Colors.
7. Since we are dealing with a Cartoon structure of an enzyme the options in Setting->Cartoon will affect the structure. If there were ligands present then other types of settings will need to be touched.
8. Another useful option is Transparency. You make can the cartoon structure transparent while focusing on a ligand to make it pop out more.

Now that we have our structure, we need to choose an interesting camera angle and render the image. <br>
To get a rendered ray trace image you can use the command line input `ray x, y` where x is the horizontal ratio and y is the vertical ratio. A good choice is to use `ray 2400,2400` for a square image and then decide if that fits your structure. 

There are different modes for raytracing.
`set ray_trace_mode, X` where X is 0,1,2 or 3. 0 is the default, 1 puts a black outline around the molecule, 2 gives you a black and white 'sketch' and 3 gives you a funky cartoon like image. Pick the mode which looks the best to you.

Once you set the ray trace mode and render an image with ray you want to save this rendered image.
`png /path/to/your/file, dpi=1000` will save this image to the path you select. The dpi option will decide how sharp the image is upon zooming. 1000 works well for most use cases.

The final result might look something like this.

Ray Trace mode 1
![1gns_git](https://github.com/ParthBandivadekar/protein_ligand_md/assets/159869420/a864b450-3dfd-4fa1-8260-15078a0764f8)

Ray Trace mode 3
![1gns_git3](https://github.com/ParthBandivadekar/protein_ligand_md/assets/159869420/18fa93c6-bfad-4677-bcc1-e5c78daf1d11)





