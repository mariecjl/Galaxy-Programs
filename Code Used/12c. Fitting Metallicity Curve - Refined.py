import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.optimize import curve_fit


#file paths
errors_file = 'newerrors (copy) (wo outliers).csv'
filtered_file = 'newfiltered (with R23 & x error) (wo outliers).csv'

#initiating x error list
x_error_list=[]

#errors_data = pd.read_csv(errors_file)
filtered_data=pd.read_csv(filtered_file)

#extract x-values and y-values
x_values = filtered_data.iloc[:, 1] #logSmass
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
  color=filtered_data.iloc[i,3]
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
for j in range (0,10):
  r_x_term=[]
  r_y_term=[]
  r_error_term=[]
  for k in range (0,len(red_x)):
    #if a specific value in red_x can be found within a particular interval
    if ((x_values.min()+j*diff*0.5)<=red_x[k]<=(x_values.min()+j*diff*0.5+diff)):
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

for j in range (0,10):
  b_x_term=[] #(x/(sigma)**2)
  b_y_term=[]
  b_error_term=[]
  for k in range (0,len(blue_x)):
    if ((x_values.min()+j*diff*0.5)<=blue_x[k]<=(x_values.min()+j*diff*0.5+diff)):

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

#converting all of the lists used into arrays for better performing operations/calculations
#-------------
r_x_array=np.array(red_x)
r_y_array=np.array(red_y)

b_x_array=np.array(blue_x)
b_y_array=np.array(blue_y)

#defining the custom equation and the variables Z, m, and r
def custom_equation(x, Z, m, r):
  return Z + np.log10(1 - np.exp(-(x/m)**r))

# fiting the model to the data
#initial_guesses: I picked values on the same order of magnitude as the paper's described Z, m and r values of [8.977, 9.961, 0.661] respectively
initial_guess = [10,10,1]

#fitting the curve for the all the big dots (I concatenated the blue and red dots together)
params, covariance = curve_fit(custom_equation, np.concatenate((r_x_array, b_x_array)), np.concatenate((r_y_array, b_y_array)), p0=initial_guess)


#extracting the values of Z, m, and r from the fitted curve
Z_fit, m_fit, r_fit = params

#plotting the curve
#I generated some x-values along the x-axis
x_fit_dense = np.linspace(x_values.min(), x_values.max(), 1000)
#Generating y values based off of the determined parameters/values for Z, m and r
y_fit_dense = custom_equation(x_fit_dense, *params)

#creating the plot
#regular datapoints (scatterplot with small dots) 
plt.scatter(blue_x, blue_y, s=10, c='blue', label='Mass Clumpy', marker='s')
plt.scatter(red_x, red_y, s=10, c='red', label='Mass Nonclumpy')

#adding the metallicity error bars (y-axis)
plt.errorbar(x_values, y_values, yerr=x_error_list, linestyle='None', capsize=3, label=None)

#displaying the fitted curve for both red and blue dots

plt.plot(x_fit_dense, y_fit_dense, color='purple', label='Fitted metallicity curve')


#plotting the weighted averages
plt.errorbar(b_avg_x, b_avg_y, alpha=0.4, yerr=b_avg_error, fmt='s', markersize=8, color='blue', ecolor='black', capsize=5, label='Weighted Avg Mass-Clumpy')
plt.errorbar(r_avg_x, r_avg_y, alpha=0.4, yerr=r_avg_error, fmt='o', markersize=8, color='red', ecolor='black', capsize=5, label='Weighted Avg Mass-Nonclumpy')

#labelling the axes, title, and legend
plt.xlabel('logSmass')
plt.ylabel('x = 12+log(O/H)') 
plt.title('x (metallicity) v. logSmass')
plt.legend()

#printing the fitted parameters
print(f'Fitted parameters: Z={Z_fit}, m={m_fit}, r={r_fit}')

plt.show()
