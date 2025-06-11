import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from algorithms import *
from fractal.fractal import *
from sys import getsizeof
global image
image = None

def addImage():
    path = filedialog.askopenfilename(
        filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif *.bmp")]
    )
    if path:
        global image 
        image = Image.open(path) 
        image = resize(image, 900, 900)
        imageTk = ImageTk.PhotoImage(image)
        imageLabel.config(image=imageTk)
        imageLabel.image = imageTk 

def resize(image, maxWidth, maxHeight):
    originalWidth, originalHeight = image.size
    aspectRatio = min(maxWidth / originalWidth, maxHeight / originalHeight)
    newWidth = int(originalWidth * aspectRatio)
    newHeight = int(originalHeight * aspectRatio)
    return image.resize((newWidth, newHeight), Image.Resampling.LANCZOS)

def cleanLeftColumn():
    global leftFrameColumn
    if leftFrameColumn:
        leftFrameColumn.destroy()
    leftFrameColumn = tk.Frame(leftFrame)
    leftFrameColumn.grid(column=0, row=1)
    leftFrameColumn.columnconfigure(1, weight=1)
def DWTLeftColumn():
    global leftFrameColumn
    global slider1
    global slider2
    global subImageLabel1
    
    slider1 = None
    slider2 = None
    subImageLabel1 = None

    cleanLeftColumn()
    
    titleLabel = tk.Label(leftFrameColumn, text="DWT (Transformada Wavelet Discreta)", justify='left', font=("TkDefaultFont", 10))
    titleLabel.grid(row=1, column=0, columnspan=2, sticky='w', pady=10)

    textLabel = tk.Label(leftFrameColumn, text="A Compressão de Imagens com DWT é uma técnica moderna e eficiente para"  
    "reduzir o tamanho de imagens digitais, preservando a qualidade visual.  Quando a DWT  é aplicada em um canal" 
    "de uma imagem, representamos a imagem original em um formato de multiresolução, onde separamos a base estrutural"  
    "de uma imagem de seus detalhes finos e ruídos, esses quais o olho humano tem dificuldade de observar detalhadamente."
    "\n\n\nFator é o valor responsável por determinar o número de iterações da decomposição DWT: ", wraplength=300, justify='left')
    textLabel.grid(row=2, column=0, columnspan=2, sticky='we')

    textLabelFactor = tk.Label(leftFrameColumn, text="Fator: ")
    textLabelFactor.grid(row=3, column=0, sticky='ws')
    
    slider1 = tk.Scale(leftFrameColumn,
                    from_=1, to=10,     
                    orient="horizontal",  
                    command=sliderChange)     
    slider1.grid(row=3, column=1, sticky='we')

    subImageLabel1 = tk.Label(leftFrameColumn)
    subImageLabel1.grid(row=4, column=0, columnspan=2, sticky='w')

    textLabel2 = tk.Label(leftFrameColumn, text="\n\nO treshhold determina qual a porcentagem de altas frequências serão descartadas: ", wraplength=300, justify='left')
    textLabel2.grid(row=5, column=0, columnspan=2, sticky='w')

    textLabelTreshhold = tk.Label(leftFrameColumn, text="TreshHold: ")
    textLabelTreshhold.grid(row=6, column=0, sticky='ws')

    slider2 = tk.Scale(leftFrameColumn,
                    from_= 5, to=999,     
                    orient="horizontal",  
                    command=sliderChange)     
    slider2.grid(row=6, column=1, sticky='we')

def SubsampleLeftColumn():
    global leftFrameColumn
    global slider1
    global slider2
    global subImageLabel1
    global subimageLabel2
    slider1 = None
    slider2 = None
    subImageLabel1 = None
    
    cleanLeftColumn()
    
    if leftFrameColumn:
        leftFrameColumn.destroy()
    leftFrameColumn = tk.Frame(leftFrame)
    leftFrameColumn.grid(column=0, row=1)
    leftFrameColumn.columnconfigure(1, weight=1)
    
    titleLabel = tk.Label(leftFrameColumn, text="Chroma Subsampling", justify='left', font=("TkDefaultFont", 10))
    titleLabel.grid(row=1, column=0, columnspan=2, sticky='w', pady=10)

    textLabel = tk.Label(leftFrameColumn, text="O subsampling dos canais chroma é uma tecnica de redução de tamanho de imagens."
                        "Após converter a imagem do espaço RGB"
                        "para um espaço YCbCr (Luminanscia, Chroma Azul, Chroma vermelho). Considerando que o olho humano é"
                        "pouco sensível a alterações dos canais de cor (CbCr), o"
                        "método de subsampling reduz o tamanho do canal, adotando o primeiro pixel como a cor original de"
                        "um grupo de pixels de grade fator por fator.", wraplength=300, justify='left')
    textLabel.grid(row=2, column=0, columnspan=2, sticky='we')

    textLabelFactor = tk.Label(leftFrameColumn, text="Fator: ")
    textLabelFactor.grid(row=3, column=0, sticky='ws')
    slider1 = tk.Scale(leftFrameColumn,
                    from_=2, to=100,     
                    orient="horizontal",  
                    command=sliderChange)     
    slider1.grid(row=3, column=1, sticky='we')

    subImageLabel1 = tk.Label(leftFrameColumn)
    subImageLabel1.grid(row=4, column=0, sticky='w')
    subimageLabel2 = tk.Label(leftFrameColumn)
    subimageLabel2.grid(row=4, column=1, sticky='w')

