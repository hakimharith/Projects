
# Python program to illustrate HoughLine 
# method for line detection 
import cv2 
import numpy as np
import math
import glob
from os import listdir
from PIL import Image as PImage
import csv
  
# Reading the required image in  
# which operations are to be done.  
# Make sure that the image is in the same  
# directory in which this python program is

ImageNameList = []
AngleList = []

path = r'C:\Users\hakim\OneDrive\Desktop\Angle Measurement\Week 8 Results\11.5deg-ccw\*.*'
#change path accordingly
for file in glob.glob(path):

    #ImageName = '33.jpg'
    img = cv2.imread(file)
    img[0,0] = [0,0,255]
      
    # Convert the img to grayscale 
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
      
    # Apply edge detection method on the image 
    edges = cv2.Canny(gray,50,150,apertureSize = 3) 
      
    # This returns an array of r and theta values 
    lines = cv2.HoughLines(edges,1,np.pi/180, 200) 
      
    # The below for loop runs till r and theta values  
    # are in the range of the 2d array 
    for r,theta in lines[0]: 
          
        # Stores the value of cos(theta) in a 
        a = np.cos(theta) 
      
        # Stores the value of sin(theta) in b 
        b = np.sin(theta) 
          
        # x0 stores the value rcos(theta) 
        x0 = a*r 
          
        # y0 stores the value rsin(theta) 
        y0 = b*r 
          
        # x1 stores the rounded off value of (rcos(theta)-1000sin(theta)) 
        x1 = int(x0 + 1000*(-b)) 
          
        # y1 stores the rounded off value of (rsin(theta)+1000cos(theta)) 
        y1 = int(y0 + 1000*(a))
      
        # x2 stores the rounded off value of (rcos(theta)+1000sin(theta)) 
        x2 = int(x0 - 1000*(-b)) 
          
        # y2 stores the rounded off value of (rsin(theta)-1000cos(theta)) 
        y2 = int(y0 - 1000*(a))
          
        # cv2.line draws a line in img from the point(x1,y1) to (x2,y2). 
        # (0,0,255) denotes the colour of the line to be  
        #drawn. In this case, it is red.  
        cv2.line(img,(x1,y1), (x2,y2), (0,0,255),2) 
          
    # All the changes made in the input image are finally 
    # written on a new image houghlines.jpg 
    cv2.imwrite('linesDetected.jpg', img)

    dy = y1-y2
    dx = x2-x1

    pi = 3.1415

    angle = math.atan2(dy, dx)

    angle_degrees = (angle/3.1415)*180
    ImageSubString = file[path.find('\\', 50)+1:]
    #print(ImageSubString)#changed from ImageName
    #print(angle_degrees)
    #print(x1, y1)
    #print(x2, y2)
    #print(dx, dy)
    ImageNameList.append(ImageSubString)
    AngleList.append(angle_degrees)
    print(ImageSubString)

#print(ImageNameList)
#print(AngleList)

SlashLocation = path.find('\\', 52)
FileSubString = path[50:SlashLocation]
filename = FileSubString + "_Results.csv"

with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Image File", "Angle Recorded", "Difference"])
    for i in range(0, len(glob.glob(path)), 1):
        if i is 0:
            writer.writerow([ImageNameList[i], AngleList[i], 0])
        else:
            writer.writerow([ImageNameList[i], AngleList[i], (AngleList[i]-AngleList[i-1])])

print("Done!")
print(str(len(glob.glob(path))) + " files processed")
print(FileSubString)

#fix error problem where some pictures will obtain an error, eg. 31


    
