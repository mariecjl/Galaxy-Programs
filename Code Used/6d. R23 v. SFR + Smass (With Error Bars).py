import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#file paths
errors_file = 'errors (copy).csv'
filtered_file = 'filtereddata(noduplicates)+x+diff (2).csv'

R23_error_list=[]

with open(errors_file, 'r') as errors_csv, open(filtered_file, 'r') as filtered_csv:
    errors_reader = csv.reader(errors_csv)
    filtered_reader = csv.reader(filtered_csv)

    #skip headers
    next(errors_reader, None)  
    next(filtered_reader, None)  

    for errors_row, filtered_row in zip(errors_reader, filtered_reader):
        try:

            #obtaining the O3727 value and associated error from the filtered csv file and errors csv file respectively
            O3727_error = float(errors_row[1])
            O3727 = float(filtered_row[6])  

            O4959_error = float(errors_row[2])
            O4959 = float(filtered_row[7])  

            O5007_error = float(errors_row[3])
            O5007 = float(filtered_row[8])  

            Hbeta_error = float(errors_row[4])
            Hbeta = float(filtered_row[9])  

          #Each of terms which, when squared, are summed together under the square root in the error propagation formula
            O3727_term=(1/Hbeta)*O3727_error
            O4959_term=(1/Hbeta)*O4959_error
            O5007_term=(1/Hbeta)*O5007_error
            Hbeta_term = -((O3727+O4959+O5007)/(Hbeta**2))*Hbeta_error

          #The expression under the square root of the error propagation formula
            R23_error_squared = O3727_term**2 + O4959_term**2 + O5007_term**2 + Hbeta_term**2
          #R23 error via the error propagation formula 
            R23_error = R23_error_squared**0.5
            print (R23_error)
          #Appending the calculated R23 value to the R23 error list
            R23_error_list.append(R23_error)

        except (ValueError, IndexError) as e:
            print(f"Error processing row: {e}")

#print (max(R23_error_list))

df = pd.read_csv(errors_file)
df['R23 Errors'] = R23_error_list
df.to_csv(errors_file, index=False)

#--------------------------------------------------------------------
def plot_csv_data(csv_filename):
  #getting data from csv file
  data = pd.read_csv(csv_filename)

  #extract x-values and y-values
  x_values = data.iloc[:, 1]-0.32*data.iloc[:, 2] #logSFR
  y_values = data.iloc[:, 10] 
  color_values = data.iloc[:, 3] #the color values are either from column 4 (massclumpy) or column 5 (UV clumpy)

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
  plt.scatter(blue_x, blue_y, s=10, c='blue', label='Mass Clumpy', marker='s')
  plt.scatter(red_x, red_y, s=10, c='red', label='Mass Nonclumpy')

  #Adding the error bars to the scatterplot using the compiled error list
  plt.errorbar(x_values, y_values, yerr=R23_error_list, linestyle='None', capsize=3, label=None)

  #bigger dots for the averages in each region
  plt.scatter(avg_blue_x, avg_blue_y, s=150, c='blue', marker='s', edgecolors='black', label='Avg Mass-Clumpy')

  plt.scatter(avg_red_x, avg_red_y, s=150, c='red', marker='o', edgecolors='black', label='Avg Mass-Nonclumpy')

  #labels, title, legend
  plt.xlabel('logSmass-0.32logSFR')
  plt.ylabel('R23') #using subscripts and greek letters
  plt.title('R23 v. logSmass-0.32logSFR')
  plt.legend()
  plt.show()

#making sure it's from the right file
csv_filename = 'filtereddata(noduplicates)+x+diff (2).csv'
plot_csv_data(csv_filename)
