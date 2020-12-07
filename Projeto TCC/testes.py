import cv2
import numpy as np
from tkinter import filedialog

def transformImageInBlackAndGray(imagem):
    return cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)


def putFilterBlackWhite(imagem, limiar):
    ret, imgT = cv2.threshold(imagem, limiar, 255, cv2.THRESH_BINARY)
    return imgT
def editImage(imagem, limiar):
    imagem = transformImageInBlackAndGray(imagem)
    imagem = putFilterBlackWhite(imagem, limiar)
    return imagem

def printImage(image, time):
    cv2.imshow("imagem", image)
    key = cv2.waitKey(time)
    if key == 27:
        cv2.destroyAllWindows()
        return -1
    
    
def saveImage(img, ind):
    cv2.imwrite("etapaNails{}.png".format(ind),img) 
    
    
    
limiar1 = 75
limiar2 = 150
limiar3 = 225 
    
    
    
imagemPath = filedialog.askopenfilename()
imagem = cv2.imread(imagemPath, 1)


img = editImage(imagem,limiar1)
saveImage(img,limiar1);
img = editImage(imagem,limiar2)
saveImage(img,limiar2);
img = editImage(imagem,limiar3)
saveImage(img,limiar3);