def downSampleLeftColumn():
    global leftFrameColumn
    global slider1
    global slider2
    global subImageLabel1
    global subimageLabel2
    slider1 = None
    slider2 = None
    subImageLabel1 = None
    
    cleanLeftColumn()
    
    if leftFrameColumn:
        leftFrameColumn.destroy()
    leftFrameColumn = tk.Frame(leftFrame)
    leftFrameColumn.grid(column=0, row=1)
    leftFrameColumn.columnconfigure(1, weight=1)
    
    titleLabel = tk.Label(leftFrameColumn, text="Chroma Downsampling", justify='left', font=("TkDefaultFont", 10))
    titleLabel.grid(row=1, column=0, columnspan=2, sticky='w', pady=10)

    textLabel = tk.Label(leftFrameColumn, text="O downSample dos canais chroma é uma tecnica de redução de tamanho de imagens."
                        "Após converter a imagem do espaço RGB"
                        "para um espaço YCbCr (Luminanscia, Chroma Azul, Chroma vermelho). Considerando que o olho humano é"
                        "pouco sensível a alterações dos canais de cor (CbCr), o"
                        "método de subsampling reduz o tamanho do canal, adotando o a média entre um grupo de pixels fator por fator como a"
                        "cor original desse grupo de pixels", wraplength=300, justify='left')
    textLabel.grid(row=2, column=0, columnspan=2, sticky='we')

    textLabelFactor = tk.Label(leftFrameColumn, text="Fator: ")
    textLabelFactor.grid(row=3, column=0, sticky='ws')
    slider1 = tk.Scale(leftFrameColumn,
                    from_=2, to=100,     
                    orient="horizontal",  
                    command=sliderChange)     
    slider1.grid(row=3, column=1, sticky='we')

    subImageLabel1 = tk.Label(leftFrameColumn)
    subImageLabel1.grid(row=4, column=0, sticky='w')
    subimageLabel2 = tk.Label(leftFrameColumn)
    subimageLabel2.grid(row=4, column=1, sticky='w')


def showLeftColumn(event=None):
    option = dropdownBtn.get()
    if option == "DWT (Transformada Wavelet Discreta)":
        DWTLeftColumn()
    elif option == "Subsample dos canais chroma":
        SubsampleLeftColumn()
    elif option == "Downsample dos canais chroma":
        downSampleLeftColumn()

