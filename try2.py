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
# Initialize text-to-speech engine
engine = pyttsx3.init()
voice_id = 0

openai.api_key = apikey
chatStr = ""
def chat(query):
    global chatStr
    models = ["gpt-3.5-turbo", "gpt-3.5-turbo-0301", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-1106", "gpt-3.5-turbo-16k"]
    
    while True:
        current_second = datetime.now().second
        model_index = current_second % len(models)  
        client = openai.ChatCompletion.create(
            model=models[model_index],
            messages=[{"role": "system", "content": "Please act as an AI assistant named Jarvis created by 'JADHAV AVINASH'. Listen and respond to user commands and inquiries in a helpful and efficient manner. Perform tasks such as setting reminders, answering questions, providing information, and executing basic tasks. Use a friendly and professional tone throughout."}, {"role": "user", "content": query}],
            temperature=0.7,
            max_tokens=450,
            n=1,
            stop=""
        )
        
        response = client.choices[0].message
        chatStr += f"Avinash: {query}\n Jarvis: {response['content']}\n"

        try:
            print(response['content'])
        except UnicodeEncodeError:
            print("Unable to print the content due to encoding issues.")
        
        say(response['content'])

        # Check if user wants to continue or exit
        user_input = takeCommand()
        exit_keywords = ['exit', 'quit', 'quit Jarvis', 'exit Jarvis','Jarvis exit','Jarvis quit']

        if any(keyword in user_input for keyword in exit_keywords):
            break
        # Get the user's next query
        query = user_input

    return chatStr


def say(text):    
    engine.say(text)
    engine.runAndWait()

# Set the voice based on the initial voice_id
def set_voice():
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_id].id)

# Change the voice and set it
def change_voice():
    global voice_id
    voice_id = (voice_id + 1) % 2  # Toggle between 0 and 1
    set_voice()
    say("Voice changed.")

# Function to get system information
def get_system_info():
    system_info = {
        'System': platform.system(),
        'Node Name': platform.node(),
        'Release': platform.release(),
        'Version': platform.version(),
        'Machine': platform.machine(),
        'Processor': platform.processor()
    }

    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()

    system_info['CPU Usage'] = f'{cpu_usage}%'
    system_info['Total Memory'] = f'{round(memory_info.total / (1024 ** 3), 2)} GB'
    system_info['Available Memory'] = f'{round(memory_info.available / (1024 ** 3), 2)} GB'
    system_info['Used Memory'] = f'{round(memory_info.used / (1024 ** 3), 2)} GB'
    system_info['Memory Usage'] = f'{memory_info.percent}%'

    return system_info 

def get_current_location():
    # Get your current location based on IP address
    location = geocoder.ip('me')

    # Access city and country information
    city = location.city
    country = location.country

    return city, country
def google_search_temperature():
    # Get current location
    city, country = get_current_location()
   
    # Construct a Google search query for the current temperature
    search_query = f"temperature in {city}, {country}"

    # Open the default web browser with the Google search query
    webbrowser.open(f"https://www.google.com/search?q={search_query}")
def play_song(query):
    song = query.replace('play', "")
    say("playing " + song)
    pywhatkit.playonyt(song)
    while True:
        query = takeCommand().lower()
        if "pause" in query or "stop" in query:
            pyautogui.press("k")
            say("video paused")
        elif any(keyword in query for keyword in ["on", "start", "play"]):
            pyautogui.press("k")
            say("video played")
        elif "mute" in query:
            pyautogui.press("m")
            say("video muted")
        elif "unmute" in query:
            pyautogui.press("m")
            say("video unmuted")
        elif "volume up" in query:
            say("Turning volume up, sir")
            volumeup()
        elif "volume down" in query:
            say("Turning volume down, sir")
            volumedown()
        elif "skip backward" in query or "back" in query:
            pyautogui.press("left") 
            pyautogui.press("left") 
            say("Skipping backward by 10 seconds")
        # Add other playback control conditions here
        elif "skip more" in query:
            for _ in range(10):
                pyautogui.press("right")  # Simulate right arrow key to skip forward
                say("Skipping forward")
        elif "skip forward" in query or "forward" in query or "skip" in query:
            pyautogui.press("right")
            pyautogui.press("right")  # Simulate right arrow key to skip forward
            say("Skipping forward by 10 seconds")    
   
        elif "close tab" in query or "close the tab" in query:
            pyautogui.hotkey("ctrl", "w")
            say("Closing the current tab")
            break
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            if query == "":
                exit()
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Jarvis"
def check_internet_speed():
    say("calculating internet speed")
    print("calculating internet speed...please wait!")
    wifi = speedtest.Speedtest()
    upload_net = wifi.upload() / 1048576
    download_net = wifi.download() / 1048576
    print("Wifi Upload Speed is", upload_net)
    print("Wifi download speed is ", download_net)
    say(f"Wifi Upload speed is {upload_net}")
    say(f"Wifi download speed is {download_net}")


