#The columns in the inputted CSV file has columns: ID, mass, SFR, mass clumpy, UV clumpy, z, O3727, O4959, O5007, HBeta, R23, x obtained from logR23, x obtained from logO32


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_csv_data(csv_filename):
  #getting data from csv file
  data = pd.read_csv(csv_filename)

  #extract x-values and y-values
  x_values = data.iloc[:, 1]-0.32*data.iloc[:, 2] #logSmass-0.32logSFR
  y_values = data.iloc[:, 11]+8.69 #R23-calculated roots
  color_values = data.iloc[:, 3] #the color values are either from column 4 (massclumpy) or column 5 (UV clumpy)

  #separate the x and y values based off of the color values (if the dot is red or blue)
  red_x = x_values[color_values == 0.0]
  red_y = y_values[color_values == 0.0]
  blue_x = x_values[color_values == 1.0]
  blue_y = y_values[color_values == 1.0]

  #separating the x axis into 5 regions (bins)
  #I added the 0.000001 at the end of the the rightmost bound so the rightmost point could be included in the last bin
  bins = np.linspace(x_values.min(), x_values.max()+0.0000001, num=6)
  #print (bins)

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

  #create the regular scatterplot using the 62 datapoints from the csv files
  plt.scatter(blue_x, blue_y, c='blue', label='Mass Clumpy', marker='s')
  plt.scatter(red_x, red_y, c='red', label='Mass Nonclumpy')

  #bigger dots for the averages in each region
  plt.scatter(avg_blue_x, avg_blue_y, s=150, c='blue', marker='s', edgecolors='black', label='Avg Mass-Clumpy')
  plt.scatter(avg_red_x, avg_red_y, s=150, c='red', marker='o', edgecolors='black', label='Avg Mass-Nonclumpy')

  #labels, title, legend
  plt.xlabel('log(Mass)-0.32log(SFR)')
  plt.ylabel('x = 12+log(O/H)')
  plt.title('Metallicity(x) v. SFR&Mass')
  plt.legend()

  plt.show()

#making sure it's from the right file
csv_filename = 'filtereddata(noduplicates)+x+diff.csv'
plot_csv_data(csv_filename)
