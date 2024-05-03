import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

def plot_scatter_from_csv(csv_file_path, dot_size=50):
    df = pd.read_csv(csv_file_path)

    #getting values for x, y, and the color from different columns
  #also columns are 0-indexed
    x_values = df.iloc[:, 2] 
    y_values = df.iloc[:, 10]
    color_values = df.iloc[:, 3]

    # color values to actual colors (red for 0.0 (false) and blue for 1.0 (true))
    colors = ['red' if color == 0.0 else 'blue' for color in color_values]

    # scatterplot
    scatter = plt.scatter(x_values, y_values, c=colors, s=dot_size, label='Dots')

    # axis label and title
  
    plt.xlabel('SFR')
    plt.ylabel('R23')
    plt.title('SFR v. R23 v. Clumpiness')

    #custom legend bc the original one doesn't work
  
    legend_elements = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=8, label='is_mass_clumpy: False'), 
                       plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=8, label='is_mass_clumpy: True')]

  #location for legend
    plt.legend(handles=legend_elements, loc='lower right')
  
    plt.show()

#plotting :) (and also how big the dots are)
plot_scatter_from_csv('plotdataforuse(withr23).csv', dot_size=3)
