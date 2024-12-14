# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 12:37:29 2024

@author: Val Kyrvey Latoja
"""

import tkinter as tk
import tkinter.font as tkFont
from tkinter import Label
from PIL import Image, ImageTk
from io import BytesIO

def animation():
    global y_position, speed

    remaining_distance = target_y - y_position

    if abs(remaining_distance) > 1:
        speed = max(1, int(remaining_distance / 10))
        y_position += speed
        title.place(x=window_width//2 - title.winfo_width()//2, y=y_position)
        root.after(10, animation)

def fade_in_text(step=0):
    max_steps = 20
    r = g = b = int((1 - step / max_steps) * 255)
    color = f"#{r:02x}{g:02x}{b:02x}"
    open_button.config(fg=color)

    if step < max_steps:
        root.after(20, fade_in_text, step + 1)

def open_new_window():
    newwindow = tk.Toplevel(root)
    newwindow.title("Pokedex")
    newwindow_width = 600
    newwindow_height = 500
    newwindow.geometry(f"{newwindow_width}x{newwindow_height}")
    root.resizable(False, False)

    img = Image.open("logo.png")
    resized_image = img.resize((100, 100))
    new_image = ImageTk.PhotoImage(resized_image)
    newwindow.iconphoto(False, new_image)

    newwindow.mainloop()
    
root = tk.Tk()
root.title("Pokemon API")
window_width = 600
window_height = 500
root.geometry(f"{window_width}x{window_height}")
root.resizable(False, False)

img = Image.open("logo.png")
resized_image = img.resize((100, 100))
new_image = ImageTk.PhotoImage(resized_image)
root.iconphoto(False, new_image)

canvas = tk.Canvas(root, width=window_width, height=window_height)
canvas.pack(fill="both", expand=True)

canvas.create_rectangle(0, 0, window_width, window_height // 2, fill="#f54260", outline="")
canvas.create_rectangle(0, window_height // 2, window_width, window_height, fill="white", outline="")

black_bar_height = 10
canvas.create_rectangle(0, window_height // 2 - black_bar_height // 2, window_width, window_height // 2 + black_bar_height //2, fill="black", outline="")
font = tkFont.Font(family = "Agency FB", size = 50, weight = "bold")
button_font = tkFont.Font(family = "Agency FB", size = 25, weight = "bold")

button_radius = 60
button_x = window_width // 2
button_y = window_height // 2

canvas.create_oval(button_x - button_radius, button_y - button_radius, button_x + button_radius, button_y + button_radius, fill="white", outline="black", width=2)

title_text = "Pokedex"
title = tk.Label(root, text=title_text, font=font, fg="white", bg="#f54260")
title.update_idletasks()
title_width = title.winfo_width()

open_button = tk.Button(root, text="OPEN", font=button_font, width=6, height=1, bg="white", fg="black", relief="sunken", highlightthickness=0, bd=0, command=open_new_window)
open_button.place(x=button_x - 40, y=button_y - 30)

y_position = -300
target_y = window_height // 2 - 350 // 2
speed = 10

title.place(x=window_width // 2 - title.winfo_width() // 2, y=y_position)

fade_in_text()

animation()

root.mainloop()