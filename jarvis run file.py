# Import necessary modules
import pyttsx3
import speech_recognition as sr
import datetime
import os
import webbrowser
import psutil
import pyjokes
import wikipedia
import time
import requests
from googlesearch import search
import openai

# Initialize pyttsx3 engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Initialize OpenAI API
openai.api_key = "" # add your api key here
client = openai.OpenAI(api_key=openai.api_key)

# Initialize speech recognition
recognizer = sr.Recognizer()

# Function to listen for user input
def listen():
    with sr.Microphone() as source:
        print("I am listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            data = recognizer.recognize_google(audio, language='en-in').lower()
            print("You said:", data)
            return data
        except sr.UnknownValueError:
            respond("Pardon me, please say that again")
        except sr.RequestError as e:
            respond("Request Failed due to network issues")
        return None

# Function to respond with speech
def respond(audioString):
    print(audioString)
    engine.say(audioString)
    engine.runAndWait()


def chat_with_jarvis(user_input):
    try:
        prompt_text = f"User: {user_input}\nJarvis:"
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt_text}],
            max_tokens=150
        )
        jarvis_response = response.choices[0].message.content
        print(f"Jarvis: {jarvis_response}")
        speak(jarvis_response)
    except Exception as e:
        print(f"An error occurred: {e}")
        respond("An error occurred, please try again.")


# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to get battery percentage
def get_battery():
    battery = psutil.sensors_battery()
    return battery.percent if battery else "Battery information not available"

# Function to get CPU usage
def get_cpu_usage():
    return psutil.cpu_percent()

# Function to get current weather
def get_weather():
    # Your weather API code here
    pass

def wishme():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        respond("Good Morning")
    elif 12 <= hour < 18:
        respond("Good Afternoon")
    else:
        respond("Good Evening")

# Function to handle digital assistant tasks
def digital_assistant(data):
    try:
        if "how are you" in data:
            respond("I am well")

        elif "time" in data:
            respond(datetime.datetime.now().ctime())

        elif any(word in data for word in ("who are you", "what can you do", "define yourself")):
            respond("I am Amal's personal assistant...")

        elif any(word in data for word in ("who made you", "who created you")):
            respond("I was built by Amal")

        elif "joke" in data:
            respond(pyjokes.get_joke())

        elif "shutdown" in data:
            respond("Are you sure you want to shutdown your computer?")
            confirmation = listen()
            if confirmation == "yes":
                os.system("shutdown /s /t 1")

        # Add more assistant tasks here...

        else:
            chat_with_jarvis(data)

    except Exception as e:
        print("An error occurred:", e)
        respond("An error occurred, please try again.")

# Main function
if __name__ == "__main__":
    respond("Checking remote servers!")
    respond("Importing preferences and loading all the system drivers!")
    respond("Establishing secure connection!")
    respond("Secure connection established!")
    respond("We are online!")
    respond("Welcome back sir!")
    wishme()
    respond("Jarvis is at your service")
    while True:
        respond("Please tell me how can I help you?")
        data = listen()
        if data is None:
            continue
        if any(word in data for word in ("stop listening", "ok bye", "stop", "exit")):
            respond("Good bye . Have a nice day")
            os.system("taskkill /f /im Rainmeter.exe")
            break
        digital_assistant(data)
        time.sleep(2)