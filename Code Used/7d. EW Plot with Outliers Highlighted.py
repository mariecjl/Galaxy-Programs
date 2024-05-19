import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV file into a DataFrame
df = pd.read_csv('EW.csv')

x_values = np.log(df.iloc[:, 3]/df.iloc[:, 4])  #log of EW5007/EWHbeta (x-axis)
y_values = np.log(df.iloc[:, 1]/df.iloc[:, 4]) #log of EW3727/EWHBeta (y-axis))
color = df.iloc[:, 0] #the color values is dependent on the id (if the ids have been identified as corresponding to outlier points)

# Defining the color based on if the datapoint is a outlier
colors = ['orange' if value in [41325.0,109010.0,129027.0,157147.0,165155.0,239335.0,254580.0] else 'black' for value in color]

# Plot the data with color and marker mapping
plt.scatter(x_values, y_values, c=colors)

# Add labels and title
plt.xlabel('log(EW(O3727)/EW(Hβ)))')
plt.ylabel('log(EW(O5007)/EW(Hβ))')
plt.title('Equivalent Width Ratios of Galaxies')

# Display the plot
plt.show()
