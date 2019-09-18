# Compress and resize Width and Height of jpeg image with python script

This script is intended to read all image from one directory then,
    compress and resize all jpg, or jpeg images in directory and 
    write the output in another directory.

INPUT Directory is the source directory where all the images resides.
OUTPUT Directory will contain the output after the script is run.

## usage: 
   `python compress.py <input_directory_path> <output_directory_path> <options (optional)>`



## examples: 
* jpg with 50% quality reduction
    
    `python compress.py input_dir output_dir --format jpg --quality 50`
 
* jpg with 90% quality reduction
    `python compress.py input_dir output_dir --format jpg --quality 10`

* png with 90% quality reduction
    `python compress.py input_dir output_dir --format png --quality 1`

* png with 10% quality reduction
    `python compress.py input_dir output_dir --format png --quality 9`

## default:
    `--format: jpg`
    `--quality: 5`

Author: Zain Ulabidin
Email : zainulabidin302@gmail.com
