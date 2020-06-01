from PIL import Image
import os
import string
from matplotlib import pyplot as plt
 
path = "/home/maggie/work/caffe/data/HEMLET&VEST/JPEGImages"         
filelist=os.listdir(path)
 
for file in filelist:
    whole_path = os.path.join(path, file)
    img = Image.open(whole_path)  
    img = img.convert("RGB") 
    save_path =  '/home/maggie/work/caffe/data/HEMLET&VEST/JPEGImages-new/' 
    #img.save(save_path + img1)
    img.save(save_path + file)

