import tkinter as tk
from tkinter import scrolledtext
from PIL import Image
import threading
import time
import sys
import speech_recognition as sr
import os
import webbrowser
from config import apikey
import datetime
import pyttsx3
import pywhatkit
import platform
import psutil
from datetime import datetime
import openai
import geocoder
import webbrowser
import threading
import time
from num2words import num2words
import pyautogui 
import speedtest
from keyboard import volumedown,volumeup
from try2 import say,chat,set_voice,change_voice,get_system_info,get_current_location,google_search_temperature,play_song,check_internet_speed,ai,open
# Initialize text-to-speech engine
engine = pyttsx3.init()
voice_id = 0

# Custom stream class to capture printed text dynamically
class DynamicTextStream:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        self.text_widget.configure(state='normal')
        self.text_widget.insert('end', text)
        self.text_widget.configure(state='disabled')
        self.text_widget.see('end')  # Scroll to the end to always show the latest text



# Function to start Jarvis
def start_jarvis():
    # Switch to loading GIF
    switch_gif("loading")
    # Set voice and say welcome message
    set_voice()
    print('Welcome to Jarvis A.I')
    say("Jarvis AI")
    # Simulate some processing time
    time.sleep(1.5)  # Simulate 3 seconds of processing
    switch_gif("happy")
    print('Jarvis A.I. has finished initializing.')    
    say("Finished Initializing and processing")
    say("What can i do for you")
    query = takeCommand().lower()
    if "system information".lower() in query.lower():
        system_info = get_system_info()
        for key, value in system_info.items():
            print(f'{key}: {value}')
            say(f'{key}: {value}')
    elif "open" in query:
           open(query)
    elif "time" in query:
                    hour = datetime.now().strftime("%H")
                    min = datetime.now().strftime("%M")
                    print(f"Sir time is {hour} and {min} minutes")
                    say(f"Sir time is {hour} and {min} minutes")
                
    elif "play" in query:
                    
                    play_song(query)

    elif "internet speed" in query:
                    check_internet_speed()

    elif "Using artificial intelligence".lower() in query.lower() or "using ai".lower() in query.lower():
                    ai(prompt=query)
    elif "change voice" in query or "switch voice" in query or "change your voice" in query or "switch your voice" in query:
                    change_voice()
    elif "temperature" in query:
                    google_search_temperature()

    elif "jarvis quit" in query.lower() or "jarvis exit" in query.lower():
                    print("Goodbye!")
                    say("Goodbye!")
                    exit()

    elif "reset chat".lower() in query.lower():
                    chatStr = ""
                


# Function to load and display GIF
def load_gif(gif_file, frames):
    photoimage_objects = []
    for i in range(frames):
        obj = tk.PhotoImage(file=gif_file, format=f"gif -index {i}")
        photoimage_objects.append(obj)
    return photoimage_objects

# Function to animate GIF
def animation(photoimages, loop_id):
    global current_loop_id
    current_loop_id = loop_id
    loop = [None]  # Use a mutable object to store loop variable

    def update_frame(current_frame=0):
        image = photoimages[current_frame]
        gif_label.configure(image=image)
        current_frame = (current_frame + 1) % len(photoimages)
        loop[0] = root.after(50, lambda: update_frame(current_frame))

    update_frame()
    return loop
def takeCommand():
    switch_gif("confused")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            if query == "":
                exit()
            print(f"User said: {query}")
            switch_gif("happy")
            return query
        except Exception as e:
            switch_gif("happy")
            return "Some Error Occurred. Sorry from Jarvis"
# Function to switch GIFs
def switch_gif(gif):
    global current_gif
    global current_loop_id
    current_gif = gif
    if current_loop_id:
        root.after_cancel(current_loop_id[0])  # Cancel the current animation loop
    if gif == "loading":
        current_loop_id = animation(loading_images, current_loop_id)
    elif gif == "sad":
        current_loop_id = animation(sad_images, current_loop_id)
    elif gif == "happy":
        current_loop_id = animation(happy_images, current_loop_id)
    elif gif == "confused":
        current_loop_id = animation(confused_images, current_loop_id)

# Function to stop animation
def stop_animation():
    if current_loop_id:
        root.after_cancel(current_loop_id[0])
    root.destroy()  # Close the window when animation stops

