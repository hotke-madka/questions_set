import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import re
import csv

class ImageDisplayApp:
    def __init__(self,master):
        self.master = master
        self.master.title("アンケート入力ツール")
        
        self.input_field = []
        self.image_paths = []
        self.original_images = []
        self.current_index = 0
        
        self.original_frame = tk.Frame(master)
        self.original_frame.pack(side="left",padx=10,pady=10)
        self.current_frame =tk.Frame(master)
        self.current_frame.pack(side="left",padx=10,pady=10)
        self.input_frame = tk.Frame(master)
        self.input_frame.pack(side="right",padx=10,pady=10)
        
        
        self.load_images()
        self.input_data(self.input_frame)
        
    def load_images(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            image_files = sorted([file for file in os.listdir(folder_path) if file.endswith((".jpg",".jpeg",".png"))])
            self.image_paths = [os.path.join(folder_path,file) for file in image_files]
            self.original_images  =[self.load_original_image(path) for path in self.image_paths]
            self.show_images()
    
    def load_original_image(self,image_path):
        original_filename = re.sub(r"_reg\d+","_original",os.path.basename(image_path))
        original_filepath = os.path.join(os.path.dirname(image_path),original_filename)
        if os.path.exists(original_filepath):
            original_image = Image.open(original_filepath)
            original_image = original_image.resize((300,300))
            original_photo = ImageTk.PhotoImage(original_image)
            return original_photo
        else:
            return None
    
    def show_images(self):
        if self.image_paths:
            current_image_path = self.image_paths[self.current_index]
            current_original_image = self.original_images[self.current_index]
            
            image = Image.open(current_image_path)
            image = image.resize((300,300))
            photo = ImageTk.PhotoImage(image)
            
            if hasattr(self,"image_label"):
                self.image_label.destroy()
            self.image_label =tk.Label(self.current_frame,image=photo)
            self.image_label.image = photo
            self.image_label.pack()
            
            if current_original_image:
                if hasattr(self,"original_rabel"):
                    self.orginal_label.destroy()
                self.original_label = tk.Label(self.original_frame,image=current_original_image)
                self.original_label.image =current_original_image
                self.original_label.pack()
            
            #self.update_input_field()
    
    def input_data(self,parent_frame):
        
        submit_btn = tk.Button(parent_frame,text="確定")
        submit_btn.pack()
        
        
        
        
def main():
    master = tk.Tk()
    app = ImageDisplayApp(master)
    master.mainloop()
    
if __name__ =="__main__":
    main()
    