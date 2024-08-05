#importing everything
import urllib.request
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#adding file paths
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
pos_x_Y=368
pos_y_Y=61

#initial pasting position for Non UVClumpy
pos_x_N=368
pos_y_N=61

#I made a list for all the IDs that did not have cutouts
no_cutout=[]

for index, row in filtered_radec.iterrows():
  csv_row_index = filtered_df[filtered_df.iloc[:, 0] == row.iloc[0]].index.tolist()
   #UVClumpy is in the 5th column
  color = filtered_df.iloc[csv_row_index[0], 4]
   #Obtain the ra and dec value
  ra = row.iloc[1]
  dec=row.iloc[2]

  #actually "scraping" the image
  urllib.request.urlretrieve("https://grizli-cutout.herokuapp.com/thumb?ra="+str(ra)+"&dec="+str(dec)+"&size=3&filters=f814w,f115w-clear,f150w-clear,f277w-clear,f444w-clear&rgb_scl=1.5,0.74,1.3&asinh=True&all_filters=True", "test.png")
  
  try:
    image = mpimg.imread("test.png")
    plt.imshow(image)

    #adding the galaxy ID at the corner
    plt.text(text_x, text_y, row.iloc[0], color='red', fontsize=30)
    #print (row.iloc[0])
    #I saved the image so it can better be accessed and pasted as an overlay image
    plt.savefig('cutout.png')

    #clear it so the text doesn't overlap with new cutouts
    plt.clf()

  #sometimes a ra-dec pairing will not yield a cutout, so we use a custom error message to skip it
  except SyntaxError as e:
    # handling the case where the file is not a valid PNG
    if str(e) == 'not a PNG file':
      #outputting the ID of the galaxy that doesn't have a cutout
        print("This ID has no cutout: "+str(row.iloc[0]))
        no_cutout.append(row.iloc[0])
    else:
        raise
      
  #if it's UVClumpy, we paste it onto the UVClumpy collage
  if (color==1.0):
    collage = Image.open('clumpy.png')

  #if it's UV Nonclumpy, we paste it onto the Non-UVClumpy collage
  else:
    collage=Image.open('nonclumpy.png')

  #opening the cutout
  cutout = Image.open('cutout.png')

  #measuring the image dimensions to better paste the cutout onto the collage (since the collage will become very long (height will change with every loop run))
  width1, height1 = collage.size
  width2, height2 = cutout.size

  #defining a new width and new height based off of the collage and the new cutout
  new_width = max(width1, width2)
  new_height = height1 + height2

  #making the updated collage by adding the new cutout to the bottom
  newcollage = Image.new('RGB', (new_width, new_height))

  #pasting the original collage on top
  newcollage.paste(collage, (0, 0))
  #new cutout on the bottom
  newcollage.paste(cutout, (0, height1))

  #saving the updated collage
  if (color==1.0):
    newcollage.save('clumpy.png')
  else:
    newcollage.save('nonclumpy.png')
