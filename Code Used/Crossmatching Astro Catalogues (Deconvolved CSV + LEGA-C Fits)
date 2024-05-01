from astropy.table import Table
from astropy.io import fits
import csv

#id_list, ra_list, and dec_list are all for the fits file
#FITS FILE INFO PROCESSING
id_list=[]
ra_list=[]
dec_list=[]

csv_file_path = 'Astro Data Catalogs/deconvolved.csv'  


fitspath = 'Astro Data Catalogs/LEGA-C.fits'

fitstable = Table.read(fitspath)

for i in range (0,len(fitstable)):
    id_list.append(float(fitstable[i][1]))
    ra_list.append(float(fitstable[i][4]))
    dec_list.append(float(fitstable[i][5]))

#-----------------------------------------------------------------------
#CSV FILE INFO PROCESSING
column_index_to_read1 = 1 # Index 1 corresponds to the second column (0-based index)
column_index_to_read2 = 2
column_index_to_read3 = 3

def read_column_from_csv(file_path, column_index):
    data_list = []

    with open(file_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)

        for row in csv_reader:
            if len(row) > column_index:
                if (row[column_index])!="id" and (row[column_index])!="ra" and (row[column_index])!="dec":
                    data_list.append(float(row[column_index]))

    return data_list

#csvid, csvra, csvdec are for the CSV file
csvid = read_column_from_csv(csv_file_path, column_index_to_read1)
csvra = read_column_from_csv(csv_file_path, column_index_to_read2)
csvdec = read_column_from_csv(csv_file_path, column_index_to_read3)

#---------------------------------------------------------------------------
print (id_list)
#MATCHING THE FITS FILE WITH THE CSV FILE
samefitsid=[]
samefitsra=[]
samefitsdec=[]

samecsvid=[]
samecsvra=[]
samecsvdec=[]

for k in range (0,len(csvid)):
  #(0,101) this will go from 0 and 100 (included)
  if k%100==0:
    print (k)
  for l in range (0,len(ra_list)):
    if (float(ra_list[l])-0.0001)<=float(csvra[k])<=(float(ra_list[l])+0.0001):
      if (float(dec_list[l])-0.0001)<=float(csvdec[k])<=(float(dec_list[l])+0.0001):
        #print ("Matching items: CSV:",csvid[k]," Fits ID:",id_list[l]," CSV Ra:",csvra[k]," CSV Dec:",csvdec[k], " Fits RA:",ra_list[l]," Fits Dec:",dec_list[l])

        samefitsid.append(id_list[l])
        samefitsra.append(ra_list[l])
        samefitsdec.append(dec_list[l])

        samecsvid.append(csvid[k])
        samecsvra.append(csvra[k])
        samecsvdec.append(csvdec[k])

print ("# of Items of the list for the CSV ID that yielded close RAs and Decs with FITS:",len(samecsvid))
print ("# of Items of the list for the FITS ID that yielded close RAs and Decs with CSV:",len(samefitsid))


#--------------------------------------------------------------------------------
#TESTING AND DOUBLE-CONFIRMING (BC OF THE STRANGE ID OUTPUT)
#Testing the number of IDs in the two lists that are the same:
sameid=[]
for m in id_list:
  if m in csvid:
    sameid.append(m)
#There are 1804 repeated IDs across both lists which is exactly the same number as number of IDs in the cross-matched dataset

print ("# of repeated IDs in the two datasets:",len(sameid))

#for CSV ID 261500.0 and FITs ID 261500.0 are said to have very close (within 0.0001) RAs and Decs so here we check their actual RAs and Decs in the created lists
testindexcsv=csvid.index(261500.0)
print ("Corresponding CSV ID 261500.0's RA value:",csvra[testindexcsv], " Dec value:",csvdec[testindexcsv])

testindexfits=id_list.index(261500.0)
print ("Corresponding FITS ID 261500.0's RA value:",ra_list[testindexfits], " Dec value:",dec_list[testindexfits])
#The RAs and Decs are indeed as shown in the data output

#-----------------------------------------------------------------------------------------
#PRINTING ALL DATA INTO A CSV FILE

csv_file_path = "Astro Data Catalogs/combined.csv"

# Open the existing CSV file in append mode
with open(csv_file_path, mode='a', newline='') as file:
    csv_writer = csv.writer(file)

    # Zip the lists together and iterate over corresponding elements
    for csvid_value, csvra_value, csvdec_value, fitsid_value, fitsra_value, fitsdec_value in zip(samecsvid,samecsvra, samecsvdec,samefitsid, samefitsra, samefitsdec):
        csv_writer.writerow([csvid_value, csvra_value, csvdec_value, fitsid_value, fitsra_value, fitsdec_value])

print(f"Data has been added to {csv_file_path}.")
