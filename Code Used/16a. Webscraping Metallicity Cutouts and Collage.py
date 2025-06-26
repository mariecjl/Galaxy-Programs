#importing all required libraries
import os
import requests
from astropy.io import fits
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pandas as pd
from PIL import Image

#method for webscraping (downloading the file into the MaNGA Scrape folder)
def download_file(url, folder_name="MaNGA Scrape"):
    #creating a MaNGA Scrape folder the first time the program runs
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    #getting the file name
    filename = url.split("/")[-1]
    #creating the complete file path
    file_path = os.path.join(folder_name, filename)

    #sending a "GET" request to the url specified in order to download the file
    response = requests.get(url)

    #checking if the webscraping was successful
    if response.status_code == 200:
        #writing the webscraped file/data into the specified path (under the folder)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"file downloaded successfully to {file_path}")
    #error message if the download was unsuccessful
    else:
        print(f"download failed: {response.status_code}")
        return None

#deleting a file (I used this method every time the loop ran to avoid running out of storage)
def delete_file(url, folder_name="MaNGA Scrape"):
    #trying to delete a file by specifying the file name and file path
    try:
        filename = url.split("/")[-1]
        file_path = os.path.join(folder_name, filename)
        os.remove(file_path)
        print(f"file {file_path} deleted successfully.")
    #error message if the deletion was unsuccessful
    except Exception as e:
        print(f"error deleting file {file_path}: {e}")

#method for obtaining the file path given the url inputed and the folder in which all data is stored
def get_filepath(url, folder_name="MaNGA Scrape"):
    #trying to obtain the file path, and, if successful, to return it
    try:
        filename = url.split("/")[-1]
        file_path = os.path.join(folder_name, filename)
        return file_path
    #return error message if not successful
    except Exception as e:
        print (f"double check")
    
#-----------------------

def metallicityplot(directory, ifu, url, destination="newcollage"):
    try:
        #open the FITS file and access HDU 4
        hdu4 = fits.open(get_filepath(url))[4].data
        
        #extracting H-alpha (channel 6) and N[II] (channel 7) data
        halpha = hdu4[6]
        nii = hdu4[7]
        
        #masking out any invalid values (zeros and NaNs)
        halpha = np.where((halpha == 0) | np.isnan(halpha), np.nan, halpha)
        nii = np.where((nii == 0) | np.isnan(nii), np.nan, nii)
        
        #calculating the ratio N[II] / H-alpha (avoiding division by zero)
        ratio = np.divide(nii, halpha, out=np.full_like(nii, np.nan), where=(halpha != 0))
        
        #setting color range based on the 3rd and 97th percentile to avoid outliers
        vmin = np.nanpercentile(ratio, 3)
        vmax = np.nanpercentile(ratio, 97)

        #plotting the ratio of [NII]6583 to H-alpha
        plt.imshow(ratio, origin='lower', cmap='inferno', vmin=vmin, vmax=vmax)
        plt.colorbar(label='[NII]6583/H-alpha')
        plt.title(f"{directory}, {ifu} [NII]6583/H-alpha")

        #saving the plot to combine later into the collage
        plt.savefig(f"{destination}.png", bbox_inches='tight', pad_inches=0)
        plt.close()

    except Exception as e:
        print(f"Error processing data for {directory}, {ifu} from {url}: {e}")


#vertical paste (to paste multiple horizontal cutout-out trios together)
def verticalpaste(cutout,collage,finalimg="newcollage"):
    #open the cutout and the collage (the image to be pasted and the one onto which it's pasted)
    cutout=Image.open(cutout+'.png')
    collage = Image.open(collage+'.png')

    #obtaining the height and widths of both the collage and the cutout
    width1, height1 = collage.size
    width2, height2 = cutout.size

    #defining a new width and new height based off of the collage and the new cutout
    new_width = max(width1, width2)
    new_height = height1 + height2

    #making the updated collage by adding the new cutout to the bottom
    newcollage = Image.new('RGB', (new_width, new_height))

    width1, height1 = collage.size
    width2, height2 = cutout.size

    #pasting the original collage on top
    newcollage.paste(collage, (0, 0))
    newcollage.paste(cutout, (0, height1))

    #saving the collage obtained for the combination of three filters
    newcollage.save(finalimg+'.png')

#I made a csv file of all of the parent directories so the program could just go through the csv file to access all directories
df = pd.read_csv('/Users/marie/Desktop/MaNGA Scrape/Code/parentdirectories.csv')

for i in range(0, 615):
    #when I didn't want my laptop running for too long, I set the  two lines below with a target directory number, so the code would automatically break when it reached that number
    #if i==606:
        #break
    
    #I copied the list of IFUs used (the same IFUs were seen throughout all parent directories)
    for ifu in ('12701', '12702', '12703', '12704', '12705', '1901', '1902', '3701', '3702', '3703', '3704', '6101', '6102', '6103', '6104', '9101', '9102'):
        
        #obtaining the MaNGA-assigned number of the current parent directory
        parentdirectory=df.iat[i,0]
        print(parentdirectory)
        #generating a unique url through the combination of parent directories and IFUs
        url = f"https://data.sdss.org/sas/dr17/manga/spectro/pipe3d/v3_1_1/3.1.1/{parentdirectory}/manga-{parentdirectory}-{ifu}.Pipe3D.cube.fits.gz"
        
        #try to webscrape at the URL, but pass if any errors occur.
        try:
            download_file(url)
            print(ifu+" succeeded")
        except Exception as e:
            print(ifu+" excepted, passing")
            pass

        #for each of my vertical collages, I limited it to 3 parent directories (so the collage would not get excessively big and slow the program)
        #so for every third parent directory, and if the IFU was the first one on the list, I created a new collage
        if (i%3==0 and ifu=='12701'):
            directorysetter=parentdirectory
            print(directorysetter)
            #the collage is named after the three parent directories whose cutouts are included
            metallicityplot(parentdirectory,ifu,url,f"newcollage{directorysetter}, {int(directorysetter)+1}, {int(directorysetter)+2}.png")

        #if a new directory is not being created, the cutout is directly pasted onto the collage
        else:
            metallicityplot(parentdirectory,ifu,url,"cutout")
            verticalpaste("cutout",f"newcollage{directorysetter}, {int(directorysetter)+1}, {int(directorysetter)+2}.png",f"newcollage{directorysetter}, {int(directorysetter)+1}, {int(directorysetter)+2}.png")
        
        #delete the webscraped MaNGA file so as to reduce the storage usage
        delete_file(url)
