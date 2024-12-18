# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 12:37:29 2024

@author: Val Kyrvey Latoja
"""

import pygame
import requests
import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO

pygame.mixer.init()
music_file = "Pokemon Center - Tee Lopes.mp3"

def play_music(button):
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        button.config(text="MUSIC OFF")
    else:
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play(-1)
        button.config(text="MUSIC ON")
    
def on_closing():
    pygame.mixer.music.stop()
    root.destroy()
    newwindow.destroy()

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
    
    def getpokemondata():
        pokemon_name_or_id = pokemon_entry.get().strip().lower()
        
        if not pokemon_name_or_id:
            messagebox.showerror("Error", "Please enter a Pokemon name or ID")
            return
        try:
            response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name_or_id}")
            response.raise_for_status()
            
            data = response.json()
            name = data['name'].title()
            height = data['height']
            weight = data['weight']
            
            abilities = [ability['ability']['name'].title() for ability in data['abilities']]
            abilities_text = ", ".join(abilities)
            
            name_label.config(text=f"Name: {name}")
            height_label.config(text=f"Height: {height / 10} m")
            weight_label.config(text=f"Weight: {weight / 10} kg")
            abilities_label.config(text=f"Abilities: {abilities_text}")
            
            sprite_url = data['sprites']['front_default']
            if sprite_url:
                image_response = requests.get(sprite_url)
                image_response.raise_for_status()
                image_data = Image.open(BytesIO(image_response.content))
                image_data = image_data.resize((150, 150))
                
                global pokemon_image
                pokemon_image = ImageTk.PhotoImage(image_data)
                image_label.config(image=pokemon_image)
            else:
                messagebox.showinfo("Info", "No image available for this Pokemon.")
                
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to fetch data:\n{e}")
        except KeyError:
            messagebox.showerror("Error", "Invalid Pokemon name or ID. Please try again.")
    
    global newwindow
    newwindow = tk.Toplevel(root)
    newwindow.title("Pokedex")
    newwindow_width = 600
    newwindow_height = 500
    newwindow.geometry(f"{newwindow_width}x{newwindow_height}")
    newwindow.resizable(False, False)
    newwindow.configure(bg="white")
    # Configure the grid columns to expand
    newwindow.grid_columnconfigure(0, weight=1)
    newwindow.grid_columnconfigure(1, weight=1)
    newwindow.grid_columnconfigure(2, weight=1)

    # Header Section
    font = tkFont.Font(family="Agency FB", size=30, weight="bold")
    header = tk.Label(newwindow, text="Pokedex", bg="#f54260", fg="white", font=font, height=2)
    header.grid(row=0, column=0, columnspan=3, sticky="ew")  # Sticky 'ew' makes it stretch horizontally
    
    # Input Section
    font2 = tkFont.Font(family="Agency FB", size=20, weight="bold")
    input_label = tk.Label(newwindow, text="Enter Pokemon Name or ID:", font=font2, bg="white")
    pokemon_entry = tk.Entry(newwindow, font=font2, width=10, fg="white", bg="#f54260")
    fetch_button = tk.Button(newwindow, text="Enter", command=getpokemondata, font=font2, fg="white",bg="#f54260", width=10)
    
    input_label.grid(row=1, column=0, columnspan=2, pady=5, padx=10, sticky="w")
    pokemon_entry.grid(row=1, column=1, pady=5, padx=5, sticky="e")
    fetch_button.grid(row=1, column=2, columnspan=2, pady=10, padx=10)

    # Labels
    name_label = tk.Label(newwindow, text="Name: ", font=font2, bg="white")
    height_label = tk.Label(newwindow, text="Height: ", font=font2, bg="white")
    weight_label = tk.Label(newwindow, text="Weight: ", font=font2, bg="white")
    abilities_label = tk.Label(newwindow, text="Abilities: ", font=font2, wraplength=150, justify="left", bg="white")
    image_label = tk.Label(newwindow,bg="white")  # Image placeholder
    
    # Grid Placement
    name_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
    height_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)
    weight_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)
    abilities_label.grid(row=5, column=0, sticky="w", padx=10, pady=5)
    image_label.grid(row=2, column=2, rowspan=3, padx=10, pady=5)  # Occupies all rows in column 2
    
    
    # Music Button Animation
    start_y = 550
    end_y = 450

    def music_animate_button():
        def move_button():
            nonlocal y
            if y > end_y:
                step = max(1, (y - end_y) // 10)
                y -= step
                music_button.place(x=510, y=y)
                newwindow.after(10, move_button)
                
        y = start_y
        move_button()
    
    button_font2 = tkFont.Font(family="Agency FB", size=15, weight="bold")
    music_button = tk.Button(newwindow, text="MUSIC OFF", font=button_font2, command=lambda: play_music(music_button),fg="white",bg="#f54260")
    music_button.place(x=510, y=start_y)  # Start outside window
    
    newwindow.protocol("WM_DELETE_WINDOW", on_closing)
    music_animate_button()
    
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

title_text = "Pokemon API"
title = tk.Label(root, text=title_text, font=font, fg="white", bg="#f54260")
title.update_idletasks()
title_width = title.winfo_width()

open_button = tk.Button(root, text="OPEN", font=button_font, width=6, height=1, bg="white", fg="black", relief="sunken", highlightthickness=0, bd=0, command=open_new_window)
open_button.place(x=button_x - 40, y=button_y - 30)

y_position = -300
target_y = window_height // 2 - 350 // 2
speed = 10

title.place(x=window_width // 2 - title.winfo_width() // 2, y=y_position)

root.protocol("WM_DELETE_WINDOW", on_closing)

fade_in_text()

animation()

root.mainloop()