#import all packages/libraries
from astropy.io import fits
import pandas as pd
import csv

#read the filtered csv file (the filtered csv file was the file whose data I used to create all of my past graphs)
csv_file_path = "filtereddata(noduplicates)+x+diff.csv"
csv_data = pd.read_csv(csv_file_path)
csvlist = csv_data.iloc[:, 0].tolist() #obtaining the IDs of the filtered csv file (1st column)

#reading the LEGA-C fits file
fits_file_path = "LEGA-C.fits"
fits_data = fits.open(fits_file_path)
fitslist = fits_data[1].data.field(1).tolist()  #the IDs are stored in the 2nd column for the fits file
fits_table = fits_data[1].data
fits_data.close()

#the columns for OII3727, NEIII3869, OIII4959, OIII5007, and HBeta are respectively in columns 62, 66, 90, 94, and 86
column_indices = [62, 66, 90, 94, 86]

#creating a new csv file to store the values (OII3727, NEIII3869, OIII4959, OIII5007, and HBeta)
NEIII_csv_path = "NEIII.csv"

with open(NEIII_csv_path, 'w', newline='') as NEIII_csv:
    csv_writer = csv.writer(NEIII_csv)
    for csv_value in csvlist:
        try:
          #find the index for each row in the Fits file containing the IDs in the filtered CSV file
            index_in_fitslist = fitslist.index(csv_value)
          #Obtain the desired values (from their respective columns) in each of the above Fits row indices
            fits_row_values = [fits_table[index_in_fitslist][col_idx - 1] for col_idx in column_indices]
          #Write the obtained values in the NEIII csv file
            csv_writer.writerow([csv_value] + fits_row_values)

        #error output
        except ValueError:
            print(f"CSV Value: {csv_value} not found in FITS List")

print(f"Error values written to {NEIII_csv_path}")

