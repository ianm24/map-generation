# Program Made By: Ian McDowell
# Started 8 Oct 2020

from PIL import Image
import glob, os, imageio, random, math
path = 'images'

#map maker
def map_maker(
	filename,width,height,
	lastColorIncentive,
	landToWater,nRange):
	img = Image.new("RGBA",(width, height),(0,0,0,0))
	img.save(path+'/'+filename+'.bmp')
	blue = (10,0,240,255)
	green = (0,240,10,255)
	lastColor = 0
	for x in range(width):
		for y in range(height):
			if(random.random() + lastColorIncentive*lastColor<= landToWater):
				img.putpixel((x,y),green)
				lastColor = landToWater
			else:
				img.putpixel((x,y),blue)
				lastColor = -landToWater
	print("initial "+filename+" map Pixels Placed")
	img.save(path+'/'+filename+'.bmp')

	for x in range(width):
		for y in range(height):
			im = Image.open(path+'/'+filename+'.bmp')
			pixels = im.load()
			neighborProportion = check_neighbors(pixels,width,height,x,y,nRange)
			# print(x,y,neighborProportion)
			if neighborProportion < landToWater:
				img.putpixel((x,y),green)
			elif neighborProportion > landToWater:
				img.putpixel((x,y),blue)
			else:
				img.putpixel((x,y), pixels[x,y])
			img.save(path+'/'+filename+'.bmp')
	print("Final "+filename+" map Pixels Placed")
	img.save(path+'/'+filename+'.bmp')

def check_neighbors(pixels,width,height,posX,posY,nRange):
	numGreen = 0
	numBlue = 0
	for x in range(posX-nRange,posX+nRange):
		for y in range(posY-nRange,posY+nRange):
			if x < 0 or x >= width or y < 0 or y >= height:
				continue
			if pixels[x,y] == (10,0,240):
				numBlue = numBlue+1
			elif pixels[x,y] == (0,240,10):
				numGreen = numGreen+1
	return numGreen/(numBlue+numGreen)

#map_maker
#	filename: string; name of the image file
#	width:	int i > 0; width of the image file
#	height: int j > 0; height of the image file
#	lastColorIncentive: float y; incentive for a pixel to be the same as the last one placed
#	landToWater: float 0 <= x <= 1; percent (roughly) of the image with land
#	nRange: int 0 < k <= max(width,height); neighbor range for checking land to water proportion
#

width = 100
height = 50
map_maker("map1",width,height,0.3,0.3,1)
map_maker("mapH10",width,height,0.3,0.3,int(height/10))
map_maker("mapW10",width,height,0.3,0.3,int(width/10))
map_maker("mapH5",width,height,0.3,0.3,int(height/5))
map_maker("mapW5",width,height,0.3,0.3,int(width/5))
map_maker("mapH2",width,height,0.3,0.3,int(height/2))
map_maker("mapW2",width,height,0.3,0.3,int(width/2))
map_maker("mapH",width,height,0.3,0.3,height)
map_maker("mapW",width,height,0.3,0.3,width)