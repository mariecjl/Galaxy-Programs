import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# reading the kinematics file
with open('Rotational Velocities 2.csv', 'r') as kinematics_csv:
    kinematics_reader = csv.reader(kinematics_csv)
    kinematics_data = list(kinematics_reader)

# reading the filtered file
with open('filtereddata(noduplicates)+x+diff.csv', 'r') as filtered_csv:
    filtered_reader = csv.reader(filtered_csv)
    filtered_data = list(filtered_reader)

# extract IDs from both files and convert to floats (so the data type would be the same)
kinematics_ids = [float(row[1]) for row in kinematics_data]
filtered_ids = [float(row[0]) for row in filtered_data]

#creating a list for the matching ids
matching_ids = []

#appending all matching ids into the previously created list
for id in kinematics_ids:
  if id in filtered_ids:
    matching_ids.append(id)

#print ('')
#print (matching_ids)

#creating lists for the rows in the kinematics file and the filtered file which contain the same IDs
kinematics_matching_rows = []
filtered_matching_rows=[]

#adding respective row numbers to the lists
for same_id in matching_ids:
  kinematics_matching_rows.append(kinematics_ids.index(same_id))
  filtered_matching_rows.append(filtered_ids.index(same_id))
  
#print (filtered_matching_rows)
#print (kinematics_matching_rows)

#creating lists for the sfr value, the massClumpy value and UVClumpy value
filtered_sfr=[]
mass_filtered_color=[]
UV_filtered_color=[]

#appending all desired values
for row in filtered_matching_rows:
  sfr=filtered_data[row][2]
  filtered_sfr.append(float(sfr))

  mass_color=filtered_data[row][3]
  mass_filtered_color.append(float(mass_color))

  UV_color=filtered_data[row][4]
  UV_filtered_color.append(float(UV_color))
  
#creating lists for the sigma0, vrot_Re and vrot_Re2 values
kinematics_sigma0=[]
kinematics_vrot_Re=[]
kinematics_vrot_Re2=[]

#appending all desired values
for row in kinematics_matching_rows:
  sigma0=kinematics_data[row][9]
  kinematics_sigma0.append(float(sigma0))

  vrot_Re=kinematics_data[row][3]
  kinematics_vrot_Re.append(float(vrot_Re))

  vrot_Re2=kinematics_data[row][6]
  kinematics_vrot_Re2.append(float(vrot_Re2))

#-----------------------------------------------------------------------
#creating a new kinematics csv file
output_file='newkinematics.csv'

with open(output_file, 'w', newline='') as csv_file:
  csv_writer = csv.writer(csv_file)

  # writing header
  csv_writer.writerow(['matching_IDs', 'filtered_sfr', 'mass_filtered_color', 'UV_filtered_color', 'kinematics_sigma0', 'kinematics_vrot_Re','kinematics_vrot_Re2'])

  # writing all data
  for data in zip(matching_ids, filtered_sfr, mass_filtered_color, UV_filtered_color, kinematics_sigma0, kinematics_vrot_Re,kinematics_vrot_Re2):
      csv_writer.writerow(data)

#---------------------------------------------------------------------
data = pd.read_csv('newkinematics.csv')

#extract x-values and y-values
x_values = data.iloc[:, 1] #logSFR
y_values = data.iloc[:, 4]/data.iloc[:, 5] #sigma_gas/VRe
color_values = data.iloc[:, 2] #the color values are either from column 3 (massclumpy) or column 4 (UV clumpy)

#separate the x and y values based off of the color values (if the dot is red or blue)
red_x = x_values[color_values == 0.0]
red_y = y_values[color_values == 0.0]
blue_x = x_values[color_values == 1.0]
blue_y = y_values[color_values == 1.0]

#separating the x axis into 5 regions (bins)
#I added the 0.000001 at the end of the the rightmost bound so the rightmost point could be included in the last bin
bins = np.linspace(x_values.min(), x_values.max()+0.000001, num=6)

#creating lists for the averages of the blue dots and red dots
avg_red_x = []
avg_red_y = []
avg_blue_x = []
avg_blue_y = []

#for each of the bins (the 5 regions)
for i in range(len(bins) - 1):

    #red_mask and blue_mask finds the values of the red_x and blue_x which are in the current bin (bigger than the current bin's minimum and smaller than the next bin's minimum))
    red_mask = (red_x >= bins[i]) & (red_x < bins[i + 1])
    blue_mask = (blue_x >= bins[i]) & (blue_x < bins[i + 1])

    #adds the average of the red_mask to its respective x, y lists
    avg_red_x.append(np.mean(red_x[red_mask]))
    avg_red_y.append(np.mean(red_y[red_mask]))

    #adds the average of the blue_mask to its respective x, y lists
    avg_blue_x.append(np.mean(blue_x[blue_mask]))
    avg_blue_y.append(np.mean(blue_y[blue_mask]))

#create the regular scatterplot using the csv file datapoints
plt.scatter(blue_x, blue_y, c='blue', label='Mass Clumpy', marker='s')
plt.scatter(red_x, red_y, c='red', label='Mass Nonclumpy')

#bigger dots for the averages in each region
plt.scatter(avg_blue_x, avg_blue_y, s=150, c='blue', marker='s', edgecolors='black', label='Avg Mass-Clumpy')
plt.scatter(avg_red_x, avg_red_y, s=150, c='red', marker='o', edgecolors='black', label='Avg Mass-Nonclumpy')

#labels, title, legend
plt.xlabel('logSFR')
plt.ylabel(r'$\sigma_{gas}/V_{rotational(Re)}$') #using subscripts and greek letters
plt.title(r'$\sigma_{gas}/V_{rotational(Re)}\ v.  logSFR$')
plt.legend()
plt.show()
