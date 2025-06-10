import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from algorithms import *


global imagem
imagem = None
def inserirImagem():
    caminho = filedialog.askopenfilename(
        filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif *.bmp")]
    )
    
    if caminho:
        global imagem 
        imagem = Image.open(caminho) 
        imagem = redimensionar(imagem, 900, 900)
        imagemTk = ImageTk.PhotoImage(imagem)
        imagemLabel.config(image=imagemTk)
        imagemLabel.image = imagemTk 

def redimensionar(imagem, larguraMax, alturaMax):
    larguraOriginal, alturaOriginal = imagem.size
    proporcao = min(larguraMax / larguraOriginal, alturaMax / alturaOriginal)
    novaLargura = int(larguraOriginal * proporcao)
    novaAltura = int(alturaOriginal * proporcao)
    return imagem.resize((novaLargura, novaAltura), Image.Resampling.LANCZOS)

def sliderChange(valor):
    dropdownValue = dropdownBtn.get()
    if dropdownValue == "DWT (Transformada Wavelet Discreta)":
        #DWTCompression(channel, factor=2, wavelet='haar', threshHold=0.05)
        global imagem
        if imagem == None:
            return
        
        #Pegando o fator e o treshhold do slider
        fator = int(slider1.get())
        treshHold = 1 - ((1000 - (100 - int(slider2.get())))/1000)
        
        #Transformando a imagem pra ser legivel em CV
        imagemCV = np.array(imagem)
        imagemCV = cv.cvtColor(imagemCV, cv.COLOR_RGB2BGR)
        
        #Separando os canais
        Y, Cb, Cr = YCbCrImage(imagemCV)
        
        #Chamando a compressão DWT
        data = DWTCompression(Y, fator, 'haar', treshHold)
        
        #Reconstruindo a imagem com DWT reverso
        reconstructedImage = DWTDecompression(data[0], data[1], 'haar')
        
        #Separando os canais novamente
        Y2, Cb2, Cr2 = YCbCrImage(reconstructedImage)
        
        #Reconstruindo imagem com o canal luminanscia comprimido
        reconstructedImage = channelsResize(Y2, Cb, Cr, imagemCV.shape) 
        
        #Convertendo de volta para imagem
        imagemRgb = cv.cvtColor(reconstructedImage, cv.COLOR_BGR2RGB)
        imagemRgb = Image.fromarray(imagemRgb)
        
        #Redimensionando imagem para posicionar na tela
        imagemInput = redimensionar(imagemRgb, 900, 900)
        
        #Transformando em objeto TK
        imagemTk = ImageTk.PhotoImage(imagemInput)
        
        #Trocando imagem da label da imagem
        imagemLabel.config(image=imagemTk)
        imagemLabel.image = imagemTk 
        
        
    elif dropdownValue == "Opção 2":
        print("Opção 2")
    elif dropdownValue == "Opção 3":
        print("Opção 3")
    else:
        print("Nenhuma opção!")
        
root = tk.Tk()  
root.geometry("1280x960")
root.title("Janela Principal")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=5)
root.grid_rowconfigure(0, weight=1)
frameEsquerda = tk.Frame(root)
frameEsquerda.grid(column=0, sticky='nsew')
frameEsquerda.grid_columnconfigure(0, weight=1)

frameDiv = tk.Frame(frameEsquerda)
frameDiv.grid(column=0, pady=30)

frameDireita = tk.Frame(root, bg='green')
frameDireita.grid_columnconfigure(0, weight=1)
frameDireita.grid(row=0, column=1, sticky='nswe')

iconeInserir = Image.open("assets\\open-folder.png")
iconeInserir = iconeInserir.resize((24, 24))
iconeInserir = ImageTk.PhotoImage(iconeInserir)

btnInserir = tk.Button(frameDiv, image=iconeInserir, relief='flat', command=inserirImagem)
btnInserir.grid(row=0, padx=10, column=0, sticky='e')

values = ["DWT (Transformada Wavelet Discreta)", "Opção 2", "Opção 3"]
dropdownBtn = ttk.Combobox(frameDiv, values=values)
dropdownBtn.current(0)
dropdownBtn.grid(row=0, column=1, sticky='e')

imagemLabel = tk.Label(frameDireita)
imagemLabel.grid(row=0, column=0)

textLabel1 = tk.Label(frameDiv, text="Factor: ")
textLabel1.grid(row=1, column=0, sticky='ws')

slider1 = tk.Scale(frameDiv,
                from_=0, to=15,     # intervalo de valores
                orient="horizontal",  # ou "vertical"
                command=sliderChange)     # função chamada ao mover
slider1.grid(row=1, column=1, sticky='we')

textLabel2 = tk.Label(frameDiv, text="TreshHold: ")
textLabel2.grid(row=2, column=0, sticky='ws')

slider2 = tk.Scale(frameDiv,
                from_= 0, to=99,     # intervalo de valores
                orient="horizontal",  # ou "vertical"
                command=sliderChange)     # função chamada ao mover
slider2.grid(row=2, column=1, sticky='we')






root.mainloop()










