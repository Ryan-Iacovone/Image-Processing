# libraries 

from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
from PIL.ExifTags import TAGS
import time
from datetime import datetime


# Function to extract the date from a picture's metadata 
def extract_date_taken(image_path):
    try:
        with Image.open(image_path) as img:
            #Getting the meta data of the image
            exif_data = img._getexif()

            if exif_data:
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    if tag_name == 'DateTimeOriginal':
                        date_str = str(value)

                        # Convert the date string to a date object
                        date_obj = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')

                        # Reformat the date object as a string that takes the form of 'MM/DD/YY'
                        formatted_date = date_obj.strftime('%m/%d/%y')
                        return formatted_date
                    
    except (AttributeError, KeyError):
        pass
    return None


#function to write the date an image was taken on the image
def overlay_date_on_image(image_path, date_taken):
    
    with Image.open(image_path) as img:
        # Need to transpose the image here so PIL properly reads all metadata and doesn't randomly rotate images
        img = ImageOps.exif_transpose(img)

        draw = ImageDraw.Draw(img)
        #Gathering the dimensions of the image to make a proportional font size based on each image
        width, height = img.size
        #Adding the font type and size 
        font = ImageFont.truetype(r"C:\Windows\Fonts\timesbd.ttf", int(min(width, height) * 0.0225))  # You may need to change the font path

        #The written text I want on each image and it's location 
        text = f"Date Taken: {date_taken}"
        text_bbox = draw.textbbox((0, 0), text, font)
        x = width - text_bbox[2] - 10  # Adjust the position as needed
        y = 10  # Adjust the position as needed

        #The color I use here (255, 165, 0) is orange
        draw.text((x, y), text, fill=(255, 165, 0), font=font)

        #Saving the new image over the old one, but maintaining all meta data from original pic
        img.save(image_path, exif=img.info["exif"])

# Defining the folder path where I want to direct this program to look for images to write the dates on 
folder_path = 'coolio pics'

# Looping over each file that qualifies as a picture and writing the date it was taken on it 
# Applying both functions I wrote above 
pics = 0

for filename in os.listdir(folder_path):

    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):

        image_path = os.path.join(folder_path, filename)
        date_taken = extract_date_taken(image_path)

        if date_taken:
            overlay_date_on_image(image_path, date_taken)
            pics += 1

print(f"The date was added to {pics} pictures in the \"{folder_path}\" directory!\n")

#Counting the total number of files in the directory
total_files = len(os.listdir(folder_path))

print(f"Therefore, out of the {total_files} files in the directory, {(pics/total_files) * 100:.2f}% of them were transformed.")