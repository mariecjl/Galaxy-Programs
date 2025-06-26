#importing all libraries used (matplotlib, numpy, astropy, Pandas)
import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
import pandas as pd

#from clumps import NormalizedMaps and Galaxy
from clumpsNoPlot import NormalizedMaps
from clumpsNoPlot import Galaxy

#importing csv, OS module and other packages for processing and analyzing images
import csv
import os
import requests
from photutils.segmentation import detect_sources
from astropy.stats import sigma_clipped_stats
from skimage.segmentation import expand_labels

#reading in the CSV file which contains all the plate numbers (Parent directories)
df = pd.read_csv("/Users/marie/Desktop/Clump Classification/parentdirectories.csv")

#----------------------------
#This is just the method used in the MaNGA Scrape to generate file paths for later use in downloading files
def get_filepath(url, folder_name="MaNGA Scrape"):
    #trying to obtain the file path, and, if successful, to return it
    try:
        filename = url.split("/")[-1]
        file_path = os.path.join(folder_name, filename)
        return file_path
    #return error message if not successful
    except Exception as e:
        print (f"double check")

#----------------------
#Method to download a file from the SDSS release website
def download_file(url, folder_name="MaNGA Scrape"):
    #creating a MaNGA Scrape folder the first time the program runs
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    #getting the file name
    filename = url.split("/")[-1]
    #creating the complete file path
    file_path = os.path.join(folder_name, filename)

    #sending a "GET" request to the url specified in order to download the file
    response = requests.get(url, stream=True)

    #checking if the webscraping was successful
    if response.status_code == 200:
        #writing the webscraped file/data into the specified path (under the folder)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"file downloaded successfully to {file_path}")
        return True
    #error message if the download was unsuccessful
    else:
        print(f"download failed: {response.status_code}")
        return False

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

#-------------------------
with open('clumpy.csv', mode='a', newline='') as file:
    #Opening CSV to write new lines
    writer = csv.writer(file)
    
    #Going through the parent directories of plate numbers as loaded in the CSV file
    for i in range(0, 615):
        for ifu in ('12701', '12702', '12703', '12704', '12705', '1901', '1902', '3701', '3702', '3703', '3704', '6101', '6102', '6103', '6104', '9101', '9102'):

            parentdirectory = df.iat[i, 0]

            #Generating a url for the file path of the FITS file
            url = f"https://data.sdss.org/sas/dr17/manga/spectro/pipe3d/v3_1_1/3.1.1/{parentdirectory}/manga-{parentdirectory}-{ifu}.Pipe3D.cube.fits.gz"
            
            #Trying to download the FITS file from the SDSS website
            try:
                success = download_file(url, "Clump Classification")
                #If the download was not successful, the code outputs an error message and goes on to the next IFU
                if not success:
                    print(f"Skipping {url} due to failed download.")
                    continue
            #If there are any other errors, an error message is also outputed.
            except Exception as e:
                print(f"Unexpected error: {e}")
                continue
            
            #Generating the file path 
            manga_datacube_filename = get_filepath(url, "Clump Classification")
            
            #Accessing the FITS file data of HAlpha emission lines
            elines = fits.open(manga_datacube_filename)[4].data
            ha_line_map = elines[6]

            #Accessing the FITS file data of the mass maps
            ssps = fits.open(manga_datacube_filename)[1].data
            mass_map = ssps[19]

            #this is just to handle if the HAlpha or Mass map didn't exist (or if all pixels were 0 or NaN)
            #skips onto the next iteration if the maps do not contain necessary data
            if np.all(ha_line_map == 0) or np.all(np.isnan(ha_line_map)) or np.all(mass_map == 0) or np.all(np.isnan(mass_map)):
                print("Skipping iteration: ha_line_map or mass_map is empty or NaN")
                continue

            #computes statistics of the H-alpha line map
            mean, _, std = sigma_clipped_stats(ha_line_map, sigma=4.0)
            threshold = 5 * std
            
            #detect sources and regions of significant signal in the H-alpha line map
            segment_map = detect_sources(ha_line_map, threshold, npixels=10, connectivity=4)

            #if no sources were detected, print a message and move to the next iteration
            if segment_map is None:
                print("No segment map. Go on to the next iteration")
                continue

            #expand sources by 3 pixels
            segmap = expand_labels(segment_map.data, distance=3).astype(float)
            segmap[segmap == 0] = np.nan

            #store galaxy information
            galinfos = {
                "platenumber": parentdirectory,
                "plateifu": str(parentdirectory)+" "+str(ifu),
            }

            #creating a dictionary of relevant data maps
            maps = {
                "ha": ha_line_map * segmap, 
                "mass": 10**mass_map * segmap,
                "weighted_map": np.ones_like(ha_line_map),
                "segmap": segmap,
            }

           #try to create a NormalizedMap by using galaxy and map information
            try:
                normmaps = NormalizedMaps(galinfos, maps)
                #determines if the galaxy is clumpy in the mass and halpha maps
                isclumpy = normmaps.is_clumpy(mapTypes=["mass", "ha"], plot_profiles=False)
            #if there are any errors, the code will skip to the next iteratiojn
            except Exception as error:
                continue
            
            print(isclumpy)

            #write the results of the clumpiness classification in the CSV file
            writer.writerow([galinfos["platenumber"], ifu, isclumpy['mass_isclumpy'], isclumpy['ha_isclumpy']])
            #delete the FITS file downloaded to free storage
            delete_file(url, "Clump Classification")
