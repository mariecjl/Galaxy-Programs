import csv
import statistics

#creating a function to process data given the CSV's file path and column
def process_csv(file_path, col):
    values = []
    
    #reading the csv file
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        
        #iterating through each row in the csv file
        for row in reader:
            try:
                #extracting the desired column's value, and adding it to the values list
                value = float(row[col])
                #ignore negative values bc those were outliers/unstable signals
                if value > 0:
                    values.append(value)
            #if there was missing data, that row was not taken into consideration
            except (ValueError, IndexError):
                continue
    
    if values:
        #the median is calculated using the library "statistics"
        median = statistics.median(values)
        #calculating the max
        max_val = max(values)
        #calculating the min
        min_val = min(values)
        
        #displaying the median, max and min
        print(f"Median: {median:.4e}")
        print(f"Max: {max_val:.4e}")
        print(f"Min: {min_val:.4e}")
    else:
        print("No valid positive data found")

#defining the two file paths
drp = '/Users/marie/Desktop/MaNGA Scrape/drpdata.csv'
dap='/Users/marie/Desktop/MaNGA Scrape/dapdata.csv'

#I used the function to output the median, min and max of a specific column by specifying file and column
process_csv(dap,2)
