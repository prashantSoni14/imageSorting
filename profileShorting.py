from tkinter import Message, PhotoImage, Tk, Text, BOTH, W, N, E, S
import tkinter
from tkinter.ttk import Frame, Button, Label, Style
import json
import pytest
import os, os.path
from PIL import ImageTk
import PIL.Image
import shutil
import sys

image_count = 0

def read_jason(file_path): # to read the appconfig.json file.
    with open(file_path, "r") as f:
        return json.load(f)

def file_validate_json(): # validation of Json file
    with pytest.raises(FileNotFoundError):
        read_jason(file_path="source/data/non_existing_file.json")

    with pytest.raises(json.decoder.JSONDecodeError):
        read_jason(file_path="source/data/sample_invalid.json")

def handle_exception(exception, value, traceback):
    print("Caught exception:", exception)

class CreateFrame(Frame): # class to created GUI.
    imgs = [] # list of image in directory

    def __init__(self): # inaciating Fram constructor and calling Image loading and class/].
        super().__init__()
        self.loadImageFiles()
        self.initUI()        
    
    def initUI(self): # Class constructor construct the GUI.

        self.file_json = read_jason("appsetting.json") # read the jason file.

        #print(file_json)
        #print(len(self.imgs))

        # Create master GUI and give title name.
        self.master.title("Image Sorthing")
        self.pack(fill=BOTH, expand=True)

        #define row and coulmbs, here we created 3 columbs and rows as per variable for jason file.
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(int(self.file_json["totalClass"])+5, weight=1)
        self.rowconfigure(int(self.file_json["totalClass"])+4, pad=7)

        # Top Left Label
        self.lbl1 = Label(self, text="Profile : "+ str(len(self.imgs))+" Image : "+ str(image_count+1))
        self.lbl1.grid(sticky=W, pady=4, padx=5)

        # Loading first image from folder.
        if len(self.imgs) != 0:
            photo = PhotoImage(file=str(self.imgs[0]))

            self.lbl2 = Label(self, image=photo)
            self.lbl2.grid(row=1, column=0, columnspan=2, rowspan=int(self.file_json["totalClass"])+3, padx=5, sticky=E+W+S+N)
            self.lbl2.photo = photo
        else:
            self.lbl2 = Label(self, text="No Image in Image Folder. add image in folder and restart the application.")
            self.lbl2.grid(row=1, column=0, columnspan=2, rowspan=int(self.file_json["totalClass"])+3, padx=5, sticky=E+W+S+N)

        self.abtn = Button(self, text="Forward >", command=self.forward)
        self.abtn.grid(row=1, column=3)

        self.cbtn = Button(self, text="Backword <", command=self.backward)
        self.cbtn.grid(row=2, column=3, pady=4)

        for i in range(int(self.file_json["totalClass"])):
            self.fbtn = Button(self, text=str(self.file_json["Class"+str(i+1)]), command=lambda x = i+1:self.copyFolder(x))
            self.fbtn.grid(row=i+4, column=3, pady=4)

        self.hbtn = Button(self, text="Help")
        self.hbtn.grid(row=int(self.file_json["totalClass"])+4, column=0, pady=5)

        self.obtn = Button(self, text="Close", command=self.quit)
        self.obtn.grid(row=int(self.file_json["totalClass"])+4, column=3)

    def loadImageFiles(self):
        config_name = 'Image'

        # determine if application is a script file or frozen exe
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        elif __file__:
            application_path = os.path.dirname(__file__)

        path = os.path.join(application_path, config_name)
        if not os.path.isdir(path):
            os.mkdir(path)
        
        #path_dir = os.path.dirname(os.path.abspath(__file__))
        #print(path_dir)
        #path = os.path.join(path_dir,"Image")
        #print(path)
        valid_image = [".bmp",".gif", ".jpg", ".png"]

        list_dir = os.listdir(path)
        if list_dir != 0:    
            for f in list_dir:
                ext = os.path.splitext(f)[1]
                if ext.lower() not in valid_image:
                    continue
                full_path=os.path.join(path, f)
                #print(full_path)
                self.imgs.append(full_path)

    def forward(self):
        #print("Forward")
        global image_count
                    
        if image_count < len(self.imgs)-1:
            image_count += 1
            photo = PhotoImage(file=str(self.imgs[image_count]))
            self.lbl2.configure(image=photo)
            self.lbl2.photo= photo
            self.lbl1.configure(text="Profile : "+ str(len(self.imgs))+" Image : "+ str(image_count+1))
        #print(image_count)

    def backward(self):
        #print("Backward")
        global image_count
            
        if image_count > 0:
            image_count -= 1
            photo = PhotoImage(file=str(self.imgs[image_count]))
            self.lbl2.configure(image=photo)
            self.lbl2.photo= photo
            self.lbl1.configure(text="Profile : "+ str(len(self.imgs))+" Image : "+ str(image_count-1))
        #print(image_count)
        

    def copyFolder(self, btnnumber):
        global image_count
        classVar = "sortedProfile\\"+self.file_json["Class"+str(btnnumber)]
        if not os.path.isdir(classVar):
            os.mkdir("sortedProfile")
            os.mkdir(classVar)
            #print(classVar)
        source_file = str(self.imgs[image_count])
        destination_file = source_file.replace("Image",str(classVar))
        dest = shutil.move(source_file, destination_file)
        #print(len(self.imgs))
        #print(image_count)
        #print(str(self.imgs[int(image_count)]))
        #print("******************")
        del self.imgs[int(image_count)]
        if len(self.imgs) != 0:
            photo = PhotoImage(file=str(self.imgs[image_count]))
            self.lbl2.configure(image=photo)
            self.lbl2.photo= photo
            self.lbl1.configure(text="Profile : "+ str(len(self.imgs))+" Image : "+ str(image_count+1))
        else:
            self.lbl2 = Label(self, text="No Image in Image Folder. add image in folder and restart the application.")
            self.lbl2.grid(row=1, column=0, columnspan=2, rowspan=int(self.file_json["totalClass"])+3, padx=5, sticky=E+W+S+N)
        
        
    def helpbtn(self):
        print()


def main():

    root = Tk()
    root.report_callback_exception=handle_exception
    root.geometry("550x450+300+300")
    app = CreateFrame()
    root.mainloop()


if __name__=='__main__':
    main()