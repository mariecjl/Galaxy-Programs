import pandas as pd

input_file = "combined_radec.csv"
output_file = "radec.csv"

#read the file into a dataframe
df = pd.read_csv(input_file)

#use method provided by pandas library to remove duplicated rows
no_duplicates = df.drop_duplicates()

#write out the new dataset without duplicates into the output file
#index=False to avoid writing the index column (which pandas apparently adds by default)
no_duplicates.to_csv(output_file, index=False)
