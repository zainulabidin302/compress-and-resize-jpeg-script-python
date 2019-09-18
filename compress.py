#!/usr/local/bin/python3

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
import rmbg
import cv2
import numpy as np
args = sys.argv
files = None

def processImage(source, dest, options):
    img = Image.open(source)
    img = rmbg.removeBackgroundFromImage(source)
    height, width, _ = img.shape

    BASE_HEIGHT = 1200
    HPERCENT = (BASE_HEIGHT/float(height))
    WIDTH_SIZE = int((float(width)*float(HPERCENT)))
    img = cv2.resize(img, (WIDTH_SIZE, BASE_HEIGHT), interpolation = cv2.INTER_AREA)

    if options['format'] == 'jpg':

        params = list()
        params.append(cv2.IMWRITE_JPEG_QUALITY)
        params.append(options['quality'])
        cv2.imwrite(dest, img, params)

    elif options['format'] == 'png':
        # PNG OUTPUT
        params = list()
        params.append(cv2.IMWRITE_PNG_COMPRESSION)
        params.append(options['quality'])
        cv2.imwrite(dest, img, params)
    else:
        print('Unkown format')
        sys.exit(-1)

def main(argv):
    q = 5
    image_format = 'jpg'
    if (len(args) < 3):
        print('usage: python compress.py <input_directory_path> <output_directory_path>')
        sys.exit(0)
    # Check if the given path in command line arguments exists.
    if not os.path.isdir(args[1]):
        print('INPUT Directory does not exists.')
        sys.exit(-1)
    # Check if the given path for output exists.
    if not os.path.isdir(args[2]):
        print('OUTPUT Directory doesls not exists.')
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

    if '--format' in options:
        try:
            i = options.index('--format')
            image_format = options[i + 1]
            print('Format set to {}'.format(image_format))
        except:
            print('Format must be jpg or png')
            sys.exit(-1)


    if '--quality' in options:
        try:
            i = options.index('--quality')
            q = int(options[i + 1])
            
            if image_format == 'jpg':
                if not (q >=0 and q <= 100):
                    raise Exception("For jpg, quality must be between 0, 100")
            elif image_format == 'png':
                if not (q >=0 and q <= 9):
                    raise Exception("For png, quality must be between 0, 9")
            else:
                raise Exception("Unkown image format.")

            print('Quality set to {}'.format(q))
        except Exception as e:
            print(e)
            sys.exit(-1)

    for i, f in enumerate(files):
        print(f)
        ## only process jpeg or jpg images.
        if any(f.endswith(ext) for ext in ['jpeg', 'jpg']):
            src = os.path.join(args[1], f)
            dst = os.path.join(args[2], "{}.{}".format(str(i), image_format) )
            processImage(src, dst, options = {
                'quality': q,
                'format': image_format
            })

if __name__ == '__main__':
    main(sys.argv)