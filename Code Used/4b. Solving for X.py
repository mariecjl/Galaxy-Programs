#I TOOK OUT ROWS 8, 20, 77, 125 AND ROW 129 FROM THE ORIGINAL NO DUPLICATE FILE B/C THEY DIDN'T HAVE ANY REAL X ROOTS AND COULDN'T BE USED IN GRAPHING
#The columns in the outputted CSV file has columns: ID, mass, SFR, mass clumpy, UV clumpy, z, O3727, O4959, O5007, HBeta, R23, x obtained from logR23, x obtained from logO32

import csv
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt

#making new & empty lists for the minimum difference between roots, the R23 root and the O32 root that were closest to each other
mindiff=[]
R23x=[]
O32x=[]

#I just used "i" to keep track of which R23s yielded no real roots so I could go back and delete the rows
#After deleting the rows that yielded no real roots, "i" was not displayed/used anywhere else in the program
i=1

csv_file_path = "filtereddata(noduplicates).csv"

#reading the csv file path and telling it that the program that I don't have any headers (no column names displayed)
df = pd.read_csv(csv_file_path, header=None)

with open(csv_file_path, 'r') as file:
    reader = csv.reader(file)

    for row in reader:
        #R23 values are in the 11th column
        R23 = float(row[10])

        #taking the log of R23
        log_R23=math.log10(R23)

        #the coefficients correspond to the equation -0.2524x^4-0.6154x^3-0.9401x^2-0.7149x+0.7462-log(R23)=0
        #which is the equivalent of equation 3) -0.2524x^4-0.6154x^3-0.9401x^2-0.7149x+0.7462 = log(R23)
        coefficients = [-0.2524, -0.6154, -0.9401, -0.7149, 0.7462-log_R23]

        #solving for the roots
        roots_R23 = np.roots(coefficients)
      
        #only outputting real roots
        real_roots_R23 = roots_R23[np.isreal(roots_R23)].real

        #again, "i" was just used to keep track of which of R23 value did not yield any real roots
        i+=1
#-----------------------------
        #obtaining values for O4959, O5007 and O3727
        O4959=float(row[7])
        O5007=float(row[8])
        O3727=float(row[6])

        #calculating the O32 value
        O32 = (O4959+O5007)/O3727

        #taking log of the O32 value
        log_O32=math.log10(O32)
        #print ("log_O32 value is", log_O32)

        #the coefficients correspond to the equation -0.3172x^2-1.3881x-0.2839-logO32=0
        #which is the equivalent of equation 4) -0.3172x^2-1.3881x-0.2839=logO32
        coefficients2 = [-0.3172,-1.3881, -0.2839-log_O32]

        #solving for the roots
        roots_O32 = np.roots(coefficients2)

        #only outputting real roots
        real_roots_O32 = roots_O32[np.isreal(roots_O32)].real

#--------------------------------------------------------------------
      #calculating the difference between any pair of the R23 root and O32 root and then appending it to a list
        differences=[]
        for Rroot in real_roots_R23:
          for Oroot in real_roots_O32:
            differences.append(abs(float(Rroot)-float(Oroot)))
        print (differences)

      #This was just to see which R23 value yielded no real roots (an empty set for real_roots_R23 which would mean there'd be no difference calculatable between the R23 and O32 roots) ("i" was outputted so I could locate the row and go back to delete it because it wouldn't be able to be used in graphing)
        if len(differences)==0:
          print (i)

        else:
   #I really could not think about any better way to do this so I just worked with conditional statements on which R23-obtained x and which O32-obtained X to add based off of which differences was the minimum
  #I just used how in the new list of the four differences (2x2) ([differences]), the ordering would be: [diff(first R23 and first O32), diff(first R23 and second O32), diff(second R23 and first O32), diff(second R23 and second O32)]. So depending on which one was the smallest difference, I added the corresponding root pair.
          
          if min(differences) == differences[0]:
            mindiff.append(differences[0])
            R23x.append(real_roots_R23[0])
            O32x.append(real_roots_O32[0])
          elif min(differences) == differences[1]:
            mindiff.append(differences[1])
            R23x.append(real_roots_R23[0])
            O32x.append(real_roots_O32[1])
          elif min(differences) == differences[2]:
            mindiff.append(differences[2])
            R23x.append(real_roots_R23[1])
            O32x.append(real_roots_O32[0])
          else:
            mindiff.append(differences[3])
            R23x.append(real_roots_R23[1])
            O32x.append(real_roots_O32[1])

#making the R23x and O32x lists into series so they could be easier added into the CSV file as new columns
R23x_series = pd.Series(R23x, name="R23x values")
O32x_series = pd.Series(O32x, name="O32 values")

#inserting the R23x values and O32x values respectively into columns 12 and 13 of the dataframe
df.insert(11, "R23x values", R23x_series, True)
df.insert(12, "O32x values", O32x_series, True)

#updating the csv file
df.to_csv(csv_file_path, index=False, mode='w', header=False)
