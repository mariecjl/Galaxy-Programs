import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#file paths
errors_file = 'errors (with R23 & x error).csv'
filtered_file = 'filtereddata(noduplicates)+x+diff.csv'

#creating a list for the x errors whose contents will form the error bars
x_error_list=[]

with open(errors_file, 'r') as errors_csv, open(filtered_file, 'r') as filtered_csv:
  #read both the error and the filtered file
  errors_reader = csv.reader(errors_csv)
  filtered_reader = csv.reader(filtered_csv)

  #skip headers
  next(errors_reader, None)  
  next(filtered_reader, None)  

  for errors_row, filtered_row in zip(errors_reader, filtered_reader):
    #read both the R23 error value (from the errors file) and the x value (from the filtered file)  
    R23_error=float(errors_row[5])
    x=float(filtered_row[11])

    #log(R23)=P(x) --> R23=10^(P(x)) where P(x) is the quartic polynomial containing x
    #R23_error=√((differentiating 10^P(x) with respect to x)*x_error)^2
    #where differentiating 10^P(x) with respect to x is ln(10)*10^(P(x))*(derivative of P(x)
    #Confirmed by online calculator: https://www.symbolab.com/solver/step-by-step/%5Cfrac%7Bd%7D%7Bdx%7D%5Cleft(10%5E%7B0.7462-0.7149x-0.9401x%5E2-0.6154x%5E3-0.2524x%5E4%7D%5Cright)?or=input

    #poly is P(x)
    poly=0.7462-0.7149*x-0.9401*(x**2)-0.6154*(x**3)-0.2524*(x**4)

    #dpoly is derivative of P(x)
    dpoly=-0.7149-2*0.9401*(x)-3*0.6154*(x**2)-4*0.2524*(x**3)

    print ('')
    
    #differentiating 10^P(x) with respect to x
    differential=np.log(10)*(10**(poly))*dpoly

    #calculating the error bar on the x value (the square then square root corresponds to the absolute value taken)
    dx=abs(R23_error/differential)
    print (dx)
    #appending the error bar to the list
    x_error_list.append(dx)

#----------------------------------------------------
#the first time I ran the code, I made the program add the x_error values to the csv file for easier access

#df = pd.read_csv(filtered_file)
#df['x_errors'] = x_error_list
#df.to_csv(filtered_file, index=False)

#--------------------------------------------------

def plot_csv_data(csv_filename):
  #getting data from csv file
  data = pd.read_csv(csv_filename)

  #extract x-values and y-values
  x_values = data.iloc[:, 1]-0.32*data.iloc[:, 2] #logSmass-0.32logSFR
  y_values = data.iloc[:, 11]+8.69 #R23-calculated value of x + 8.69
  color_values = data.iloc[:, 3] #the color values are either from column 4 (massclumpy) or column 5 (UV clumpy)
  error_values = data.iloc[:, 13] #error bar values from the new csv column

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

  #create the regular scatterplot using the datapoints from the csv files
  plt.scatter(blue_x, blue_y, c='blue', label='UV Clumpy', marker='s')
  plt.scatter(red_x, red_y, c='red', label='UV Nonclumpy')

  #bigger dots for the averages in each region
  plt.scatter(avg_blue_x, avg_blue_y, s=150, c='blue', marker='s', edgecolors='black', label='Avg UV-Clumpy')
  plt.scatter(avg_red_x, avg_red_y, s=150, c='red', marker='o', edgecolors='black', label='Avg UV-Nonclumpy')

  #adding the error bars from the error values column
  plt.errorbar(x_values, y_values, yerr=error_values, fmt='none', capsize=5,alpha=0.8)

  #labels, title, legend
  plt.xlabel('log(Mass)-0.32log(SFR)')
  plt.ylabel('x = 12+log(O/H)')
  plt.title('Metallicity(x) v. SFR&Mass')
  plt.legend()

  plt.show()

#making sure it's from the right file
csv_filename = 'filtereddata(noduplicates)+x+diff.csv'
plot_csv_data(csv_filename)
