import PySimpleGUI as sg
from tkinter import filedialog
import cv2


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
          
            [sg.Text("Limiar Value: ", key="text")],
            [sg.Slider(range=(0,255),default_value = 0, orientation='h', key="sliderLimiar",change_submits=True)],
            [sg.Image(filename='', key='image')],
            [sg.Button('OK')]
            
        ]
        #Janela
        self.janela = sg.Window('String art', layout, finalize=True)
        
            
        
    def iniciar(self):
        imagemPath = filedialog.askopenfilename()
        imagem = cv2.imread(imagemPath, 1)
        imagemBG = transformImageInBlackAndGray(imagem)
    
        while True: 
            self.events,self.values = self.janela.Read()
           
             
            if(self.events == sg.WINDOW_CLOSED):
                break
            
            if(self.events == 'sliderLimiar'):
                imagem = cv2.threshold(imagemBG,self.values["sliderLimiar"], 255, cv2.THRESH_BINARY)[1]
                imgbytes = cv2.imencode('.png', imagem)[1].tobytes()  # ditto 
                self.janela["image"].update(data=imgbytes)
               
            if(self.events == 'OK'):
                return imagem
               
                
                
                
            
            
                
               
                
            
def qtdBlack(image):
    size = image.shape
    qtd = 0
    for i in range(0,size[0]):
        for y in range(0,size[1]):
            if(image.item(i,y) == 0):
                qtd += 1
    return qtd
    
print("done")