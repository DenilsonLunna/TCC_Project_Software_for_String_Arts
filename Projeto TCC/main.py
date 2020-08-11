import cv2
import numpy as np
from tkinter import filedialog
from math import sin, cos, radians
from random import randint
import copy 



def transformImageInBlackAndGray(imagem):
    return cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)


def putFilterBlackWhite(imagem, limiar):
    ret, imgT = cv2.threshold(imagem, limiar, 255, cv2.THRESH_BINARY)
    return imgT


def printImage(image, time):
    cv2.imshow("imagem", image)
    key = cv2.waitKey(time)
    if key == 27:
        cv2.destroyAllWindows()
        return -1


def createCanvas(image):
    canvas = copy.copy(image)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            canvas[i, j] = 255
    return canvas





def nailsCreate(image, nailsQuantity):
    size = image.shape
    center = [int(size[1] / 2), int(size[0] / 2)]
    angle = 360 / nailsQuantity
    for i in range(0, nailsQuantity):
        x = int(center[0] + ((center[0] - 1) * sin(-(radians(angle * i)))))
        y = int(center[1] + ((center[0] - 1) * cos(-(radians(angle * i)))))
        # image.itemset((y, x), 0)
        if(image[y,x] == 0):
            image[y:y+5, x: x+5] = 255 #adicionando ponto na imagem no tamanho 3x3 pixels
        else:
            image[y:y+5, x: x+5] = 0 #adicionando ponto na imagem no tamanho 3x3 pixels
        nail_positions.append([x, y])
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

def editImage(imagem, limiar):
    imagem = transformImageInBlackAndGray(imagem)
    imagem = putFilterBlackWhite(imagem, limiar)
    return imagem

def algorithmWeaver(lineQtd):
    actual_point = nail_positions[0]
    segments = [0]
    lines = 0
    cont1 = 0
    cont2 = 0
    while True:
        bigger = [0, nail_positions[0], nail_positions[0]]
        for i in range(0, nailsQuantity):
            point_analysis = nail_positions[i]
            a = pixels_analysis(actual_point, point_analysis, img)
            if a[0] > bigger[0]: #a quantidade de pixels dessa linha é maior do que a maior atual? 
                bigger = [a[0], a[1], a[2]]
        actual_point = bigger[2]
        line = [bigger[1], bigger[2]]
        index = nail_positions.index(bigger[2])
        segments.append(index)
        cv2.line(img, (line[1][0], line[1][1]), (line[0][0], line[0][1]), (255, 255, 255), 1)
        cv2.line(canvas, (line[1][0], line[1][1]), (line[0][0], line[0][1]), (0, 0, 0), 1)
        image_output_1 = cv2.resize(img, (700, 700))
        image_output_2 = cv2.resize(canvas, (700, 700))
        
        #essa parte comentada é para criar as imagens no decorrer do processo, ele vai salvar imagens com multiplos de 20 e multiplos de 250
        #usei para gerar uma imagem não apague pois posso precisar de novo
        '''if((lines < 200) and (lines % 20) == 0):
            cv2.imwrite("img_{}_.png".format(cont1),image_output_1)
            cv2.imwrite("imgString_{}_{}lines_.png".format(cont2,lines),image_output_2)
            cont1 = cont1 +1
            cont2 = cont2 +1
        if ((lines % 250) == 0):
            cv2.imwrite("img_{}_.png".format(cont1),image_output_1)
            cv2.imwrite("imgString_{}_{}lines_.png".format(cont2,lines),image_output_2)
            cont1 = cont1 +1
            cont2 = cont2 +1'''
            
        cv2.imshow('output_1', image_output_1)
        cv2.imshow('output_2', image_output_2)
        k = cv2.waitKey(1)
        if(k == 27):
            break
        lines += 1
        if bigger[0] == 0 or lines == lineQtd:
            break
        
def cutImage(imagem):
    y = imagem.shape[0]
    x = imagem.shape[1]
    yM = int(y/2)
    xM = int(x/2)
    smaller = 0
    if(yM < xM):
        smaller = yM
    else:
        smaller = xM
   
    if(smaller == yM):
        initialPoint = yM - smaller
    else:
        initialPoint = xM - smaller
    
    tam = smaller*2
    
    crop = imagem[initialPoint:tam,initialPoint:tam]
    crop = cv2.resize(crop,(1000,1000))
    return crop
    
    
    
    
# ===================================================== MAIN ============================================
imagemPath = filedialog.askopenfilename()
imagem = cv2.imread(imagemPath, 1)

img = editImage(imagem,80)


img = cutImage(img)
nail_positions = []
nailsQuantity = 210
canvas = createCanvas(img)
canvas = nailsCreate(canvas,nailsQuantity)
img = nailsCreate(img, nailsQuantity)
cv2.imwrite("etapaNails.png",img)


algorithmWeaver(25)

fileSeparated = imagemPath.split("/")
nameFile = fileSeparated[len(fileSeparated) - 1]
cv2.imwrite("StringArt_{}".format(nameFile),canvas)
    
    
            
    
        
