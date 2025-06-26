#importing libraries
import os
from PIL import Image

#creating the larger, rectangular collage
def createcollage(imagepaths, collagenumber, outputfolder):
    #opening and accessing the original collages
    try:
        images = [Image.open(imagepath).convert("RGBA") for imagepath in imagepaths]
    except Exception as e:
        print(f"error opening these images: {e}")
        return
    
    #calculating the total width and height needed
    totalwidth = sum(image.width for image in images)
    maxheight = max(image.height for image in images)
    
    #creating a combined collage
    combinedimage = Image.new("RGBA", (totalwidth, maxheight), (255, 255, 255, 0))  # Support transparency

    #initialize the horizontal offset so the images start centered at (0,0)
    xoffset = 0
    for img in images:
        #paste the current image at (offset, 0) to paste collages side-by-side
        combinedimage.paste(img, (xoffset, 0), img if img.mode == "RGBA" else None)
        #move the xoffset coordinate to the right by the width of the image just measured
        xoffset += img.width  

    collagename = f"ComboCollage{collagenumber}.png"

    #try to save the newly combined collage
    try:
        combinedimage.convert("RGB").save(os.path.join(outputfolder, collagename))  # Save as RGB
        print(f"collage saved as {collagename}")
    #if any errors are encountered, error message is raised
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
inputfolder = "/Users/marie/Desktop/MaNGA Scrape/New Rescaled MaNGA Collage" 
outputfolder = "/Users/marie/Desktop/MaNGA Scrape/New Rescaled Combo Collage"

#creating the collage
createcollagesfromfolder(inputfolder, outputfolder)
