# Program Made By: Ian McDowell
# Started 8 Oct 2020

from datetime import datetime
from PIL import Image
import glob, os, imageio, random, math, csv
path = 'maps'

#map maker
def map_maker(
	filename,width,height,
	lastColorIncentive,
	landToWater,nRange):
	mapStart = datetime.now()
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
	img.save(path+'/'+filename+'.bmp')
	mapEnd = datetime.now()
	with open('mapTimes.csv','a') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow([filename,str(mapEnd-mapStart)])
	print("Final "+filename+" map Pixels Placed. Total time: "+str(mapEnd-mapStart))

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

start = datetime.now()
counter = 0

LCI = -1.0 # last color incentive
LTW = 0.0 # land to water
NRD = 1 # nRange denominator
while LCI <= 1.0:
	while LTW <= 1.0:
		while NRD <= 10:
			for denomSet in range(0,3):
				if denomSet == 0 and NRD > 1:
					continue
				filename = "map_LCI"+str(round(LCI,1)).replace("-","n").replace(".","-")+"_LTW"+str(round(LTW,1)).replace(".","-")
				if denomSet == 0 and NRD == 1: #nRange = 1
					filename += "_NR-1"
					map_maker(filename,width,height,LCI,LTW,1)
				elif denomSet == 1: #nRange = height/NRD
					filename += "_NR-H"+str(NRD)
					map_maker(filename,width,height,LCI,LTW,int(height/NRD))
				elif denomSet == 2: #nRange = width/NRD
					filename += "_NR-W"+str(NRD)
					map_maker(filename,width,height,LCI,LTW,int(width/NRD))
				counter += 1
			NRD += 1
		NRD = 1
		LTW += 0.1
	LTW = 0.0
	LCI += 0.1

end = datetime.now()
with open('mapTimes.csv','a') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow([start,end,end-start])
print("Took "+str(datetime.now()-start)+" to generate "+str(counter)+" maps.")