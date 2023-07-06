import speech_recognition as sr
import pyttsx3
import requests
from bs4 import BeautifulSoup

# Initialize the recognizer
r = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Initialize the to-do list
todo_list = []

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-US")
        print(f"User said: {query}")
    except Exception as e:
        print("Sorry, I didn't catch that. Could you please repeat?")
        return ""

    return query

def process_command(command):
    if "reminder" in command:
        # Handle reminder logic here
        set_reminder()
    elif "to-do list" in command:
        # Handle to-do list logic here
        speak("Yes, I can help you with that. Let's create a to-do list.")
        manage_todo_list()
    elif "what" or "when" or "which" or "how" in command:
        # Handle web search logic here
        query = command.replace("what" or "when" or "which" or "how", "").strip()
        search_web(query)
    elif "exit" in command:
        speak("Goodbye!")
        exit()
    else:
        speak("Sorry, I can't help with that at the moment.")

def set_reminder():
    speak("What would you like me to remind you about?")
    reminder = listen()

    if reminder:
        speak(f"Sure, I will remind you about {reminder}.")
        # Add logic to set the reminder here
    else:
        speak("Sorry, I didn't catch that. Could you please repeat?")

def manage_todo_list():
    while True:
        speak("What would you like to add to the to-do list?")
        item = listen()

        if item:
            todo_list.append(item)
            speak(f"Added '{item}' to the to-do list.")
        else:
            speak("Sorry, I didn't catch that. Could you please repeat?")

        speak("Do you want to add more items to the to-do list?")
        response = listen().lower()
        if "no" in response:
            speak("Okay, no more items will be added to the to-do list.")
            break

    if todo_list:
        speak("Here is your to-do list:")
        for i, item in enumerate(todo_list, start=1):
            speak(f"{i}. {item}")
    else:
        speak("Your to-do list is empty.")

def search_web(query):
    speak(f"Sure, I will search the web for '{query}'.")
    try:
        response = requests.get(f"https://www.google.com/search?q={query}")
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.select('.kno-rdesc span')

        if results:
            answer = results[0].text
            speak(f"According to the web, {answer}")
        else:
            speak("I'm sorry, I couldn't find any relevant information.")
    except:
        speak("I'm sorry, an error occurred while searching the web.")

# Main loop
while True:
    query = listen().lower()
    process_command(query)