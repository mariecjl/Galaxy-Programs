import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

#file paths
errors_file = 'errors (with R23 error)(wo outliers).csv'
filtered_file = 'filtereddata(noduplicates)+x+diff(wo outliers).csv'

#initiating x error list
x_error_list=[]

#errors_data = pd.read_csv(errors_file)
filtered_data=pd.read_csv(filtered_file)

#extract x-values and y-values
x_values = filtered_data.iloc[:, 1]-0.32*filtered_data.iloc[:, 2] #logSFR
y_values = filtered_data.iloc[:, 11]+8.69

#extract the data from the x error column to the x_error_list
x_error_list=filtered_data['x_errors'].tolist()

#creating lists for later use
red_ID=[]
blue_ID=[]

red_x=[]
blue_x=[]

red_y=[]
blue_y=[]

red_error=[]
blue_error=[]

for i in range(len(x_error_list)):
  #the color is either determined by the value of the 4th or 5th column (massclumpy or UVclumpy)
  #iterate through each row for the entire CSV file
  color=filtered_data.iloc[i,4]
  #append the necessary data of a specific ID to red lists if the color value is 0.0
  if (color == 0.0):
    red_ID.append(filtered_data.iloc[i,0])
    red_x.append(x_values[i])
    red_y.append(y_values[i])
    red_error.append(filtered_data.iloc[i,13])
  #append the necessary data of a specific ID to blue lists if the color value is 1.0
  else:
    blue_ID.append(filtered_data.iloc[i,0])
    blue_x.append(x_values[i])
    blue_y.append(y_values[i])
    blue_error.append(filtered_data.iloc[i,13])

#--------------------------------------------------
#creating the intervals for the bins
diff=((x_values.max()+0.000000000001)-(x_values.min()))/5

#lists for creating the big dots (for the weighted avgs)
r_avg_x=[]
r_avg_y=[]
r_avg_error=[]

#iterate through each of the 5 intervals 
for j in range (0,5):
  r_x_term=[]
  r_y_term=[]
  r_error_term=[]
  for k in range (0,len(red_x)):
    #if a specific value in red_x can be found within a particular interval
    if ((x_values.min()+j*diff)<=red_x[k]<=(x_values.min()+(j+1)*diff)):
      r_x_term.append((red_x[k])/((red_error[k])**2)) #(x/(sigma)^2)
      r_y_term.append((red_y[k])/((red_error[k])**2)) #(y/(sigma)^2)
      r_error_term.append(1/((red_error[k])**2)) #1/sigma^2

  
  r_avg_x.append((sum(r_x_term))/sum(r_error_term)) #weighted avg for the x value of the big red dot
  r_avg_y.append((sum(r_y_term))/sum(r_error_term)) #weighted avg for the y value of the big red dot
  r_avg_error.append(math.sqrt(1/(sum(r_error_term)))) #weighted error bar value of the big red dot

#-------------------------------------------------
#the exact same as the above, except the segment below is for creating the big blue dots
b_avg_x=[]
b_avg_y=[]
b_avg_error=[]

for j in range (0,5):
  b_x_term=[] #(x/(sigma)**2)
  b_y_term=[]
  b_error_term=[]
  for k in range (0,len(blue_x)):
    if ((x_values.min()+j*diff)<=blue_x[k]<=(x_values.min()+(j+1)*diff)):

      b_x_term.append((blue_x[k])/((blue_error[k])**2)) #(x/(sigma)^2)
      b_y_term.append((blue_y[k])/((blue_error[k])**2)) #(y/(sigma)^2)
      b_error_term.append(1/((blue_error[k])**2)) #1/sigma^2

  #if there are any datapoints in the interval
  if (len(b_error_term)!=0):
    b_avg_x.append((sum(b_x_term))/sum(b_error_term))
    b_avg_y.append((sum(b_y_term))/sum(b_error_term))
    b_avg_error.append(math.sqrt(1/(sum(b_error_term))))
    
#----------------------------------------------------------------------------------------
print (x_error_list)
#creating the scatterplot (including the datapoints from each row and the weighted average datapoints)

#regular datapoints (small dots) 
plt.scatter(blue_x, blue_y, s=10, c='blue', label='UV Clumpy', marker='s')
plt.scatter(red_x, red_y, s=10, c='red', label='UV Nonclumpy')
plt.errorbar(x_values, y_values, yerr=x_error_list, linestyle='None', capsize=3, label=None)

#plotting the weighted averages
plt.errorbar(r_avg_x, r_avg_y, alpha=0.4, yerr=r_avg_error, fmt='o', markersize=8, color='red', ecolor='black', capsize=5, label='Weighted Avg UV-Nonclumpy')
plt.errorbar(b_avg_x, b_avg_y, alpha=0.4, yerr=b_avg_error, fmt='s', markersize=8, color='blue', ecolor='black', capsize=5, label='Weighted Avg UV-Clumpy')

#labelling the axes, title, and legend
plt.xlabel('logSmass-0.32logSFR')
plt.ylabel('x = 12+log(O/H)') 
plt.title('x (metallicity) v. logSmass-0.32logSFR')
plt.legend()

plt.show()

