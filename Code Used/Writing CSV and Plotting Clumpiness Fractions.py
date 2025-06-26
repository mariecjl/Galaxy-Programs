#importing all libraries needed
import csv
from astropy.io import fits
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#file paths for the DAP and DRP files downloaded from MaNGA
dapfile = "/Users/marie/Desktop/MaNGA Scrape/dapall-v3_1_1-3.1.0.fits"
drpfile = "/Users/marie/Desktop/MaNGA Scrape/drpall-v3_1_1.fits" 

#Method for writing the desired columns of the DAP & DRP file into their respective CSV files
#I only called this method the first time I ran the program to create the CSV files
def write_csv(fits_file, output_csv, *column_hdu_pairs):
   #opening the fits file and extracting data
    with fits.open(fits_file) as hdul:
        extracted_data = []
        
        # for each column and corresponding HDU...
        for column, hdu_index in column_hdu_pairs:
            #ensuring the HDU index range is valid
            if len(hdul) > hdu_index:
                #accessing the specified HDU's data and extracting the specified column
                data = hdul[hdu_index].data  
                extracted_data.append(data[column])
            else:
                #error message (so I could double-check if anything went wrong)
                print(f"Error: HDU index {hdu_index} is out of range. This file has {len(hdul)} HDUs.")
                return
        
        # Writing the data obtained in a CSV file
        with open(output_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            #writing the column names (headers)
            writer.writerow([pair[0] for pair in column_hdu_pairs])
            
            # writing the data rows
            for row in zip(*extracted_data):
                writer.writerow(row)

    print(f"CSV file '{output_csv}' has been written successfully.")

#In the first time running the program, I ran this to write the dap and drp file, then I commented it out in subsequent runs
#write_csv(drpfile, "/Users/marie/Desktop/MaNGA Scrape/drpdata.csv", ("plateifu",1), ("nsa_elpetro_mass",1))
#write_csv(dapfile, "/Users/marie/Desktop/MaNGA Scrape/dapdata.csv", ("PLATEIFU",1), ("STELLAR_SIGMA_1RE",1), ("HA_GSIGMA_1RE",1), ("SFR_TOT ",1))

#reading DAP, DRP and clumpiness data through the csv file
df_dap = pd.read_csv("/Users/marie/Desktop/MaNGA Scrape/dapdata.csv")
df_drp = pd.read_csv("/Users/marie/Desktop/MaNGA Scrape/drpdata.csv")
df_clumpy=pd.read_csv("/Users/marie/Desktop/MaNGA Scrape/clumpy classification.csv")

#Combine the clumpiness file's plate and IFU together (since the DRP and DAP combines them (PlateIFU))
df_clumpy['clumpyplateifu'] = df_clumpy[df_clumpy.columns[0]].astype(str) + '-' + df_clumpy[df_clumpy.columns[1]].astype(str)

#Getting the PlateIFU values from the DAP and DRP files
dap_plateifu = df_dap.iloc[:, 0].astype(str)
drp_plateifu=df_drp.iloc[:, 0].astype(str)

#Merging the clumpiness CSV with either the DAP or DRP CSV using the PlateIFU of both
merged = pd.merge(df_clumpy, df_drp, left_on='clumpyplateifu', right_on=df_drp.columns[0])

#print(merged.columns)

#X_col corresponds to the variable on the x-axis of the plots
x_col='nsa_elpetro_mass'
#Obtaining the mass and H-alpha clumpy columns in the merged data
y_mass_raw = merged['mass_isclumpy']
y_halpha_raw=merged['ha_isclumpy']
#Obtaining the x-variable from the merged variable
x_raw = merged[x_col]

#to avoid outliers, I only used x-data which were between the 1st and 99th percentiles
x_1 = np.percentile(x_raw, 1)
x_99 = np.percentile(x_raw, 99)
#applying the mask to x
mask = (x_raw >= x_1) & (x_raw <= x_99)
x = x_raw[mask]

#ensuring we only use y-values with corresponding x satisfies the range requirements
y_mass = y_mass_raw[mask]
y_halpha = y_halpha_raw[mask]


#print(y_mass)
#print(y_halpha)
#print(x)

#Sorting the x-values
sorted_indices = np.argsort(x)
x_sorted = x.iloc[sorted_indices]
#Sorting the y-values so each y still corresponds to/aligns with its correct x
y_mass_sorted = y_mass.iloc[sorted_indices]
y_halpha_sorted=y_halpha.iloc[sorted_indices]

#Creating 10 bins (10 intervals)
bins = np.linspace(min(x_sorted), max(x_sorted), 11)

#print(bins)

#Creating empty lists for the clumpiness fractions (for mass and Halpha clumpy) and the centers of each bin
mass_percentages = []
halpha_percentages=[]
bin_centers = []

#Iterating through each bin
for i in range(1, len(bins)):
    #Creating a mask to only select x values within the bin's range
    bin_mask = (x_sorted >= bins[i-1]) & (x_sorted < bins[i])
    #applying the mask to all x values, and the clumpiness fractions whose x value satisfies the mask
    bin_x = x_sorted[bin_mask]
    bin_y_mass = y_mass_sorted[bin_mask]
    bin_y_halpha = y_halpha_sorted[bin_mask]
    
    #calculating the clumpiness fraction of mass clumpy galaxies
    mass_percentage = np.mean(bin_y_mass) * 100 
    mass_percentages.append(mass_percentage)

    #calculating the clumpiness fraction of Halpha clumpy galaxies
    halpha_percentage = np.mean(bin_y_halpha) * 100 
    halpha_percentages.append(halpha_percentage)
    
    #calculating the average x-value within the bin (mean of the bin's x-values)
    if len(bin_x) > 0:
        bin_center = np.mean(bin_x)
    #if there are no values within a bin, set the bin's center to be NaN
    else:
        bin_center = np.nan
    
    bin_centers.append(bin_center)

#print(bin_centers)
#print(halpha_percentages)
#print(mass_percentages)

#setting up the plot
plt.figure(figsize=(8, 6))
#creating the scatter plot for mass and Halpha clumpy galaxies
plt.scatter(bin_centers, mass_percentages, marker='o', color='r', label="Mass Clumpy Fraction")
plt.scatter(bin_centers, halpha_percentages, marker='o', color='b', label="Halpha Clumpy Fraction")
#adding the legend
plt.legend()
#displaying the x-label
plt.xlabel(x_col)
#displaying the y-label (for clumpiness percentage)
plt.ylabel('Clumpy Percentage')
#adding a graph title
plt.title('Clumpiness Fraction v. '+x_col)
plt.grid(True)
plt.show()
