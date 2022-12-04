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
    def __init__(self, count, process_ID, queue, img_counter, semaphore):
        multiprocessing.Process.__init__(self)
        self.counter=int((count/num_process))
        self.list=[]
        self.item=0
        self.ID=process_ID
        self.queue=queue
        self.brightness = brightness
        self.sharpness = sharpness
        self.contrast = contrast
        self.enhance_time = time.perf_counter() + (enhancing_minutes * 60)
        self.output_directory = output_directory
        self.semaphore = semaphore
        self.img_counter = img_counter

    def run(self):
        start_time = time.perf_counter()
        curr_time = start_time
        end_time = 0
        for i in range(self.counter):
            # If start time is greater than the enhance time in minutes, stop the loop
            curr_time = time.perf_counter()
            if(curr_time > self.enhance_time):
                print("Process: %d" % self.ID + " finished processing due to timeout")
                break

            else:
                self.item=self.queue.get()
                self.list.append(self.item)

                print("Process: %d" % self.ID + " is enhancing Image: " + self.item)
                image_enhanced = Image.open(self.item)
                fn = str(image_enhanced.filename)
                dump = fn.split("\\")
                fn = dump[-1]

                dump2 = str(dump[-1]).split(".")
                ifGif = dump2[-1]

                if(str(ifGif) == "gif"):    # If images is in gif format
                    image_new = []
                    for frame in range(image_enhanced.n_frames):
                        image_enhanced.seek(frame)
                        new_frame = Image.new('RGB', image_enhanced.size)
                        new_frame.paste(image_enhanced)

                        brightness_img = ImageEnhance.Brightness(new_frame.convert('RGB'))
                        new_frame = brightness_img.enhance(self.brightness)
                        sharpness_img = ImageEnhance.Sharpness(new_frame.convert('RGB'))
                        new_frame = sharpness_img.enhance(self.sharpness)
                        contrast_img = ImageEnhance.Contrast(new_frame.convert('RGB'))
                        new_frame = contrast_img.enhance(self.contrast)
                        image_new.append(new_frame)

                    image_new[0].save(f"{self.output_directory}{fn}", append_images=image_new[1:], save_all=True)
                    self.semaphore.acquire()        # Acquiring semaphore so other process cant increment the manager.value
                    self.img_counter.value += 1
                    self.semaphore.release()

                else:                       # If images is in jpg or png format
                    brightness_img = ImageEnhance.Brightness(image_enhanced)
                    image_enhanced = brightness_img.enhance(self.brightness)
                    sharpness_img = ImageEnhance.Sharpness(image_enhanced)
                    image_enhanced = sharpness_img.enhance(self.sharpness)
                    contrast_img = ImageEnhance.Contrast(image_enhanced)
                    image_enhanced = contrast_img.enhance(self.contrast)
                    
                    image_enhanced.save(f"{self.output_directory}{fn}")
                    self.semaphore.acquire()        # Acquiring semaphore so other process cant increment the manager.value
                    self.img_counter.value += 1
                    self.semaphore.release()

        print("Process: %d" % self.ID + " finished processing")
        end_time = time.perf_counter()
        total_time = end_time - start_time
        txt_file = open("Output_statistics.txt", "w+")
        txt_file.write("Total Images Processed: %d\r\nOutput Folder Location: ../" % int(self.img_counter.value) + self.output_directory)
        txt_file.close()

if __name__=="__main__":

    queue = multiprocessing.Queue()
    process_list = []

    manager = multiprocessing.Manager()
    num_image_processed = manager.Value('counter', 0)

    resource_lock = multiprocessing.Semaphore(1)

    input_directory = input("Enter the folder of input directory: ")

    output_directory = input("Enter the folder of output directory: ")
    if(os.path.exists(output_directory) == False):  # Checks if directory is existing, if not create the directory
        os.mkdir(output_directory)
    output_directory = f"{output_directory}{'/'}"

    while True:
        enhancing_minutes = input("Enter the enhancing time in minutes: ")
        try:
            enhancing_minutes = int(enhancing_minutes)
            if(enhancing_minutes <= 0):
                print("Positive numbers only, try again")
                continue
            break
        except ValueError:
            print("Positive numbers only, try again")

    brightness = float(input("Enter the brightness enhancement factor: "))

    sharpness = float(input("Enter the sharpness enhancement factor: "))

    contrast = float(input("Enter the contrast enhancement factor: "))

    num_process = int(input("Enther the number of threads/process to use: "))

    list_directory = []
    extensions = ('/*.jpg', '/*.png', '/*.gif')

    for ext in extensions:
        list_directory.append(f"{input_directory}{ext}")


    image_files = []

    #Getting all files that has the extensions .jpg .png .gif in the source folder and storing it in the list
    for files in list_directory:
        image_files.extend(glob.glob(files))
   
    produce = append_image(len(image_files), queue, image_files)
    produce.start()

    for i in range(int(num_process)):
        process = process_class(len(image_files), i, queue, num_image_processed, resource_lock)
        process_list.append(process)
        process.start()

    for p in process_list:
        p.join()


    
        