# Create the root window
root = tk.Tk()
root.title("Displaying Gif")

# Set fixed size for the GUI
root.geometry("800x550")

# Prevent resizing of the window
root.resizable(False, False)

# Set the background color to black
root.configure(bg="black")

# Load GIF files
loading_gif = "loading.gif"
sad_gif = "sad.gif"
happy_gif = "happy.gif"
confused_gif = "confused.gif"

loading_info = Image.open(loading_gif)
sad_info = Image.open(sad_gif)
happy_info = Image.open(happy_gif)
confused_info = Image.open(confused_gif)

# Extract number of frames for each GIF
loading_frames = loading_info.n_frames
sad_frames = sad_info.n_frames
happy_frames = happy_info.n_frames
confused_frames = confused_info.n_frames

loading_images = load_gif(loading_gif, loading_frames)
sad_images = load_gif(sad_gif, sad_frames)
happy_images = load_gif(happy_gif, happy_frames)
confused_images = load_gif(confused_gif, confused_frames)

# Create a frame to hold the GIF
gif_frame = tk.Frame(root, bg="black")  # Set background color of the frame
gif_frame.pack(side="left", fill="both", expand=True)

gif_label = tk.Label(gif_frame, bg="black", image="")  # Set background color of the label
gif_label.pack(fill="both", expand=True)

# Start with the loading GIF
current_gif = "loading"
current_loop_id = None
switch_gif(current_gif)

# Create a frame for the buttons and pack it to the right side
buttons_frame = tk.Frame(root, bg="black", width=150)  # Increase the width of the button frame
buttons_frame.pack(side="right", fill="y")

# Function to change button color on hover
def on_enter(event):
    event.widget.config(bg="#388E3C")  # Change button color on hover

# Function to change button color back on leaving
def on_leave(event):
    event.widget.config(bg="#4CAF50")  # Change button color back on leaving

# Buttons
button_style = {"bg": "#4CAF50", "fg": "white", "font": ("Arial", 12), "bd": 0, "activebackground": "#45a049"}

sad_button = tk.Button(buttons_frame, text="Sad", command=lambda: switch_gif("sad"), **button_style)
sad_button.pack(side="top", pady=(5), ipadx=10, ipady=5)
sad_button.bind("<Enter>", on_enter)
sad_button.bind("<Leave>", on_leave)

happy_button = tk.Button(buttons_frame, text="Happy", command=lambda: switch_gif("happy"), **button_style)
happy_button.pack(side="top", pady=5, ipadx=10, ipady=5)
happy_button.bind("<Enter>", on_enter)
happy_button.bind("<Leave>", on_leave)

confused_button = tk.Button(buttons_frame, text="Confused", command=lambda: switch_gif("confused"), **button_style)
confused_button.pack(side="top", pady=5, ipadx=10, ipady=5)
confused_button.bind("<Enter>", on_enter)
confused_button.bind("<Leave>", on_leave)

loading_button = tk.Button(buttons_frame, text="Loading", command=lambda: switch_gif("loading"), **button_style)
loading_button.pack(side="top", pady=5, ipadx=10, ipady=5)
loading_button.bind("<Enter>", on_enter)
loading_button.bind("<Leave>", on_leave)

# Button to start Jarvis
start_button = tk.Button(buttons_frame, text="Start Jarvis", command=lambda: threading.Thread(target=start_jarvis).start(), **button_style)
start_button.pack(side="top", pady=5, ipadx=10, ipady=5)
start_button.bind("<Enter>", on_enter)
start_button.bind("<Leave>", on_leave)

# Create a frame for the red box
red_box_frame = tk.Frame(buttons_frame, bg="black")
red_box_frame.pack(side="top", pady=45)

# Create a text widget for displaying text inside the red box
text_widget = scrolledtext.ScrolledText(red_box_frame, bg="black", fg="white", width=20, height=10, wrap='word', state='disabled', font=("Arial", 12))  # Adjust font and other properties
text_widget.pack(expand=True, fill='both')

# Redirect stdout to the custom stream for capturing dynamic text
sys.stdout = DynamicTextStream(text_widget)

# Close window when animation stops
root.protocol("WM_DELETE_WINDOW", stop_animation)

root.mainloop()
