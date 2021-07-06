import cv2 as cv
import numpy as np
import pandas as pd
import argparse

# Tạo argumnet parser để thêm ảnh vào command line
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help='Image Path')
args = vars(ap.parse_args())
img_path = args['image']

# Read image in command line with openCv
img = cv.imread(img_path)

# declare global variable
clicked = False
red = green = blue = xpos = ypos = 0

# Reading .csv file with pandas
name = ['color', 'color_name', 'hex', 'R', 'G', 'B']
data = pd.read_csv('colors.csv', names=name, header=None)
print(data.head())

def getColorName(r,g,b):
    minimun = 10000
    for i in range(len(data)):
        # Lọc giá trị ở các cột màu R,G,B để tính toán
        d = abs(r- int(data.loc[i, 'R'])) + abs(g- int(data.loc[i, 'G'])) + abs(b- int(data.loc[i, 'B']))
        if (d<minimun):
            minimun = d
            cname = data.loc[i, 'color_name']
    return cname

def draw_func(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)

cv.namedWindow('image')
cv.setMouseCallback('image', draw_func)

while(1):
    cv.imshow('image', img)
    if(clicked):
        cv.rectangle(img, (20,20), (750, 60), (b,g,r), -1)

        text = getColorName(r,g,b) + ' RED='+ str(r) + ' GREEN='+str(g) + ' BLUE='+str(b)
        cv.putText(img, text, (50,50), 2,0.8, (255,255,255), 2, cv.LINE_AA)

        if(r+g+b >= 600):
            cv.putText(img, text, (50,50), 5, 0.8, (0,0,0),2,cv.LINE_AA)

        clicked = False

    if cv.waitKey(20) & 0xFF == 27:# ESC
        break

cv.destroyAllWindows()