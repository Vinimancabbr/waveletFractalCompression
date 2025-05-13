import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk

def selectImage():
    fileDir = filedialog.askopenfilename(
        title="Selecione uma imagem",
        filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif *.bmp")]
    )
    
    if fileDir:
        print(f"Selected Image: {fileDir}")
        image = Image.open(fileDir)
        image = image.resize((500, 500)) 
        imageTk = ImageTk.PhotoImage(image)
        return imageTk
    return None

def addImageBtnHandler(initialWindow):
    selectedImage = selectImage()
    if selectedImage:  
        imageLabel = tk.Label(initialWindow, image=selectedImage)
        imageLabel.image = selectedImage  
        imageLabel.pack()

def openInitialWindow():
    initialWindow = tk.Tk()   
    addImageBtn = tk.Button(
        initialWindow,
        text="Add Image",
        font=("Arial", 12, "bold"),
        command=lambda: addImageBtnHandler(initialWindow)
    )
    addImageBtn.pack()
    initialWindow.mainloop()

openInitialWindow()









