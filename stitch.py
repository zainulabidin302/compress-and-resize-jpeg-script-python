#!/usr/local/bin/python
# https://stackoverflow.com/questions/30227466/combine-several-images-horizontally-with-python
import sys
from PIL import Image
import sys

images_to_stich = sys.argv[2:]
output_image = sys.argv[1]
print(images_to_stich, output_image)


images = map(Image.open, images_to_stich)
widths, heights = zip(*(i.size for i in images))

total_width = sum(widths)
max_height = max(heights)

new_im = Image.new('RGB', (total_width, max_height))

x_offset = 0
for im in images:
  new_im.paste(im, (x_offset,0))
  x_offset += im.size[0]

new_im.save(output_image)