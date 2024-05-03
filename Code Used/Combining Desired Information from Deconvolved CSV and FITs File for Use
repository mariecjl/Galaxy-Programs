from astropy.table import Table
from astropy.io import fits
import csv

#id_list, ra_list, and dec_list are all for the fits file
#FITS FILE INFO PROCESSING
id_list=[]
zspec=[]
o3727=[]
o4959=[]
o5007=[]
hbeta=[]


csv_file_path = 'Astro Data Catalogs/deconvolved.csv'  
csv_combined_path= 'Astro Data Catalogs/plotdata.csv'

fitspath = 'Astro Data Catalogs/LEGA-C.fits'

fitstable = Table.read(fitspath)

for i in range (0,len(fitstable)):
    id_list.append(float(fitstable[i][1]))
    zspec.append(float(fitstable[i][14]))
    o3727.append(float(fitstable[i][61]))
    o4959.append(float(fitstable[i][89]))
    o5007.append(float(fitstable[i][93]))
    hbeta.append(float(fitstable[i][85]))

#print (o3727)

#-----------------------------------------------------------------------
#CSV FILE INFO PROCESSING

def read_column_from_csv(file_path, column_index):
    data_list = []

    with open(file_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)

        for row in csv_reader:
            if len(row) > column_index:
              if (row[column_index])!="id" and (row[column_index])!="ra" and (row[column_index])!="dec" and (row[column_index])!="log_mass" and (row[column_index])!="log_sfr" and (row[column_index])!="is_mass_clumpy" and (row[column_index])!="is_UV_clumpy":
                if row[column_index]=="False":
                  data_list.append(float(0))
                elif row[column_index]=="True":
                  data_list.append(float(1))
                #if (row[column_index])!="id" and (row[column_index])!="ra" and (row[column_index])!="dec" and (row[column_index])!="ra" and row([column_index])!="log_mass" and (row[column_index])!="log_sfr":
                else:  
                  data_list.append(float(row[column_index]))

    return data_list

#csvid, csvra, csvdec are for the CSV file
#all csv id
csvid = read_column_from_csv(csv_file_path, 1)

#stellar mass
smass = read_column_from_csv(csv_file_path, 6)

#stellar formation
sfr = read_column_from_csv(csv_file_path, 7)

#mass clumpy
massc = read_column_from_csv(csv_file_path, 8)

#uv clumpy
uvc = read_column_from_csv(csv_file_path, 9)

#combined id 
combined_id = read_column_from_csv(csv_combined_path, 0)

#print (combined_id)


#---------------------------------------------------------------------------
#obtained from csv
combined_smass=[]
combined_sfr=[]
combined_massc = []
combined_uvc = []

#obtained from fits
combined_zspec=[]
combined_o3727=[]
combined_o4959=[]
combined_o5007=[]
combined_hbeta=[]

for i in combined_id:
  if (i in csvid) and (i in id_list):
    #print (i)
    index = csvid.index(i)
    combined_smass.append(smass[index])
    combined_sfr.append(sfr[index])
    combined_massc.append(massc[index])
    combined_uvc.append(uvc[index])
    
    index1 = id_list.index(i)
    combined_zspec.append(zspec[index1])
    combined_o3727.append(o3727[index1])
    combined_o4959.append(o4959[index1])
    combined_o5007.append(o5007[index1])
    combined_hbeta.append(hbeta[index1])
    
#print (combined_smass)
print (len(combined_hbeta))

combined_r23=[]
for k in range (0,len(combined_hbeta)):
  if (combined_hbeta[k] == 0):
    combined_r23.append ("N/A")
  else:
    r23 =((combined_o3727[k]+combined_o4959[k]+combined_o5007[k])/(combined_hbeta[k]))
    combined_r23.append(r23)
  
print (len(combined_r23))
#------------------------------------------------------------------------------
#The RAs and Decs are indeed as shown in the data output

#-----------------------------------------------------------------------------------------
#PRINTING ALL DATA INTO A CSV FILE
#print (combined_zspec)

csv_file_path = "Astro Data Catalogs/plotdataforuse.csv"

# Open the existing CSV file in append mode
with open(csv_file_path, mode='a', newline='') as file:
    csv_writer = csv.writer(file)

    # Zip the lists together and iterate over corresponding elements
    
    for combined_id_values, smass_values, sfr_values, massc_value, uvc_value, zspec_value, o3727_value, o4959_value, o5007_value, hbeta_value, r23_value in zip(combined_id, combined_smass, combined_sfr, combined_massc, combined_uvc, combined_zspec, combined_o3727,combined_o4959, combined_o5007, combined_hbeta, combined_r23):
        csv_writer.writerow([combined_id_values, smass_values, sfr_values, massc_value, uvc_value, zspec_value, o3727_value, o4959_value, o5007_value, hbeta_value, r23_value])

print(f"Data has been added to {csv_file_path}.")
