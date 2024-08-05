import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#files which will be used
corrected = 'newfiltered (with R23 & x error) (wo outliers).csv'
uncorrected = 'filtereddata(noduplicates)+x+diff(wo outliers).csv'

# reading the csv files
df_corrected = pd.read_csv(corrected)
df_uncorrected = pd.read_csv(uncorrected)

#the x axis is the uncorrected metallicity while the y axis is the metallicity with dust extinction taken into account
x=df_uncorrected.iloc[:,11]
y=df_corrected.iloc[:,11]

#Blue if the galaxy is clumpy and red if it's nonclumpy
color=df_corrected.iloc[:,3]
colors=['red' if val == 0.0 else 'blue' for val in color]

#creating a scatterplot with the two metallicities
plt.scatter(x+8.69,y+8.69,c=colors)

#creating a purple line with the equation y=x to be displayed on the graph
line_range = np.linspace(8.6, 9.3, 100)

#this is just to add the labels for the plot indicating that clumpy galaxies are blue and nonclumpy galaxies are red
plt.scatter([], [], c='blue', label='MassClumpy')
plt.scatter([], [], c='red', label='Mass-Nonclumpy')
plt.plot(line_range, line_range, color='purple', linestyle='--', label='y = x')

#labeling the axis + title
plt.xlabel('Uncorrected metallicity (x = 12+log(O/H))')
plt.ylabel('Corrected metallicity (x = 12+log(O/H))')
plt.title('Dust-extinction-corrected v. Uncorrected Metallicity')

plt.legend()
plt.show()
