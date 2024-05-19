#importing all packages and libraries
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

#initiating the lists of values obtained from the csv files (NEIII csv and filtered csv)
ID_values=[]
O3727_values=[]
NE3869_values=[]
O4959_values=[]
O5007_values=[]
HBeta_values=[]

#lists for the x and y values to be plotted
x=[]
y=[]

#lists for the IDs of the outliers and the IDs that have a negative NEIII value
outlier_id=[]
negativeNE=[]

NE_path='NEIII.csv'

#appending the values from the NEIII csv file to lists
with open(NE_path, 'r') as file:
  for row in csv.reader(file):
    ID_values.append(float(row[0]))
    O3727_values.append(float(row[1]))
    NE3869_values.append(float(row[2]))
    O4959_values.append(float(row[3]))
    O5007_values.append(float(row[4]))
    HBeta_values.append(float(row[5]))

#iterate through each item in the list:
for i in range (0, 169):

#calculations are only done for NEIII values which are positive because otherwise a math error is returned (when taking the log of a negative number)
  if (NE3869_values[i] > 0):
    #expressing x and y values with the log of flux ratios
    x_value=math.log10(NE3869_values[i]/O3727_values[i])
    y_value=math.log10((O4959_values[i]+O5007_values[i])/HBeta_values[i])

    #appending each x and y value to their respective lists
    x.append(x_value) 
    y.append(y_value)

    #appending the IDs of datapoints that lie above and to the right of the equation to the outlier list
    if (y_value>(0.35/(2.8*x_value-0.8))+0.64):
      outlier_id.append(ID_values[i])

  #appending the IDs of galaxies which have a negative NEIII value to the negativeNE list
  else:
    negativeNE.append(ID_values[i])

#scatterplot the x and y lists
plt.scatter(x, y, marker='o')

#plotting the equation of the line
x_values = np.linspace(min(x), max(x), 100)
plt.plot(x_values, 0.35/(2.8*x_values-0.8)+0.64, linestyle='--', color='red')

#adding labels and titles
plt.xlabel('log ([NEIII]/[OII])')
plt.ylabel('log ([OIII]/Hβ)')
plt.title('log ([OIII]/Hβ) v. log ([NEIII]/[OII])')
plt.show()
