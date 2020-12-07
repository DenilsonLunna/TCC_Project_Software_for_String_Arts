import PySimpleGUI as sg

class TelaPython:
    def __init__(self):
        layout = [
            [sg.Text("Nome",size=(5,0)),sg.Input(size=(15,0),key=('nome'))],
            [sg.Text("Idade",size=(5,0)),sg.Input(size=(15,0),key=('idade'))],
            [sg.Text("Selecione seu e-mail")],
            [sg.Checkbox('Gmail',key=('gmail')), sg.Checkbox('Outlook',key=('outlook')), sg.Checkbox('Yahoo',key=('yahoo'))],
            [sg.Slider(range=(0,255),default_value = 0, orientation='h', size=(15,20), key="slider")],
            [sg.Button("clique",key=('button'))],
            [sg.Output(size = (30,20))]
           
        ]
        self.janela = sg.Window("Dados do usuario").layout(layout)
        
        
        
    def Iniciar(self):
        while True: 
            self.Slider,self.Button,self.value = self.janela.Read()
            nome = self.value['nome']
            idade = self.value['idade']
            aceita_gmail = self.value['gmail']
            aceita_outook = self.value['outlook']
            aceita_yahoo = self.value['yahoo']
            slider = self.value['slider']
            print(f'nome:{nome}')
            print(f'idade:{idade}')
            print(f'gmail{aceita_gmail}')
            print(f'outlook{aceita_outook}')
            print(f'yahoo{aceita_yahoo}')
            print(f'slider: {slider}')
            
        
tela = TelaPython()
tela.Iniciar();