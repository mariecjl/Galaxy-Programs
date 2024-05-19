#importing all libraries and packages needed
from astropy.io import fits
from astropy.wcs import wcs
from astropy.coordinates import SkyCoord
from astropy.nddata import Cutout2D
import matplotlib.pyplot as plt
import numpy as np
from astropy import units as u
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

#the location coordinates of where the ID is written
text_x = 10
text_y = 10

#initial pasting position for UV Clumpy
pos_x_Y=50
pos_y_Y=50

#initial pasting position for Non UVClumpy
pos_x_N=50
pos_y_N=50

#opening the COSMOS Web Fits File
with fits.open('COSMOS444.fits') as hdul:
            #All of the information was stored in extension #1
            hdu=hdul[1]
            data=hdul[1].data

            #defining number of axis
            w = wcs.WCS(naxis=2)

            #I created the WCS values by using the values present in the file's header
            w.wcs.crval = [hdu.header['CRVAL1'],hdu.header['CRVAL2']]
            w.wcs.cdelt = [hdu.header['CDELT1'],hdu.header['CDELT2']]
            w.wcs.crpix = [hdu.header['CRPIX1'],hdu.header['CRPIX2']]
            w.wcs.ctype = [hdu.header['CTYPE1'],hdu.header['CTYPE2']]
            w.array_shape = [15000, 18000]
            w.wcs.pc = [hdu.header['PC1_1'],hdu.header['PC1_2']],[hdu.header['PC2_1'],hdu.header['PC2_2']]

            #finding the bounds of the RA and Dec values surveyed (I think the RA axis is flipped since taking the min actually outputted the larger RA value (hence the naming :))
            maxra=np.min(w.wcs_pix2world(np.array([[0, 0]]), 1)[0, 0])
            minra=np.max(w.wcs_pix2world(np.array([[data.shape[1], data.shape[0]]]), 1)[0, 0])
            mindec=np.min(w.wcs_pix2world(np.array([[0, 0]]), 1)[0, 1])
            maxdec=np.max(w.wcs_pix2world(np.array([[data.shape[1], data.shape[0]]]), 1)[0, 1])

for index, row in filtered_radec.iterrows():
#if both the object's ra and dec fall within the range imaged
   if ((minra)<row.iloc[1]<(maxra)) and ((mindec)<row.iloc[2]<(maxdec)):
       
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
       dec=row.iloc[2]

        #converting the RA and Dec values to the pixel values (x and y coordinates)
       px, py = w.wcs_world2pix(ra, dec, 1)
       #print('{0} {1}'.format(px, py))
       
       #position at which the cutout is centred
       position = (px, py)
       
       #taking the cutout
       cutout = Cutout2D(data, position, (100, 100))
       plt.figure()
       plt.imshow(cutout.data, origin='lower')
       plt.colorbar()
       
       #Adding the galaxy ID at the corner 
       plt.text(text_x, text_y, row.iloc[0], color='red', fontsize=30)
       print (row.iloc[0])
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
           pos_x_Y+=600
           if (pos_x_Y>=2400):
               pos_y_Y+=500
               pos_x_Y=50
       else:
           background.save("whiteN.jpg")
           pos_x_N+=600
           if (pos_x_N>=2400):
               pos_y_N+=500
               pos_x_N=50
