#!/usr/bin/env python3

import PIL
from PIL import Image
import color
from color.color import Color
import math

def writeSquareImage(colorList, filename, finalSize = (500, 500)):
	length = len(colorList)
	height = math.floor(math.sqrt(length))
	width = math.ceil(length / height)
	
	image = Image.new("RGB", (width, height))
	try:
		for i in range(height):
			for j in range(width):
				pixel = colorList[width * i + j].toRgb()
				image.putpixel((j, i), pixel)
	except IndexError:
		pass # Finished
	
	image = image.resize(finalSize)
	image.save(filename)
	image.show(filename)
