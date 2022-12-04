import os, sys
import glob
from PIL import Image
from PIL import ImageEnhance
import time, random, multiprocessing

class append_image(multiprocessing.Process):
    def __init__(self, count, queue, image_files):
        multiprocessing.Process.__init__(self)
        self.counter=int(count)
        self.list=[]
        self.item=0
        self.queue=queue
        self.image_files = image_files

    def run(self):
        for i in self.image_files:
            self.queue.put(i)
            
class process_class(multiprocessing.Process):
    def __init__(self, count, process_ID, queue):
        multiprocessing.Process.__init__(self)
        self.counter=int((count/num_process))
        self.list=[]
        self.item=0
        self.ID=process_ID
        self.queue=queue
        self.brightness = brightness
        self.sharpness = sharpness
        self.contrast = contrast
        self.output_directory = output_directory

    def run(self):
        for i in range(self.counter):
            self.item=self.queue.get()
            self.list.append(self.item)
            image_enhanced = Image.open(self.item)
            fn = str(image_enhanced.filename)
            brightness_img = ImageEnhance.Brightness(image_enhanced)
            image_enhanced = brightness_img.enhance(self.brightness)
            sharpness_img = ImageEnhance.Sharpness(image_enhanced)
            image_enhanced = sharpness_img.enhance(self.sharpness)
            contrast_img = ImageEnhance.Contrast(image_enhanced)
            image_enhanced = contrast_img.enhance(self.contrast)
            image_enhanced.show()
            dump = fn.split("\\")
            fn = dump[-1]
            image_enhanced.save(f"{self.output_directory}{fn}")

if __name__=="__main__":

    queue = multiprocessing.Queue()
    process_list = []

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

    num_process = int(input("Enther the number of threads/process to use: "))
    #print(num_process)

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

    print(image_files)
        
    produce = append_image(len(image_files), queue, image_files)
    produce.start()

    for i in range(int(num_process)):
        process = process_class(len(image_files), i, queue)
        process_list.append(process)
        process.start()

    for p in process_list:
        p.join()


    
        
