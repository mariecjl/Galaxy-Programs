import pandas as pd
import matplotlib.pyplot as plt

#accessing different file paths
uvj_file_path = 'uvista_uvj.csv'
filtered_file_path = 'filtereddata(noduplicates)+x+diff.csv'

#obtain the IDs (column 1) of the filtered csv file
filtered_df = pd.read_csv(filtered_file_path)
filtered_ids = filtered_df.iloc[:, 0].tolist()

#Read the data of the UVJ csv file
uvj_df = pd.read_csv(uvj_file_path)

#obtain the rows in the UVJ file with overlapping IDs as the IDs of the filtered csv file
filtered_uvj_df = uvj_df[uvj_df.iloc[:, 0].isin(filtered_ids)]
filtered_color_df = filtered_df[filtered_df.iloc[:, 0].isin(filtered_ids)]

#defining the colors of the scatterplot dots based off of Mass Clumpy (4th column)/UV Clumpy (5th row)
colors = ['blue' if val == 1 else 'red' for val in filtered_color_df.iloc[:, 3]]

#Adding the legend to the graph
blue_patch = plt.Line2D([0], [0], marker='o', color='w', label='Mass Clumpy', markerfacecolor='blue', markersize=7)
red_patch = plt.Line2D([0], [0], marker='o', color='w', label='Mass Nonclumpy', markerfacecolor='red', markersize=7)
plt.legend(handles=[blue_patch, red_patch])

#obtaining the x and y values as the third column values (V-J) and the second column values (U-V) respectively
x_filtered = filtered_uvj_df.iloc[:, 2]
y_filtered = filtered_uvj_df.iloc[:, 1]

#creating the scatterplot
plt.scatter(x_filtered, y_filtered, c=colors, marker='o', s=5, label='Filtered Scatter Plot')
plt.xlabel('V-J')
plt.ylabel('U-V')
plt.title('UVJ Values Scatterplot')
plt.show()
