import os
import glob

files = glob.glob('camera_images/*')
for f in files:
    os.remove(f)