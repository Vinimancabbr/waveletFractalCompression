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
    global imagem
    if imagem == None:
        return
    
    #Transformando a imagem pra ser legivel em CV
    imagemCV = np.array(imagem)
    imagemCV = cv.cvtColor(imagemCV, cv.COLOR_RGB2BGR)
    
    #Separando os canais
    Y, Cb, Cr = YCbCrImage(imagemCV)
    dropdownValue = dropdownBtn.get()
    
    if dropdownValue == "DWT (Transformada Wavelet Discreta)":
        #DWTCompression(channel, factor=2, wavelet='haar', threshHold=0.05)
        #Pegando o fator e o treshhold do slider
        fator = int(slider1.get())
        treshHold = 1 - (int(slider2.get())/1000)

        #Chamando a compressão DWT
        data = DWTCompression(Y, fator, 'haar', treshHold)
        data1 = (data[0] * 100, data[1])
        coeffForDWT = Image.fromarray(data1[0])
        coeffForDWT = redimensionar(coeffForDWT, 300, 300)
        coeffForDWT = ImageTk.PhotoImage(coeffForDWT)
        subImagemLabel.config(image=coeffForDWT)
        subImagemLabel.image = coeffForDWT  
        #Reconstruindo a imagem com DWT reverso
        reconstructedImage = DWTDecompression(data[0], data[1], 'haar')
        
        #Separando os canais novamente
        Y2, Cb2, Cr2 = YCbCrImage(reconstructedImage)
        
        #Reconstruindo imagem com o canal luminanscia comprimido
        reconstructedImage = channelsResize(Y2, Cb, Cr, imagemCV.shape) 
        

        
    elif dropdownValue == "Opção 2":
        print("Opção 2")
    elif dropdownValue == "Subsample dos canais chroma":
        print("Opção 3")
        #subSampleChrominance(channel, factor)
        fator = int(slider1.get())
        print(fator)
        CbSampled = subSampleChrominance(Cb, fator)
        CrSampled = subSampleChrominance(Cr, fator)
        
        reconstructedImage = channelsResize(Y, CbSampled, CrSampled, imagemCV.shape)
    elif dropdownValue == "Downsample dos canais chroma":
        print("Opção 3")
        #subSampleChrominance(channel, factor)
        fator = int(slider1.get())
        print(fator)
        CbSampled = downSampleChrominance(Cb, fator)
        CrSampled = downSampleChrominance(Cr, fator)
        
        reconstructedImage = channelsResize(Y, CbSampled, CrSampled, imagemCV.shape)
    else:
        print("Nenhuma opção!")

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
        
    
root = tk.Tk()  
root.geometry("1280x960")
root.title("Janela Principal")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=5)
root.grid_rowconfigure(0, weight=1)
frameEsquerda = tk.Frame(root)
frameEsquerda.grid(column=0, sticky='nsew')
frameEsquerda.grid_columnconfigure(0, weight=1)



frameDireita = tk.Frame(root, bg='green')
frameDireita.grid_columnconfigure(0, weight=1)
frameDireita.grid(row=0, column=1, sticky='nswe')

iconeInserir = Image.open("assets\\openFolder.png")
iconeInserir = iconeInserir.resize((24, 24))
iconeInserir = ImageTk.PhotoImage(iconeInserir)

imagemLabel = tk.Label(frameDireita)
imagemLabel.grid(row=0, column=0)

frameDiv = tk.Frame(frameEsquerda)
frameDiv.grid(column=0, pady=30)

btnInserir = tk.Button(frameDiv, image=iconeInserir, relief='flat', command=inserirImagem)
btnInserir.grid(row=0, column=0, sticky='w')

values = ["DWT (Transformada Wavelet Discreta)", "Subsample dos canais chroma", "Downsample dos canais chroma"]
dropdownBtn = ttk.Combobox(frameDiv, values=values)
dropdownBtn.current(0)
dropdownBtn.grid(row=0, column=1, sticky='w')

titleLabel = tk.Label(frameDiv, text="DWT (Transformada Wavelet Discreta)", justify='left', font=("TkDefaultFont", 10))
titleLabel.grid(row=1, column=0, columnspan=2, sticky='w', pady=10)

textLabel = tk.Label(frameDiv, text="A Compressão de Imagens com DWT é uma técnica moderna e eficiente para"  
"reduzir o tamanho de imagens digitais, preservando a qualidade visual.  Quando a DWT  é aplicada em um canal" 
"de uma imagem, representamos a imagem original em um formato de multiresolução, onde separamos a base estrutural"  
"de uma imagem de seus detalhes finos e ruídos."
"\n\n\nFator é o valor responsável por determinar o número de iterações da decomposição DWT: ", wraplength=300, justify='left')
textLabel.grid(row=2, column=0, columnspan=2, sticky='we')

textLabelFactor = tk.Label(frameDiv, text="Factor: ")
textLabelFactor.grid(row=3, column=0, sticky='ws')

slider1 = tk.Scale(frameDiv,
                from_=1, to=100,     
                orient="horizontal",  
                command=sliderChange)     
slider1.grid(row=3, column=1, sticky='we')

subImagemLabel = tk.Label(frameDiv)
subImagemLabel.grid(row=4, column=0, columnspan=2, sticky='w')

textLabel2 = tk.Label(frameDiv, text="\n\nO treshhold determina qual a porcentagem de altas frequências serão descartadas: ", wraplength=300, justify='left')
textLabel2.grid(row=5, column=0, columnspan=2, sticky='w')


textLabelTreshhold = tk.Label(frameDiv, text="TreshHold: ")
textLabelTreshhold.grid(row=6, column=0, sticky='ws')

slider2 = tk.Scale(frameDiv,
                from_= 5, to=999,     
                orient="horizontal",  
                command=sliderChange)     
slider2.grid(row=6, column=1, sticky='we')

root.mainloop()










