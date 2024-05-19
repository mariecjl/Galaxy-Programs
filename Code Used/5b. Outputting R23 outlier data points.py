import csv

file_path = 'filtereddata(noduplicates)+x+diff.csv'
print ("The following is the ID, R23-calculatedx and R23-calculated x for the outlier datapoints")
#The R23-calculated x is 12+log(O/H)-8.69

with open(file_path, 'r') as csv_file:
    reader = csv.reader(csv_file)

    for row in reader:
      #Access the R23-calculated x in the 12th column in each row
      R23x = float(row[11])
      #The vast majority of datapoints lie above -0.4ish
      if R23x < -0.5:
        #The O32-calculated x is stored in the 13th column of each row
        O32x=float(row[12])
        #The ID is the 1st column of each row
        ID=float(row[0])
        print ("ID",ID," R23x", R23x, " O32x",O32x)
      
