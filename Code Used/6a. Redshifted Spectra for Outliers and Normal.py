from astropy.io import fits
import matplotlib.pyplot as plt
import csv

csv_file_path = 'filtereddata(noduplicates)+x+diff.csv'  

#Asks for the input of a row number in the filtered csv file and obtains the z of the corresponding ID item in that row
try:
    row_number = int(input("Enter the row number: "))

    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row_index, row in enumerate(reader):
            if row_index == row_number - 1: 
                if len(row) >= 6:
                  #the z value is stored in the 6th column
                  #Goes into the 6th column of the ID's corresponding row (inputted) to obtain the z value
                    value = row[5]  
                    print(value)
                    break
                else:
                    print(f"Error: Row {row_number} does not have at least 6 columns")
                    break
        else:
            print(f"Error: Row {row_number} not found in the CSV file")
except ValueError:
    print("Error: Please enter a valid integer for the row number.")

#calculates the factor to shift the graph since (1/(1+z))=λ_rest/λ_observed
shift=1/(1+float(value))
#---------------------------------------------------------------------

file_path = 'Normal/legac_M19_36641_v3.0.fits'

with fits.open(file_path) as hdul:

    wavelength=hdul[1].data['wave'][0]
    flux=hdul[1].data['flux'][0]

  #Adding the vertical red line
    plt.axvline(x=4861, color='r', linestyle='--', label='Hbeta')
  #Adding the label on top of the line
    plt.text(4861, 160, 'Hbeta', color='r', ha='center',fontsize=5)

    plt.axvline(x=3727, color='r', linestyle='--', label='O3727')
    plt.text(3727, 160, 'O3727', color='r', ha='center', fontsize=5)

    plt.axvline(x=4959, color='r', linestyle='--', label='O4959')
    plt.text(4959, 160, 'O4959', color='r', ha='center',fontsize=5)

    plt.axvline(x=5007, color='r', linestyle='--', label='O5007')
    plt.text(5007, 160, 'O5007', color='r', ha='center',fontsize=5)

    #plots the shifted corresponding rest wavelength against flux
    plt.plot((shift*wavelength),flux)

    plt.title('Spectra for ID 36641')
    plt.xlabel('Rest-Frame Wavelength (Å)')
    plt.ylabel('Flux')
  
    plt.show()

