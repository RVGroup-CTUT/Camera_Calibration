
import cv2
import os, os.path
import glob, os

image_dir = "IMG_VIEWS"
current_dir = os.getcwd()
image_savepath = os.path.join(current_dir, image_dir)
print("image save path", image_savepath)
if not os.path.isdir(os.path.abspath(image_savepath)):
    os.mkdir(image_savepath)
