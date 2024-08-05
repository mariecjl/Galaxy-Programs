import numpy as np
import matplotlib.pyplot as plt
import astropy.units as u
import pandas as pd
from dust_extinction.parameter_averages import F99
import csv

fig, ax = plt.subplots()

# Defining the R(v) value
cur_Rv = 3.1

# Creating the plot for R(v)=3.1
ext_model = F99(Rv=cur_Rv)

# Generating x-values for the plot
x = np.arange(ext_model.x_range[0], ext_model.x_range[1], 0.1) / u.micron

# calculating y values for the plot
y = ext_model(x)

# creating the actual plot:
ax.plot(x, y, label='R(V) = ' + str(cur_Rv))
ax.set_xlabel(r'$x$ [$\mu m^{-1}$]')
ax.set_ylabel(r'$A(x)/A(V)$')
ax.legend(loc='best')

# getting y values for HBeta
HBeta_x_value = (1/0.4861) * u.micron**-1  # x-value in the correct unit
HBeta_y_value = ext_model(HBeta_x_value)

#y values for O3727
O3727_x_value = (1/0.3727) * u.micron**-1  # x-value in the correct unit
O3727_y_value = ext_model(O3727_x_value)

#y values for O4959
O4959_x_value = (1/0.4959) * u.micron**-1  # x-value in the correct unit
O4959_y_value = ext_model(O4959_x_value)

#y values for O5007
O5007_x_value = (1/0.5007) * u.micron**-1  # x-value in the correct unit
O5007_y_value = ext_model(O5007_x_value)

#accessing the extinction file
extinction = 'UVISTA_final_BC03_v4.1.fout'

# Load the data using NumPy, assuming whitespace delimiter
data = np.loadtxt(extinction)

# Extract the first column
ID = data[:, 0]


#-----------------------------------------------------------------------
filtered_csv = 'filtereddata(noduplicates)+x+diff.csv'

# loading the IDs of the csv file
filtered_df = pd.read_csv(filtered_csv)
filtered_ids = filtered_df.iloc[:, 0].tolist()

extinction_data = np.loadtxt(extinction, dtype=float)

#identify matching rows where the IDs in the CSV corresponds to the IDs in the fout file
matching_rows = extinction_data[np.isin(extinction_data[:, 0], filtered_ids)]

#av is in the 6th column of the fout file
Av_array = matching_rows[:, 5]

#converting it to a list
Av = Av_array.tolist()


#adj stands for "adjusted for dust extinction
#--------------------------------------------------
adj_O3727_list=[]
adj_O4959_list=[]
adj_O5007_list=[]
adj_HBeta_list=[]
#------------------------------------------------------------------
r_filtered_csv = open(filtered_csv, mode='r')
csv_reader = csv.reader(r_filtered_csv)
filtered_all = list(csv_reader)

count=0
i=0

#iterating through all values in O3727, O4959, O5007 and HBeta to add the corrected flux into their respective lists
for j in Av:
        #just adding the above line so the header doesn't get counted
    #Ax=y value according to model * Av value
    Ax_O3727=j*O3727_y_value
    Ax_O4959=j*O4959_y_value
    Ax_O5007=j*O5007_y_value
    Ax_HBeta=j*HBeta_y_value

    #we're adding one to take into account that the csv file has a header but the fout file array doesn't so row in the csv file is shifted down by 1
    adj_O3727_list.append((float(filtered_all[i+1][6]))/(10**(-0.4*Ax_O3727)))
    adj_O4959_list.append((float(filtered_all[i+1][7]))/(10**(-0.4*Ax_O4959)))
    adj_O5007_list.append((float(filtered_all[i+1][8]))/(10**(-0.4*Ax_O5007)))
    adj_HBeta_list.append((float(filtered_all[i+1][9]))/(10**(-0.4*Ax_HBeta)))
    i+=1 
    #cycles through every matching row where each new item in the Av list corresponds to a new row in the filtered csv (indexing doesn't work because there are repeated A(v) values)

#new filtered file
newfiltered = 'newfiltered.csv'

# reading the new filtered file with pandas
newfiltered_df = pd.read_csv(newfiltered)

#adding the new values for O3727
newfiltered_df.iloc[:, 6] = adj_O3727_list
newfiltered_df.to_csv('newfiltered.csv', index=False)

#adding the new values for O4959
newfiltered_df.iloc[:, 7] = adj_O4959_list
newfiltered_df.to_csv('newfiltered.csv', index=False)

#adding the new values for O5007
newfiltered_df.iloc[:, 8] = adj_O5007_list
newfiltered_df.to_csv('newfiltered.csv', index=False)

#adding the new values for HBeta
newfiltered_df.iloc[:, 9] = adj_HBeta_list
newfiltered_df.to_csv('newfiltered.csv', index=False)

#adding the new values for R23
newfiltered_df.iloc[:, 10] = (newfiltered_df.iloc[:, 6] + newfiltered_df.iloc[:, 7] + newfiltered_df.iloc[:, 8]) / (newfiltered_df.iloc[:, 9])
newfiltered_df.to_csv('newfiltered.csv', index=False)
