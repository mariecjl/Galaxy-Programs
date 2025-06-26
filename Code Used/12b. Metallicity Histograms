#parameter values as generated in the fitted metallicity curve
Z=9.02106615051833
m=9.861653016942883
r=17.78139895012386
#I just wrote gamma as "r" for convenience

#creating a list for the difference between the real metallicity and the generated metallicity value
x_diff=[]

#importing libraries + packages
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#corrected metallicity file
corrected = 'newfiltered (with R23 & x error) (wo outliers).csv'

# Read the CSV files into dataframes
df_corrected = pd.read_csv(corrected)

for i in range (0, len(df_corrected)):
  #obtaining every metallicity value
  exp_x=df_corrected.iloc[i,11]+8.69
  #obtaining the stellar mass
  smass=df_corrected.iloc[i,1]
  #the metallicity value as calculated by the curve
  theor_x=Z + np.log10(1 - np.exp(-(smass/m)**r))
  #the difference in metallicity value between the curve and the real value
  metallicity_diff=exp_x-theor_x
  #adding the difference to the list
  x_diff.append(float(metallicity_diff))

#when I initially ran the code, I added the metallicity difference values into a new csv file so it to be better accessed in creating the histogram
#df_corrected['x_diff (fitted)'] = x_diff
#df_corrected.to_csv('newfiltered (with x_diff (fitted)).csv', index=False)

#separating all metallicity difference values into either red or blue based off of clumpiness
x_diff_r=[]
x_diff_b=[]

#the 5th column of the CSV file corresponds to UVClumpiness, while the 4th column of the file corresponds to MassClumpiness
color=4

#reading data from the new csv file containing the metallicity difference values
diff = 'newfiltered (with x_diff (fitted)).csv'
df_diff = pd.read_csv(diff)

#the loop will run for each galaxy
for j in range (0, len(df_corrected)):
  #the fololowing line is used to separate the mass range of datapopints contained
  if df_corrected.iloc[j,1] <10.5:
    #if it's nonclumpy, it will be added to the collection of red datapoints
    if (df_diff.iloc[j,color] == 0):
      x_diff_r.append(df_diff.iloc[j,14])
    #if it's clumpy, it will be added to the collection of blue datapoints
    else:
      x_diff_b.append(df_diff.iloc[j,14])

#creating the histograms
plt.hist(x_diff_b, bins=7, color='blue', alpha=0.5, label='UVClumpy')  # Blue histogram (clumpy)
plt.hist(x_diff_r, bins=7, color='red', alpha=0.5, label='UVNonclumpy')   # Red histogram (nonclumpy)

plt.title('Histogram of Metallicity Difference')
plt.xlabel('Metallicity (x) difference (Actual - Fitted Theoretical)')
plt.ylabel('Frequency')
plt.legend()

plt.show() 
