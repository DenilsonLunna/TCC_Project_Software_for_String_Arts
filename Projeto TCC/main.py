import cv2
import numpy as np
from tkinter import filedialog
from math import sin, cos, radians
from random import randint
from telas import app
import copy 

nextLine = 0;

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

def createInfor():
    for y in range(0, nailsQuantity):
        actual_point = nail_positions[y].pos
        for i in range(1, nailsQuantity):
            point_analysis = nail_positions[i].pos
            a = pixels_analysis(actual_point, point_analysis, img)
            nail_positions[y].lines.append(a);
        #ordenando do maior para para o menor
        for i in range(0,nailsQuantity):
            nail_positions[i].lines.sort(reverse=True, key = lambda l:l[0]);

    
        
    






def nailsCreate(image, nailsQuantity):
    size = image.shape
    center = [int(size[1] / 2), int(size[0] / 2)]
    angle = 360 / nailsQuantity
    for i in range(0, nailsQuantity):
        x = int(center[0] + ((center[0] - 1) * sin(-(radians(angle * i)))))
        y = int(center[1] + ((center[0] - 1) * cos(-(radians(angle * i)))))
        # image.itemset((y, x), 0)
        if(image[y,x] == 0):
            image[y:y+5, x: x+5] = 255 #adicionando ponto branco na imagem no tamanho 3x3 pixels
        else:
            image[y:y+5, x: x+5] = 0 #adicionando ponto preto na imagem no tamanho 3x3 pixels
        newNail = Nail([x,y]);
        nail_positions.append(newNail)
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


nextLine = 0;
def algorithmWeaver(lineQtd):
    nextLine = 0;
    lines = 0;
    while True:
        bigger = nail_positions[nextLine].lines[0];
        nail_positions[nextLine].lines.pop(0);
        line = [bigger[1],bigger[2]]

        cv2.line(img, (line[1][0], line[1][1]), (line[0][0], line[0][1]), (255, 255, 255), 1)
        cv2.line(canvas, (line[1][0], line[1][1]), (line[0][0], line[0][1]), (0, 0, 0), 1)
        image_output_1 = cv2.resize(img, (700, 700))
        image_output_2 = cv2.resize(canvas, (700, 700))    
        cv2.imshow('output_1', image_output_1)
        cv2.imshow('output_2', image_output_2)    
        cv2.waitKey(10)

        nextLine = findNextPoint(bigger);
        lines += 1;
        if lines >= lineQtd:
            break


def findNextPoint(line):
    index = 0
    for i in nail_positions:
        if( i.pos == line[2]):
            return index;
        index = index +1;
    

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
    crop = cv2.resize(crop,(700,700))
    return crop
    
    
    
    
# ===================================================== MAIN ============================================

tela = app.TelaPython()
[img, imagemPath] = tela.iniciar()



img = cutImage(img)
class Nail:
    def __init__(self,pos):
        self.pos = pos;
        self.lines = []


nail_positions = []
infor_nails = []
nailsQuantity = 200

canvas = createCanvas(img)
canvas = nailsCreate(canvas,nailsQuantity)
img = nailsCreate(img, nailsQuantity)
cv2.imwrite("etapaNails.png",img)
createInfor();

#print(nail_positions[0].pos," ",nail_positions[0].lines );
algorithmWeaver(2500);

fileSeparated = imagemPath.split("/")
nameFile = fileSeparated[len(fileSeparated) - 1]
cv2.imwrite("StringArt2_{}.png".format(nameFile),canvas)
    

            
    
        
