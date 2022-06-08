#program to detect the color of a pixel of an image 

import pandas as pd
import cv2

#reading an image (it is present in the same directory as the program)

img = cv2.imread("pixcol.jpg")

#reading the csv file and adding the coloumn names which were not initially present in the dataframe
#the csv file is also present in the same directory as the program

colnames = ['color','color_name','hex','R','G','B']
df = pd.read_csv("colors.csv",names=colnames,header= None)

# fucntion to get color name from csv file (using pandas)
# it is basically used to calculate the minimum distance from the most matching color in the dataset as all the 255x255x255 color codes are not given in the csv file

def getColorName(R,G,B):
    minimum = 10000
    
    for i in range(len(df)):
        d = abs(R- int(df.loc[i,"R"])) + abs(G- int(df.loc[i,"G"]))+ abs(B- int(df.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = df.loc[i,"color_name"]
    return cname

#global variables for further use

clicked = False 
r = g = b = 0

#function to return the coordinates of the mouse click
#here we are going to use a single left mouse click

def click_event(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global r,g,b,clicked #defining the varibles global
        clicked = True
        b,g,r=img[y,x] 
        r = int(r)
        g = int(g)
        b = int(b)

        if (clicked): #as this condition is checked afterwards; the setMouseCallback function already had to be executed to check if there is a mouse event(click)
            cv2.rectangle(img,(0,0), (600,60), (b,g,r), -1) #-1 is to fill the rectangle with the color
            text = getColorName(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b) 
            cv2.putText(img,text,(50,40),2,0.8,(255,255,255),2,cv2.LINE_AA)
            if(r+g+b>=600): #if the color of pixel is too light then it will be displayed with black text
                cv2.putText(img,text,(50,40),2,0.8,(0,0,0),2,cv2.LINE_AA)   
            clicked=False
       
cv2.namedWindow('image',cv2.WINDOW_NORMAL) #function to create a window of suitable size to display the picture on the screen
cv2.setMouseCallback('image',click_event) #this function is used to call the mentioned function 'click_event' during any mouse event {over here it is 'EVENT_LBUTTONDBLCLK'}

#function to display the rectangular window with the rgb color code and hex value in it

while(True):
    cv2.imshow("image",img) #to display the image on the screen    
    if cv2.waitKey(20) & 0xFF ==27: 
        break

#removing the generated GUI from the memory 

cv2.destroyAllWindows()
