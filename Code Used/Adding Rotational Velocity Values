from astropy.table import Table
from astropy.io import fits

vrefitsid=[]
vrevalues=[]

fitspath = 'vre.fits'

#printing out all the column names
with fits.open(fitspath) as hdul:
  column_names = hdul[1].columns.names
  print ("")
  print ("Below are the column names")
  print(column_names)

fitstable = Table.read(fitspath)

for i in range (0,len(fitstable)):
    #As seen in the output columns, the first column (0 under 0-index corresponds to "LEGA-C" so this line is for retrieving all the "LEGA-C" values in the file with VRe data)
    vrefitsid.append(fitstable[i][1])

   #Adding the VRe data which, 0-indexed, is in column 20
    vrevalues.append(fitstable[i][20])

  #The min and max of the "LEGA-C" column in the new catalogue, as outputted, are 5 and 4061 respectively :(

print ("")
print (vrefitsid)
#print (vrefitsid)
#print ("Min of values for 'LEGA-C' column: ",min(vrefitsid))
#print ("Max of values for 'LEGA-C' column: ", max(vrefitsid))

#there are two "Warnings" in the outputs: one about the brackets used in the column names and the other how [MSun] is not recognized as a unit (probably also because of the brackets), but I don't really think they're supposed to affect the column index.
