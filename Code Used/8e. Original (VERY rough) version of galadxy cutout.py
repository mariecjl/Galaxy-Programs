#importing all the needed packages/libraries
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style
from astropy.io import fits
from astropy.utils.data import get_pkg_data_filename
import numpy as np
import pandas as pd
from PIL import Image

#accessing the ra+dec file path and that of the filtered file
radec = 'radec.csv'
filtered_file_path = 'filtereddata(noduplicates)+x+diff.csv'

#obtain the IDs (column 1) of the filtered csv file as a list
filtered_df = pd.read_csv(filtered_file_path)
filtered_ids = filtered_df.iloc[:, 0].tolist()

#Read the data of the ra+dec file
radec_df = pd.read_csv(radec)

#obtain the rows in the ra+dec file with overlapping IDs as the IDs of the filtered csv file
filtered_radec = radec_df[radec_df.iloc[:, 0].isin(filtered_ids)]

#obtaining the cosmos image file
image_file = get_pkg_data_filename('COSMOS444.fits')
image_data = fits.getdata(image_file, ext=1)

#the cutout size for each galaxy is 100x100 pixels
half_cutout_size=50

#the location coordinates of where the ID is written
text_x = 10
text_y = 10

#initial pasting position for UV Clumpy
pos_x_Y=50
pos_y_Y=50

#initial pasting position for Non UVClumpy
pos_x_N=50
pos_y_N=50

#iterate through each row of the combined filtered and ra+dec data
for index, row in filtered_radec.iterrows():
#if both the object's ra and dec fall within the range imaged
#on the cosmos website it said that "The COSMOS survey is centered at (J2000):RA +150.11916667 (10:00:28.600)DEC +2.20583333 (+02:12:21.00)"
#I calculated the range by looking at the image dimensions, then the # of pixels per arcsec (0.06 arcsec=1 pixel)
   if (((150.11916667-0.125)<row.iloc[1]<(150.11916667+0.125)) and ((2.20583333-0.15)<row.iloc[2]<(2.20583333+0.15))):
       
       #I found the row index for each of the objects in order to find their corresponding UVClumpy value
       csv_row_index = filtered_df[filtered_df.iloc[:, 0] == row.iloc[0]].index.tolist()
       #UVClumpy is in the 5th column
       color = filtered_df.iloc[csv_row_index[0], 4]
       #If it's clumpy, the background to which it's pasted is whiteY.jpg (the Y stands for yes-clumpy :))
       if (color == 1.0):
           background = Image.open("whiteY.jpg")

        #If it's not clumpy, the background to which it's pasted is whiteN.jpg
       else:
           background = Image.open("whiteN.jpg")
        #Both whiteN and whiteY are just a plane white backdrop
      
       #Obtain the ra value
       ra = row.iloc[1]
       #find its difference in image (pixel) coordinates from the image's centre
       ra_diff=((ra-150.11916667)*3600)/0.06
       #find the galaxy cutout's centre x-value
       cutout_x=7500+ra_diff
       
       #doing the same for the dec value
       dec=row.iloc[2]
       dec_diff=((dec-2.20583333)*3600)/0.06
       cutout_y=9000-dec_diff
      
       #using the built-in plotting style for astropy
       plt.style.use(astropy_mpl_style)

       #cutout the image data centred around (cutout_x, cutout_y) as we've determined
       #the bounds are expressed as [y,x]
       cutout_data = image_data[round(cutout_y) - half_cutout_size:round(cutout_y) + half_cutout_size,round(cutout_x) - half_cutout_size:round(cutout_x) + half_cutout_size]
       
       plt.figure()
       plt.imshow(cutout_data, cmap='gray', origin='lower')
       plt.colorbar()
       
       #because when I outputted the array for each cutout, the white portion returned the value "nan" for some galaxies which I think is because it hasn't be imaged yet, I defined "nan" to correspond to the color white (1.0)
       cutout_data[np.isnan(cutout_data)] = 1.0

       #I had to convert the cutout to rgb because the background image is and without converting, the code kept on returning errors :(
       cutout_data_rgb = np.repeat(cutout_data[:, :, np.newaxis], 3, axis=2)
      
       plt.figure()
       plt.imshow(cutout_data_rgb, origin='lower')
      
      #Printing the ID value of each galaxy in red, at the bottom corner of each cutout
       plt.text(text_x, text_y, row.iloc[0], color='red', fontsize=30)
      
      #I saved the image so it can better be accessed and pasted as an overlay image
       plt.savefig('rbg.png')

       overlay = Image.open("rbg.png")

       #defining the pasting position based off of UVClumpiness (which also determines which image it'll be pasted onto)
       if (color == 1.0):
           position=(pos_x_Y, pos_y_Y)
       else:
           position=(pos_x_N, pos_y_N)
      
      #pasting it onto the background
       background.paste(overlay, position, overlay)
      
      #saving (updating) the background file (which now contains a new cutout) and updating the pasting coordinates for the next cutout to be pasted
       if (color == 1.0):
           background.save("whiteY.jpg")
           pos_x_Y+=500
           if (pos_x_Y>=2400):
               pos_y_Y+=500
       else:
           background.save("whiteN.jpg")
           pos_x_N+=500
           if (pos_x_N>=2400):
               pos_y_N+=500
