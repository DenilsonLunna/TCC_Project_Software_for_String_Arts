import PySimpleGUI as sg
from tkinter import filedialog
import cv2



#function to crop image
#Parameters: image to crop, contour, and the image number
def crop(image, contours, num):
    idNum = 0
    #cycles through all the contours to crop all
    for c in contours:
    #creates an approximate rectangle around contour
        x,y,w,h = cv2.boundingRect(image)
        # Only crop decently large rectangles
        if w>50 and h>50:
            idNum+=1
            #pulls crop out of the image based on dimensions
            new_img=image[y:y+h,x:x+w]
            #writes the new file in the Crops folder
#returns a number incremented up for the next file name
    return num+1
    
def cutImage(img, initial):
    w = img.shape[0]
    h = img.shape[1]
    
    if(h > w):
        img = img[0:initial+w,initial:initial+w]
    else:
        img = img[initial:initial+h,0:initial+h]
    
    return img
    

def printImage(image, time):
    cv2.imshow("imagem", image)
    key = cv2.waitKey(time)
    if key == 27:
        cv2.destroyAllWindows()
        return -1


def transformImageInBlackAndGray(imagem):
    return cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)


def putFilterBlackWhite(imagem, limiar):
    ret,imgT = cv2.threshold(imagem, limiar, 255, cv2.THRESH_BINARY)
    return imgT

def editImage(imagem, limiar):
    imagem = transformImageInBlackAndGray(imagem)
    #imagem = putFilterBlackWhite(imagem, limiar)
    return imagem

class TelaPython():
    def __init__(self):
        #Layout
        layout = [
            [sg.Button('Load image', key="loadImage")],
            
            [sg.Text("Limiar Value: ", key="textLimiar", visible=False), sg.Text("", key="textSizeImage", visible=True), 
             sg.Slider(range=(0,255),default_value = 80, orientation='h', key="sliderLimiar",change_submits=True, visible=False)],
            [sg.Text("Adjust Image: ", visible=True)], [sg.Slider(range=(0,255),default_value =0, orientation='h', key="sliderCutWidth",change_submits=True, visible=False)],  
            [sg.Image(filename='', key='image')],   
            [sg.Button('OK')]
            
        ]
        #Janela
        self.janela = sg.Window('String art', layout, finalize=True)
        
            
    def iniciar(self):
        
        while True: 
            self.events,self.values = self.janela.Read()
            if(self.events== "loadImage"):
                imagemPath = filedialog.askopenfilename()
                imagem = cv2.imread(imagemPath, 1)
                #logica para corte da imagem
                
                
                self.janela["textLimiar"].update(visible=True)
                self.janela["sliderLimiar"].update(visible=True)
                self.janela["sliderCutWidth"].update(visible=True)
                
                
               
                text = "Image Size = Width = {} Height = {}".format(imagem.shape[0],imagem.shape[1])
                self.janela["textSizeImage"].update(value = text)
                
                imagemCrop = cutImage(imagem,0)
                imagemBG = transformImageInBlackAndGray(imagem)
                imagem = cutImage(imagem,500)
                imagem = putFilterBlackWhite(imagemBG, self.values["sliderLimiar"])
                imagem = cv2.resize(imagem, (500,500))  
                 
                imgbytes = cv2.imencode('.png', imagemBG)[1].tobytes()  # ditto 
                self.janela["image"].update(data=imgbytes)
                
                
             
            if(self.events == sg.WINDOW_CLOSED):
                break
            
            if(self.events == 'sliderLimiar'):
                imagem = putFilterBlackWhite(imagemBG, self.values["sliderLimiar"])
                imagem = cutImage(imagem,int(self.values["sliderCutWidth"]))
                imagem = cv2.resize(imagem, (500,500))  
                
            if(self.events == 'OK'):
                return [imagem, imagemPath]
               
            if(self.events == "sliderCutWidth"):
                imagem = putFilterBlackWhite(imagemBG, self.values["sliderLimiar"])
                imagem = cutImage(imagem,int(self.values["sliderCutWidth"])) 
                imagem = cv2.resize(imagem, (500,500)) 
            
            imgbytes = cv2.imencode('.png', imagem)[1].tobytes()  # ditto 
            self.janela["image"].update(data=imgbytes)  
              
            
            
                
               
                
            
def qtdBlack(image):
    size = image.shape
    qtd = 0
    for i in range(0,size[0]):
        for y in range(0,size[1]):
            if(image.item(i,y) == 0):
                qtd += 1
    return qtd

#tela = TelaPython()
#tela.iniciar()

print("done")
