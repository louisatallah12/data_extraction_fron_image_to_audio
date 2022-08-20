# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 16:03:33 2022

@author: Louis Atallah

PARTS 2 & 3
"""
# importing libraries

from fileinput import close
from gtts import gTTS
from playsound import  playsound
from PIL import Image
import cv2
import numpy as np
import pytesseract

language='en'

# function to play a sound from an mp3 file  

def play(filename):
	
	open(filename)
	playsound(filename)
	close()
	
# path to reach the pytesseract module
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

####################################### PART 2 ##############################

mytext = pytesseract.image_to_string(Image.open('Capture.png'))			# getting the text from the image
myobj=gTTS(text=mytext,lang=language,slow=True)					# generating a gtts object to create an mp3 file

# getting the whole data of the graph
data = pytesseract.image_to_data(Image.open('Capture.png'), output_type='data.frame')
data = data.dropna()				# we drop the NaN
data = data[data['text'] != " "]	# we don't select elements containing only a blank
data = data[data['conf'] > 40]		# threshold of 40 for the confidence

print(data)

myobj.save("Graph.mp3")			# saving the file to read it


####################################### PART 3 ##############################


# Loop to iterate on the different graphs
# and perform the transformation


for i in range(1,4):
	img = Image.open('Capture'+str(i)+'.png')
	data = pytesseract.image_to_data(img, output_type='data.frame')			# Store the data from the graph into a dataframe
	data = data.dropna()				# we drop the NaN
	data = data[data['text'] != " "]	# we don't select elements containing only a blank
	data = data[data['conf'] > 40]		# threshold of 40 for the confidence

	# if the data frame is empty, then we modify the image to 
	# have a better accuracy

	if data.empty:
		img = Image.open('Capture'+str(i)+'.png').convert('L')
		ret,img = cv2.threshold(np.array(img), 125, 255, cv2.THRESH_BINARY)
		img = Image.fromarray(img.astype(np.uint8))

		data = pytesseract.image_to_data(img, output_type='data.frame')
		data = data.dropna()
		data = data[data['text'] != " "]
		data = data[data['conf'] > 40]
	
	data['text'] = data['text'].astype(str)


	img.show()			# showing the graph
	
	# graph described via audio mode
	# assembling the text
	mytext = "Graph "+ str(i)
	for j in range(data.shape[0]) : 
		mytext+= str(data.iloc[j,11])+" "

	myobj=gTTS(text=mytext,lang=language,slow=True)
	myobj.save('Graph'+str(i)+'.mp3')
	play('Graph'+str(i)+'.mp3')
	print(data)


