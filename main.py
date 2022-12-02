import os, sys
import glob
from PIL import Image
from PIL import ImageEnhance

if __name__=="__main__":

    input_directory = input("Enter the folder of input directory: ")
    #print(input_directory)

    output_directory = input("Enter the folder of output directory: ")
    #print(output_directory)
    output_directory = f"{output_directory}{'/'}"
    print(output_directory)

    enhancing_minutes = int(input("Enter the enhancing time in minutes: "))
    #print(enhancing_minutes)

    brightness = float(input("Enter the brightness enhancement factor: "))
    #print(brightness)

    sharpness = float(input("Enter the sharpness enhancement factor: "))
    #print(sharpness)

    contrast = float(input("Enter the contrast enhancement factor: "))
    #print(contrast)

    num_threads = int(input("Enther the number of threads/process to use: "))
    #print(num_threads)

    list_directory = []
    extensions = ('/*.jpg', '/*.png', '/*.gif')

    for ext in extensions:
        list_directory.append(f"{input_directory}{ext}")

    #print(list_directory)

    image_files = []
    output_files = []

    #Getting all files that has the extensions .jpg .png .gif in the source folder and storing it in the list
    for files in list_directory:
        image_files.extend(glob.glob(files))


    #Enhancing images inside the list and saving to destination folder
    for images in image_files:
        image_enhanced = Image.open(images)
        fn = str(image_enhanced.filename)
        brigthness_img = ImageEnhance.Brightness(image_enhanced)
        image_enhanced = brigthness_img.enhance(brightness)
        sharpness_img = ImageEnhance.Sharpness(image_enhanced)
        image_enhanced = sharpness_img.enhance(sharpness)
        contrast_img = ImageEnhance.Contrast(image_enhanced)
        image_enhanced = contrast_img.enhance(contrast)
        image_enhanced.show()
        dump = fn.split("\\")
        fn = dump[-1]
        image_enhanced.save(f"{output_directory}{fn}")
        