"""
    This script is intended to read all image from one directory then,
        compress and resize all jpg, or jpeg images in directory and 
        write the output in another directory.
    
    INPUT Directory is the source directory where all the images resides.
    OUTPUT Directory will contain the output after the script is run.
    
    usage: python compress.py <input_directory_path> <output_directory_path> <options (optional)>

    Author: Zain Ulabidin
    Email : zainulabidin302@gmail.com
"""
from PIL import Image
import sys
import re
import shutil
import os
args = sys.argv
files = None

def processImage(source, dest):
    img = Image.open(source)
    BASE_HEIGHT = 1200
    HPERCENT = (BASE_HEIGHT/float(img.size[1]))
    WIDTH_SIZE = int((float(img.size[0])*float(HPERCENT)))
    img = img.resize((WIDTH_SIZE,BASE_HEIGHT), Image.ANTIALIAS)
    img.save(dest,"JPEG", quality=5)


def main(argv):
    
    if (len(args) < 3):
        print('usage: python compress.py <input_directory_path> <output_directory_path>')
        sys.exit(0)
    # Check if the given path in command line arguments exists.
    if not os.path.isdir(args[1]):
        print('INPUT Directory does not exists.')
        sys.exit(-1)
    # Check if the given path for output exists.
    if not os.path.isdir(args[2]):
        print('OUTPUT Directory does not exists.')
        sys.exit(-1)
    
    options = args[3:]
    files = os.listdir(str(args[1]))
    if len(files) < 1:
        print('INPUT Directory is empty')
        sys.exit(-1)
    
    if '--clean' in options:
        try:
            shutil.rmtree(args[2])
            os.mkdir(args[2])
        except:
            print('Error while directory content.')
            sys.exit(-1)


    for i, f in enumerate(files):
        print(f)
        ## only process jpeg or jpg images.
        if any(f.endswith(ext) for ext in ['jpeg', 'jpg']):
            src = os.path.join(args[1], f)
            dst = os.path.join(args[2], "{}.jpg".format(str(i)) )
            processImage(src, dst)

if __name__ == '__main__':
    main(sys.argv)