def sliderChange(valor):
    global image
    if image == None:
        return
    
    #Transforming the image to visualization format
    imageCV = np.array(image)
    imageCV = cv.cvtColor(imageCV, cv.COLOR_RGB2BGR)
    
    #Dividing channels
    Y, Cb, Cr = YCbCrImage(imageCV)
    dropdownValue = dropdownBtn.get()
    
    if dropdownValue == "DWT (Transformada Wavelet Discreta)":
        #DWTCompression(channel, factor=2, wavelet='haar', threshHold=0.05)
        #Getting the factor and Treshold value
        factor = int(slider1.get())
        treshHold = 1 - (int(slider2.get())/1000)

        #Calling DWT compression method
        data = DWTCompression(Y, factor, 'haar', treshHold)
        getSerializedSize(data, "DWT Info:")
        getSerializedSize(image, "Image info:")
        '''print(
            f"Size of DWTCompressed file: {getsizeof(data)/1024:.3f} Kb\n"
            f"Size of original Image: {getsizeof(image)/1024:.3f} Kb"
        )'''
        
        data1 = (data[0] * 100, data[1])
        coeffForDWT = Image.fromarray(data1[0])
        coeffForDWT = resize(coeffForDWT, 300, 300)
        coeffForDWT = ImageTk.PhotoImage(coeffForDWT)
        subImageLabel1.config(image=coeffForDWT)
        subImageLabel1.image = coeffForDWT  
        
        #Rebuilding the original image using compressed data
        reconstructedImage = DWTDecompression(data[0], data[1], data[2])
        
        #Dividing channels again
        Y2, Cb2, Cr2 = YCbCrImage(reconstructedImage)
        
        #Rebuilding image with reduced luminansce size
        reconstructedImage = channelsResize(Y2, Cb, Cr, imageCV.shape) 
    
    elif dropdownValue == "Opção 2":
        print("Opção 2")
    elif dropdownValue == "Subsample dos canais chroma":
        #subSampleChrominance(channel, factor)
        factor = int(slider1.get())
        print(factor)
        CbSampled = subSampleChrominance(Cb, factor)
        CrSampled = subSampleChrominance(Cr, factor)
        altura, largura = CbSampled.shape
        
        r = np.full((altura, largura), 50, dtype=np.uint8)
        g = np.full((altura, largura), 50, dtype=np.uint8)
        b = CbSampled
        CbSampledBlueF = np.stack((r, g, b), axis=2)
        
        r = CrSampled
        g = np.full((altura, largura), 50, dtype=np.uint8)
        b = np.full((altura, largura), 50, dtype=np.uint8)
        CrSampledRedF = np.stack((r, g, b), axis=2)
        
        CbSampledImage = Image.fromarray(CbSampledBlueF)
        CrSampledImage = Image.fromarray(CrSampledRedF)
        
        CbSampledImage = resize(CbSampledImage, 150, 150)
        CrSampledImage = resize(CrSampledImage, 150, 150)
        
        CbSampledImage = ImageTk.PhotoImage(CbSampledImage)
        CrSampledImage = ImageTk.PhotoImage(CrSampledImage)
        
        subImageLabel1.config(image=CbSampledImage)
        subImageLabel1.image = CbSampledImage  
        
        subimageLabel2.config(image=CrSampledImage)
        subimageLabel2.image = CrSampledImage  
        
        reconstructedImage = channelsResize(Y, CbSampled, CrSampled, imageCV.shape)
    elif dropdownValue == "Downsample dos canais chroma":
        factor = int(slider1.get())
        print(factor)
        CbSampled = downSampleChrominance(Cb, factor)
        CrSampled = downSampleChrominance(Cr, factor)
        altura, largura = CbSampled.shape
        
        r = np.full((altura, largura), 50, dtype=np.uint8)
        g = np.full((altura, largura), 50, dtype=np.uint8)
        b = CbSampled
        CbSampledBlueF = np.stack((r, g, b), axis=2)
        
        r = CrSampled
        g = np.full((altura, largura), 50, dtype=np.uint8)
        b = np.full((altura, largura), 50, dtype=np.uint8)
        CrSampledRedF = np.stack((r, g, b), axis=2)
        
        CbSampledImage = Image.fromarray(CbSampledBlueF)
        CrSampledImage = Image.fromarray(CrSampledRedF)
        
        CbSampledImage = resize(CbSampledImage, 150, 150)
        CrSampledImage = resize(CrSampledImage, 150, 150)
        
        CbSampledImage = ImageTk.PhotoImage(CbSampledImage)
        CrSampledImage = ImageTk.PhotoImage(CrSampledImage)
        
        subImageLabel1.config(image=CbSampledImage)
        subImageLabel1.image = CbSampledImage  
        
        subimageLabel2.config(image=CrSampledImage)
        subimageLabel2.image = CrSampledImage  
        
        reconstructedImage = channelsResize(Y, CbSampled, CrSampled, imageCV.shape)
    else:
        print("Nenhuma opção!")

    #Transforming it back to RGB
    imageRgb = cv.cvtColor(reconstructedImage, cv.COLOR_BGR2RGB)
    imageRgb = Image.fromarray(imageRgb)
        
    #Resizing image to fit into the screen
    imageInput = resize(imageRgb, 900, 900)
        
    #Changing image type for TK visualization
    imageTk = ImageTk.PhotoImage(imageInput)
        
    #Changing the label image
    imageLabel.config(image=imageTk)
    imageLabel.image = imageTk    
        
    
root = tk.Tk()  
root.geometry("1280x960")
root.title("Janela Principal")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=5)
root.grid_rowconfigure(0, weight=1)
leftFrame = tk.Frame(root)
leftFrame.grid(column=0, sticky='nsew')
leftFrame.grid_columnconfigure(0, weight=1)

rightFrame = tk.Frame(root, bg='black')
rightFrame.grid_columnconfigure(0, weight=1)
rightFrame.grid(row=0, column=1, sticky='nswe')

addFileIcon = Image.open("waveletFractalCompression\\assets\\openFolder.png")
addFileIcon = addFileIcon.resize((24, 24))
addFileIcon = ImageTk.PhotoImage(addFileIcon)

imageLabel = tk.Label(rightFrame)
imageLabel.grid(row=0, column=0, pady=30)

frameDiv = tk.Frame(leftFrame)
frameDiv.grid(column=0, pady=30)

btnInserir = tk.Button(frameDiv, image=addFileIcon, relief='flat', command=addImage)
btnInserir.grid(row=0, column=0, sticky='w')

values = ["DWT (Transformada Wavelet Discreta)", "Subsample dos canais chroma", "Downsample dos canais chroma"]
dropdownBtn = ttk.Combobox(frameDiv, values=values)
dropdownBtn.current(0)
dropdownBtn.grid(row=0, column=1, sticky='w')
dropdownBtn.bind("<<ComboboxSelected>>", showLeftColumn)

global leftFrameColumn
leftFrameColumn = None

DWTLeftColumn()

root.mainloop()










