import PySimpleGUI as sg
from tkinter import filedialog
import cv2


def getBiggerSize(img):
    if(img.shape[0] < img.shape[1]):
        return img.shape[0]
    else:
        return img.shape[1]
    


    
def cutImage(img, initial):
    w = img.shape[0]
    h = img.shape[1]
    if(w == h):
        return img
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
            
            [sg.Text("Limiar Value: ", key="textLimiar", visible=False), sg.Text("W = 10000 H = 10000", key="textSizeImage", visible=False,font = 'arial')], 
            [sg.Slider(range=(0,255),default_value = 80, orientation='h', key="sliderLimiar",change_submits=True, visible=False)],
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
               
                
                
                self.janela["textLimiar"].update(visible=True)
                self.janela["sliderLimiar"].update(visible=True)
                self.janela["sliderCutWidth"].update(visible=True)
                self.janela["textSizeImage"].update(visible=True)
                
               
                text = "W = {} H = {}".format(imagem.shape[1],imagem.shape[0])
                self.janela["textSizeImage"].update(value = text)
                
                imagemCrop = cutImage(imagem,0)
                imagemBG = transformImageInBlackAndGray(imagem)
                
                imagem = putFilterBlackWhite(imagemBG, self.values["sliderLimiar"])
                imagem = cutImage(imagem,getBiggerSize(imagem))
                imagem = cv2.resize(imagem, (500,500))
                
                #Essa parte é pra resolver um bug
                imagem = putFilterBlackWhite(imagemBG, self.values["sliderLimiar"])
                imagem = cutImage(imagem,int(self.values["sliderCutWidth"]+1)) 
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

tela = TelaPython()
tela.iniciar()

print("done")