def ai(prompt):
    global chatStr
    models = ["gpt-3.5-turbo", "gpt-3.5-turbo-0301", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-1106", "gpt-3.5-turbo-16k"]
    
    current_second = datetime.now().second
    model_index = current_second % len(models)  
    client = openai.ChatCompletion.create(
        model=models[model_index],
        messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=450,
        n=1,
        stop=""
    )
    
    response = client.choices[0].message
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"
    text += response['content']
    prompt = prompt.replace("artificial intelligence", "ai")
    print("Writing...")
    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    with open(f"Openai/{''.join(prompt.split('ai')[1:]).strip()}.txt", "w") as f:
        f.write(text)




    
def open(query):
                    sites = [
                        ["google", "https://www.google.com"],
                        ["youtube", "https://www.youtube.com"],
                        ["facebook", "https://www.facebook.com"],
                        ["whatsapp", "https://www.whatsapp.com"],
                        ["instagram", "https://www.instagram.com"],
                        ["cricbuzz", "https://www.cricbuzz.com"],
                        ["gaana", "https://gaana.com"],
                        ["hotstar", "https://www.hotstar.com"],
                        ["bookmyshow", "https://www.bookmyshow.com"],
                        ["makemytrip", "https://www.makemytrip.com"],
                        ["zomato", "https://www.zomato.com"],
                        ["swiggy", "https://www.swiggy.com"],
                        ["phonepe", "https://www.phonepe.com"],
                        ["paytm", "https://paytm.com"],
                        ["chatgpt", "https://www.chatbot.com"],
                        ["stackoverflow", "https://stackoverflow.com"],
                        ["spotify", "https://www.spotify.com"],
                        ["github", "https://www.github.com"],
                        ["google maps", "https://www.google.com/maps"],
                        ["duckduckgo", "https://duckduckgo.com"],
                        ["linkedin", "https://www.linkedin.com"],
                        ["reddit", "https://www.reddit.com"],
                        ["netflix", "https://www.netflix.com"],
                        ["ebay", "https://www.ebay.com"],
                        ["microsoft", "https://www.microsoft.com"],
                        ["apple", "https://www.apple.com"],
                        ["pinterest", "https://www.pinterest.com"],
                        ["yandex", "https://www.yandex.ru"],
                        ["bing", "https://www.bing.com"],
                        ["aliexpress", "https://www.aliexpress.com"],
                        ["zoom", "https://www.zoom.us"],
                        ["wordpress", "https://www.wordpress.com"],
                        ["snapchat", "https://www.snapchat.com"],
                        ["weather", "https://www.weather.com"],
                        ["craigslist", "https://www.craigslist.org"],
                    ]
                    for site in sites:
                        if f"Open {site[0]}".lower() in query.lower():
                            say(f"Opening {site[0]} sir...")
                            webbrowser.open(site[1])
                    if "open music" in query:
                        musicPath = "/Users/harry/Downloads/downfall-21371.mp3"
                        os.system(f"open {musicPath}")

                    elif "open camera".lower() in query.lower():
                        print("Try to open camera")
                        if platform.system() == "Windows":
                            webbrowser.open("microsoft.windows.camera:")
                            print("Camera opened")
                            say("Camera opened")

                    

                    elif "open files explorer".lower() in query.lower() or "open files" in query:
                        print("Try to open File Explorer")
                        if platform.system() == "Windows":
                            os.system("start explorer")
                            print("File Explorer opened")
                            say("File Explorer opened")

                    

                    elif "open calculator".lower() in query.lower():
                        print("Try to open Calculator")
                        if platform.system() == "Windows":
                            os.system("start calc")
                            print("Calculator opened")
                            say("Calculator opened")

                    elif "open command prompt".lower() in query.lower():
                        print("Try to open Command Prompt")
                        if platform.system() == "Windows":
                            os.system("start cmd")
                            print("Command Prompt opened")
                            say("Command Prompt opened")
                    

                    elif ("open anaconda navigator".lower() in query.lower() or "open anaconda".lower() in query.lower()) and "open anaconda promt" not in query.lower():

                        print("Try to open Anaconda Navigator")
                        if platform.system() == "Windows":
                            os.system("start anaconda-navigator")
                            print("Anaconda Navigator opened")
                            say("Anaconda Navigator opened")
                    

                    elif "open chrome".lower() in query.lower():
                        print("Try to open Chrome")
                        if platform.system() == "Windows":
                            os.system("start chrome")
                            print("Chrome opened")
                            say("Chrome opened")
                    

                    elif "open vscode".lower() in query.lower():
                        print("Try to open Visual Studio Code")
                        if platform.system() == "Windows":
                            os.system("code")
                            print("Visual Studio Code opened")
                            say("Visual Studio Code opened")

                    elif "open browser".lower() in query.lower():
                        print("Try to open default browser")
                        if platform.system() == "Windows":
                            webbrowser.open("http://www.google.com")
                            print("Browser opened")
                            say("Default browser opened")
                   
                    elif "open" in query:   
                        query = query.replace("open","")
                        query = query.replace("jarvis","")
                        pyautogui.press("super")
                        pyautogui.typewrite(query)
                        pyautogui.sleep(7)
                        pyautogui.press("enter")       
