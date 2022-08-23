#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 10:14:49 2020

@author: thierry
"""
from tkinter import *
import PIL.Image
from PIL import ImageTk


def Picture(enter_folder, path):
    image = PIL.Image.open(enter_folder.get() + path) 
    
    top = Toplevel()
    
    C = Canvas(top, width = image.size[0], height = image.size[1])
    filename = PhotoImage(file = enter_folder.get() + path)
    C.create_image(0,0, anchor = NW, image=filename)
    
    C.pack()
    
    top.mainloop()

