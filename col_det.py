#program to detect the color of a pixel of an image 

import pandas as pd
import cv2

#reading an image (it is present in the same directory as the program)

img = cv2.imread("buildings.jpg")

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
r = g = b = xpos = ypos = 0

#function to return the coordinates of the mouse click
#here we are going to use a single left mouse click

def retcoor(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)
       
cv2.namedWindow('image')
cv2.setMouseCallback('image',retcoor)

#function to display the rectangular window with the rgb color code and hex value in it



while(1):

    cv2.imshow("image",img)
    if (clicked):
    
        cv2.rectangle(img,(20,20), (750,60), (b,g,r), -1)

        text = getColorName(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)
        
        cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)

        if(r+g+b>=600):
            cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
            
        clicked=False


    #here press escape to exit the window
       
    if cv2.waitKey(20) & 0xFF ==27:
        break


#removing the generated GUI from the memory 

cv2.destroyAllWindows()
