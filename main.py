import speech_recognition as sr
import pyttsx3
import requests
import time

# Initialize the recognizer
r = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Initialize the to-do list
todo_list = []

# Define rate limiting parameters
REQUESTS_PER_MINUTE = 60  # Maximum number of requests allowed per minute
REQUESTS_INTERVAL = 60 / REQUESTS_PER_MINUTE  # Interval between each request (in seconds)
last_request_time = time.time()

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
    elif any(keyword in command for keyword in ["what", "when", "which", "how"]):
        # Handle ChatGPT API logic here
        query = command.strip()
        answer = get_answer_from_chatgpt(query)
        speak(answer)
    elif "exit" or "bye" in command:
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

def get_answer_from_chatgpt(query):
    global last_request_time

    # Check if cooldown period has passed since the last request
    current_time = time.time()
    elapsed_time = current_time - last_request_time
    if elapsed_time < REQUESTS_INTERVAL:
        wait_time = REQUESTS_INTERVAL - elapsed_time
        time.sleep(wait_time)

    # Make an API call to the ChatGPT endpoint with the user query
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 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"  # Replace with your API key
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": query}],
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()

    # Update the last request time
    last_request_time = time.time()

    # Extract and return the answer from the API response
    if "choices" in result and result["choices"]:
        answer = result["choices"][0]["message"]["content"]
        return answer
    else:
        return "I'm sorry, I couldn't find any relevant information."

# Main loop
while True:
    query = listen().lower()
    process_command(query)
