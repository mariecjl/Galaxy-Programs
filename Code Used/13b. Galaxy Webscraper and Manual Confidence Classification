import urllib.request
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import csv

# File paths
radec = 'radec.csv'
filtered_file_path = 'filtereddata(noduplicates)+x+diff.csv'

# Obtain the IDs (column 1) of the filtered csv file as a list
filtered_df = pd.read_csv(filtered_file_path)
filtered_ids = filtered_df.iloc[:, 0].tolist()

# Read the data of the ra+dec file
radec_df = pd.read_csv(radec)

# Obtain the rows in the ra+dec file with overlapping IDs as the IDs of the filtered csv file
filtered_radec = radec_df[radec_df.iloc[:, 0].isin(filtered_ids)]

# List for IDs that did not have cutouts
no_cutout = []
j=0
clumplist=[]

#open the csv file to write in
with open('updatedclumpy.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    for index, row in filtered_radec.iterrows():
        j+=1

        #checking that the galaxy is indeed in the crossmatched galaxies to make sure that there is an RA and Dec listing available to use in "scraping" the image
        csv_row_index = filtered_df[filtered_df.iloc[:, 0] == row.iloc[0]].index.tolist()
        if not csv_row_index:
            continue  # Skip if no matching index found

        #obtaining the color, ra and dec of the specific galaxy
        color = filtered_df.iloc[csv_row_index[0], 4]
        ra = row.iloc[1]
        dec = row.iloc[2]

        # Scrape the image
        image_url = f"https://grizli-cutout.herokuapp.com/thumb?ra={ra}&dec={dec}&size=3&filters=f814w,f115w-clear,f150w-clear,f277w-clear,f444w-clear&rgb_scl=1.5,0.74,1.3&asinh=True&all_filters=True"
        urllib.request.urlretrieve(image_url, "test.png")

        try:
            #reading the image and saving it into the folder (I monitor this image as the code loops (and thus the image updates) to check on the galaxy cutout)
            image = mpimg.imread("test.png")
            plt.imshow(image)
            plt.savefig("test.png")

            #assigning color as "clumpy" or "nonclumpy" as the program reads through the 1s and 0s of the color column
            if color == 0:
                clumpiness = "nonclumpy"
            elif color == 1:
                clumpiness = "clumpy"
            else:
                clumpiness = "HUH. Not in defined range."
            
            print ("")
            #this line allows me to monitor my progress going through all the galaxies, the galaxy ID in question and the current clumpiness classification
            
            print(j,"/170. ID:",row.iloc[0],"Currently classified as", clumpiness)
            #I will then input either 1,2,3,4 or 0 which correspond to different confidence levels
            ans = int(input("1=Correct, 2=Not sure, 3=Likely wrong, 4=Double check, 0=Multiple Galaxies: "))
            
            #converting my input into confidence levels to be written into the csv file
            if ans == 1:
                eval = "High Confidence"
            elif ans == 2:
                eval = "Uncertain"
            elif ans == 3:
                eval = "Very low confidence"
            elif ans == 0:
                eval = "Multiple Galaxies"
            elif ans== 4:
                eval = "Needs checking"
            #I added everything to a list just in case the csv file didn't work
            clumplist.append([row.iloc[0], clumpiness, eval])
            #Writing it in the CSV file
            writer.writerow([row.iloc[0], clumpiness, eval])
            #Making sure the the CSV file updates one line at a time ()
            file.flush()

        #Generating a special output if the galaxy does not have a cutout
        except SyntaxError as e:
            if str(e) == 'not a PNG file':
                print("This ID has no cutout: " + str(row.iloc[0]))
                no_cutout.append(row.iloc[0])
            else:
                raise

print("All done.")
print (clumplist)
