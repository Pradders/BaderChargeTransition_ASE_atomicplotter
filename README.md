# BaderCharge_plotter
Leverages ASE, numpy and pyplot to calculate the differences in Bader charges between two structures acquired from VASP and then colour the different atoms according to the difference in charge (i.e., whether positive or negative).

Version 2 (v2) current release.

## Folder structure

reactionORtransition/

-> ini/

->-> CONTCARorPOSCAR

->-> ACF.dat

-> fin/

->-> CONTCARorPOSCAR

->-> ACF.dat

I.e., CONTCAR/POSCAR and ACF.dat are mandatory for the code to work

## Usage

python main.py

## Options for output adjustment, can be configured in main and/or function files

layout = "horizontal" | "vertical" | "split" #I.e., How the images should be displayed in the final figure

repeat = (1,1,1) #i.e., periodic cell expansion

views = [('0x,0y,0z')] #i.e., top view

INITIAL = ("ini","initial","is") #Default is to store key files of each transition in folders entitled "ini" (initial state) and "fin" (final state), or anything similar. These variables will store such possible names. If there are alternate names, then please include them manually

FINAL = ("fin","final","fs") #Default is to store key files of each transition in folders entitled "ini" (initial state) and "fin" (final state), or anything similar. These variables will store such possible names. If there are alternate names, then please include them manually
    
tol = 0.005 #Default tolerance, i.e., if the (abs) difference in Bader charge is less than 0.005, it will treated as 0
  
cmp = plt.cm.RdBu_r #Default colormap also in function, can be changed to any desired, plt already imported

save_dir="Bader_plots" #Save folder

element_colors = {"Ni": "lightgray", "C": "black",} #Define desired colors for atoms in POSCAR/CONTCAR if desired, else default colours will be used

## external function files
io_utils #Collect file locations (POSCAR, CONTCAR, ACF.dat) for subsequent call

atoms #Load atoms

check #Ensure consistency between files, especially with number of atoms and atomic positions between POSCAR/CONTCAR and ACF.dat

analysis #Collect Bader charges and calculate charge difference between 2 states

plotting #Plot Bader charge and save figures

colors #Set atomic colors and colormap for Bader charge

layouts #Set display configurations of ASE images (with colors)

geometry #Shifts in x,y direction where necessary

inputs #Different options of atomic shifting and image collection

# Example
Two examples are provided (the "C6" and "CH2O" folders), which you can use to observe the functionality of this code by running the main.py file. Please note that this is for single hydrogenation of the C6 atom of the furfural molecule and the O7 atom of the F-CH2O molecule. Feel free to delete these examples when running your own code. Please see a figure below:

![Example figure of bader charge changes of C6 hydrogenation of furfural](Bader_plots/Hydrogenation/Hydrogenation_C6.png)
![Example figure of bader charge changes of CH2O hydrogenation of furfural](Bader_plots/Hydrogenation/Hydrogenation_CH2O.png)
