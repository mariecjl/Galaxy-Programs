import csv

#importing the files (DRP and DAP)
file1 = "/Users/marie/Desktop/MaNGA Scrape/drpdata.csv"
file2 = "/Users/marie/Desktop/MaNGA Scrape/dapdata.csv"

#function for searching for values in a csv file
def search_value_in_csv(file, search_value):
    found = False

    #reading the csv file
    with open(file, mode='r', newline='') as f:
        reader = csv.reader(f)
        #reading the csv file
        headers = next(reader) 
        #going through each row in the csv file
        for row in reader:
            #if the row matches the desired plateIFU
            if row[0] == search_value:
                #for each header in that row
                for header, value in zip(headers[1:], row[1:]):
                    try:
                        #convert the value to a float in the form of scientific notation
                        num = float(value)
                        print(f"{header}: {num:.4e}")
                    except ValueError:
                        #if it's not a number, print the value as is
                        print(f"{header}: {value}")
                found = True
                break
    if not found:
        print(f"\nValue '{search_value}' not found in {file}.")

#continuously prompts for inputs for the Plate and IFU of galaxy targets
while True:
    plateifu = input("Plate & Ifu: ")
    #searches information in both DAP and DRP
    search_value_in_csv(file1, plateifu)
    search_value_in_csv(file2, plateifu)
    print("")
