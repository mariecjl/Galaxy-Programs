import csv
from astropy.io import fits
from astropy.table import Table

#setting up lists for the ids in each file
csvid = []
vreid = []
commonid = []
legacid = []

#setting up lists for the indices of those corresponding ids
legacindex=[]
filteredindex=[]
vreindex=[]


csvcombined = 'Inputs/filtereddata.csv'

#going through the csv file and adding the ids (1st column) to the lists
with open(csvcombined, 'r') as csvfile:
    csv_reader = csv.reader(csvfile)

    for row in csv_reader:
        csvid.append(row[0])

#read the file's contents and store in lists for easier access later on
with open(csvcombined, 'r') as infile:
  reader = csv.reader(infile)
  csvdata = list(reader)

#---------------------------------------------------------------------
fitsvre = 'Inputs/kinematics.fits'

#reading data
fitsvredata = fits.getdata(fitsvre)

#printing the values in the second column (the ids) and adding them to a list
idvre = fitsvredata.field(1)
for i in idvre:
    vreid.append(i)

#checking the common ids between the new kinematics file and the csvcombined file
for item in vreid:
  for k in range (0,len(csvid)):
    if float(item)==(float(csvid[k])):
      commonid.append(item)


#-------------------------
#storing lega-c ids into a list (so I can access the corresponding velocity dispersions)
legacfits = 'Inputs/LEGA-C.fits'
legacdata = fits.getdata(legacfits)
idlegac = legacdata.field(1)
for j in idlegac:
  legacid.append(j)

#------------------------
#find all the indices (row number) of the shared ids in their respective files
for id in (commonid):
  legacindex.append(legacid.index(float(id)))
  filteredindex.append(csvid.index(str(float(id))))
  vreindex.append(vreid.index(int(id)))

#print (legacindex)
#print (filteredindex)
#print (vreindex)
#-----------------------
output_csv_path = 'New Combined CSV.csv'

#read the fits files as tables so it's easier to process
legactable = Table.read(legacfits, format='fits')
vretable = Table.read(fitsvre, format='fits')

#writing in the csv file all of the new data
with open(output_csv_path, 'w', newline='') as csvfile:
  writer = csv.writer(csvfile)
  
  for m in range (0,len(legacindex)):

      #getting data from both fits files: from [row][column]
      #[...index[m]][n] corresponds to the [row] and [column] I'm looking for
      sigma_gas = legactable[legacindex[m]][17] #from the original lega-c
      vre = vretable [vreindex[m]][22] #from the new kinematics
      #below data is from the csv file
      mergedid = csvdata[filteredindex[m]][0]
      smass = csvdata[filteredindex[m]][1]
      sfr = csvdata[filteredindex[m]][2]
      massclumpy = csvdata[filteredindex[m]][3]
      UVclumpy = csvdata[filteredindex[m]][4]
      z = csvdata[filteredindex[m]][5]
      o3727 = csvdata[filteredindex[m]][6]
      o4959 = csvdata[filteredindex[m]][7]
      o5007 = csvdata[filteredindex[m]][8]
      hbeta = csvdata[filteredindex[m]][9]
      r23 = csvdata[filteredindex[m]][10]

      #writing all of it into the new csv file
      writer.writerow([mergedid, smass, sfr, massclumpy, UVclumpy, z, o3727, o4959, o5007, hbeta, r23, sigma_gas,vre])

