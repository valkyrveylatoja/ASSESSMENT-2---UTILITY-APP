# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 12:37:29 2024

@author: Val Kyrvey Latoja
"""

import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
from io import BytesIO

root = tk.Tk()
root.title("Pokemon API")
root.geometry("600x500")
root.resizable(False, False)

img = Image.open("logo.png")
resized_image = img.resize((100, 100))
new_image = ImageTk.PhotoImage(resized_image)
root.iconphoto(False, new_image)


root.mainloop()