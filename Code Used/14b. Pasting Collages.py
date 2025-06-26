#importing libraries
import os
from PIL import Image

#creating the larger, rectangular collage
def createcollage(imagepaths, collagenumber, outputfolder):
    #opening all desired image paths and putting them in a list
    try:
        images = [Image.open(imagepath) for imagepath in imagepaths]
    #error message in case the image was not successfully opened
    except Exception as e:
        print(f"error opening these images: {e}")
        return
    
    #calculating the sum of the widths and the maximum of the heights (since we're pasting horizontally)
    totalwidth = sum(image.width for image in images)
    maxheight = max(image.height for image in images)
    
    #creating a new blank image with the specified width and height
    combinedimage = Image.new("RGB", (totalwidth, maxheight))

    #initializing the x position for pasting images
    xoffset = 0

    #loop through all images and paste them side-by-side
    for img in images:
        combinedimage.paste(img, (xoffset, 0))  #pasting images at the current x-position (xoffset)
        xoffset += img.width  #updating xoffset for each image

    #saving the final combined image
    collagename = f"ComboCollage{collagenumber}.png"
    #trying to save it
    try:
        combinedimage.save(os.path.join(outputfolder, collagename))
        print(f"collage saved as {collagename}")
    #error message, just in case
    except Exception as e:
        print(f"error saving collage: {e}")

#method for creating collages with all images from a folder
def createcollagesfromfolder(inputfolder, outputfolder, imagespercollage=20):
    #get all jpg files from a folder and sort them alphabetically
    try:
        imagepaths = sorted([os.path.join(inputfolder, f) for f in os.listdir(inputfolder) if f.endswith('.png')])
    
    #error messages
    except Exception as e:
        print(f"error: {e}")
        return

    #just in case of running into errors where there are no png files
    if not imagepaths:
        print("no .png. double check.")
        return

    print(f"found {len(imagepaths)} images.")

    #processing images in batch of tens (so in each big collage, there are 10 individual collages)
    for i in range(0, len(imagepaths), imagespercollage):
        #getting the current batch
        batchimages = imagepaths[i:i + imagespercollage]
        #creating a collage for the batch and saving it in the output folder
        createcollage(batchimages, i // imagespercollage + 1, outputfolder)

#input and output folders
inputfolder = "/Users/marie/Desktop/MaNGA Scrape/Storing MaNGA Scrapes" 
outputfolder = "/Users/marie/Desktop/MaNGA Scrape/Combo Collage"

#creating the collage
createcollagesfromfolder(inputfolder, outputfolder)
