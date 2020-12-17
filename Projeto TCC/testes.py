import cv2
from tkinter import filedialog


imagemPath = filedialog.askopenfilename()
imagem = cv2.imread(imagemPath, 1)


def printImage(image, time):
    cv2.imshow("imagem", image)
    key = cv2.waitKey(time)
    if key == 27:
        cv2.destroyAllWindows()
        return -1

def newCutImage(imagem):
    cv2.line(imagem, ((0, 0), (1200, 813), (255, 255, 255), 1)
    return imagem
    
def cutImage(imagem):
    y = imagem.shape[0]
    x = imagem.shape[1]
    yM = int(y/2)
    xM = int(x/2)

    print("total = {}, x = {}, y = {}, xM = {}, yM = {} ".format(
        imagem.shape, x, y, xM, yM))
    smaller = 0
    if(x < y):
        smaller = x
    else:
        smaller = y

    if(smaller == yM):
        initialPoint = yM - smaller
    else:
        initialPoint = xM - smaller

    tam = smaller*2

    crop = imagem[initialPoint:tam, initialPoint:tam]
    crop = cv2.resize(crop, (700, 700))
    return crop







imagem=newCutImage(imagem)
printImage(imagem, 10000)
