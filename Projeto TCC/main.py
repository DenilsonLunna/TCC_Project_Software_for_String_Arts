import cv2
import numpy as np
from math import sin, cos, radians
from random import randint

nailsQuantity = 210

def transformImageInBlackAndGray(imagem):
    return cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)


def putFilterBlackWhite(imagem, limiar):
    ret, imgT = cv2.threshold(imagem, limiar, 255, cv2.THRESH_BINARY)
    return imgT


def printImage(image, time):
    cv2.imshow("soccer", image)
    key = cv2.waitKey(time)
    if key == 27:
        cv2.destroyAllWindows()
        return -1


def createCanvas(image):
    canvas = image
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            canvas[i, j] = 255
    return canvas

positionsNails = []
def nailsCreate(image, nailsQuantity):
    size = image.shape
    center = [int(size[1] / 2), int(size[0] / 2)]
    angle = 360 / nailsQuantity
    for i in range(0, nailsQuantity):
        x = int(center[0] + ((center[0] - 1) * sin(-(radians(angle * i)))))
        y = int(center[1] + ((center[0] - 1) * cos(-(radians(angle * i)))))
        #image.itemset((y, x), 0) 
        image[y:y+3, x: x+3] = 0
        positionsNails.append([x,y]) 
    return image
def pixels_analysis(point_1, point_2, im):
    yd = point_2[0] - point_1[0]
    xd = point_2[1] - point_1[1]
    y_abs = abs(yd)
    x_abs = abs(xd)
    if y_abs > x_abs:
        step = y_abs
    else:
        step = x_abs
    black_pixels = 0
    for pixel in range(1, step):
        y_position = int(round(point_1[0] + (yd * (pixel / step))))
        x_position = int(round(point_1[1] + (xd * (pixel / step))))
        pxp = [x_position, y_position]
        color = im.item(pxp[0], pxp[1])
        if color == 0:
            black_pixels += 1
    return [black_pixels, point_1, point_2]
# ===================================================== MAIN ============================================
imagem = cv2.imread("rosto01.jpg", 1)
img = transformImageInBlackAndGray(imagem)
img = putFilterBlackWhite(img, 127)

#canvas = createCanvas(img)
#canvas = nailsCreate(canvas,210)
img = nailsCreate(img,nailsQuantity)


v = 1

for i in range(0,nailsQuantity):
    actualPoint = positionsNails[randint(0,len(positionsNails)-1)]
    finalPoint = positionsNails[randint(0,len(positionsNails)-1)]
    cv2.line(img, (actualPoint[0],actualPoint[1]), (finalPoint[0],finalPoint[1]), 0,1)
    a = pixels_analysis(actualPoint,finalPoint, img)
    print(a)
    v = printImage(img,100)
    if(v == -1):
        break
        
