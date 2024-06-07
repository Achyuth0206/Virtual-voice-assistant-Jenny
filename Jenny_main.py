import os
import google.generativeai as genai
import speech_recognition
import pyttsx3
import pyautogui

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
rate = engine.setProperty("rate",170)

genai.configure(api_key=" Your API key")

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source, 0, 6)

    try:
        print("Understanding..")
        query = r.recognize_google(audio, language='en-in')
        print(f"You Said: {query}\n")
    except Exception as e:
        print("Say that again")
        return "None"
    return query

generation_config = {
  "temperature": 0.7,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 100,
  "response_mime_type": "text/plain",
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE",
  },
]

model = genai.GenerativeModel(
  model_name="gemini-1.0-pro",
  safety_settings=safety_settings,
  generation_config=generation_config,
)

messages = [
    {
        "parts": [
            {
                "text": "You are a Powerful AI Assistant Named Jenny. Hello, How are you?"
            }
        ],
        "role":"user"
    },
    {
        "parts":[
            {
                "text": "hello, I am doing well. How can I Help you?"
            }
        ],
        "role": "model"
    }
    ]


def Gemini(prompt):
    global messsages
    messages.append({
    "parts": [
        {
            "text": prompt
        }
    ],
    "role":"user"
    })

    response = model.generate_content(messages)

    messages.append({
        "parts":[
            {
                "text": response.text
            }
        ],
        "role": "model"
    })

    return response.text

def write_to_file(filename, content):
  with open(filename, "w") as f:
    f.write(content)

def handle_ai_request(prompt):
  # Extract the AI task and user question
  ai_task, question = prompt.split("for ", 1)

  # Generate response using the generative AI model
  response = Gemini(f"Using Artificial Intelligence, {ai_task} for {question}")

  # Create filename based on AI task and question
  filename = f"{ai_task}_{question.replace(' ', '_')}.txt"

  # Write the response (code) to a text file
  write_to_file(filename, response)

  return f"Using Artificial Intelligence, I created a file named '{filename}' containing the {ai_task}for{question}"
    

if __name__ == "__main__":
    while True:
        query = takeCommand().lower()
        if "go to sleep" in query:
            speak("Ok, You can call me anytime")
            break

        elif "using artificial intelligence" in query:
            response = handle_ai_request(query.split("using artificial intelligence ", 1)[1])
            print(response)
        
        elif "google" in query:
            from SearchNow import searchGoogle
            searchGoogle(query)

        elif "youtube" in query:
            from SearchNow import searchYoutube
            searchYoutube(query)

        elif "wikipedia" in query:
            from SearchNow import searchWikipedia
            searchWikipedia(query)

        # chrome automation
        elif 'open chrome' in query:
            os.startfile('C:\Program Files\Google\Chrome\Application\chrome.exe')
        elif 'create new tab' in query:
            pyautogui.hotkey('ctrl', 't')
        elif 'create new window' in query:
            pyautogui.hotkey('ctrl', 'n')
        elif 'create incognito window' in query:
            pyautogui.hotkey('ctrl', 'shift', 'n')
        elif 'minimise the window' in query:
            pyautogui.hotkey('super', 'down')
        elif 'open history' in query:
            pyautogui.hotkey('ctrl', 'h')
        elif 'open downloads' in query:
            pyautogui.hotkey('ctrl', 'j')
        elif 'previous tab' in query:
            pyautogui.hotkey('ctrl', 'shift', 'tab')
        elif 'next tab' in query:
            pyautogui.hotkey('ctrl', 'tab')
        elif 'close tab' in query:
            pyautogui.hotkey('ctrl', 'w')
        elif 'close window' in query:
            pyautogui.hotkey('ctrl', 'shift', 'w')
        elif 'close chrome' in query:
            os.system("taskkill /f /im chrome.exe")

        # youtube automation
        elif "pause" in query:
            pyautogui.press("k")
            speak("video paused")
        elif "play" in query:
            pyautogui.press("k")
            speak("video played")
        elif "mute" in query:
            pyautogui.press("m")
            speak("video muted")

        elif "volume up" in query:
            from keyboard import volumeup
            speak("Turning volume up")
            volumeup()
        elif "volume down" in query:
            from keyboard import volumedown
            speak("Turning volume down")
            volumedown()
        elif "next track" in query:
            pyautogui.hotkey('shift','n')                
        elif "previous track" in query:
            pyautogui.hotkey('alt','left')

        # open and close of apps
        elif "open" in query:
            query = query.replace("open", "")
            query = query.replace("jenny", "")
            pyautogui.press("super")
            pyautogui.typewrite(query)
            pyautogui.sleep(1)
            pyautogui.press("enter")

        elif "open" in query:
            from Dictapp import openappweb
            openappweb(query)

        elif "close" in query:
            from Dictapp import closeappweb
            closeappweb(query)

        elif "shut down the system" in query:
            os.system("shutdown /s /t 5")

        elif "restart the system" in query:
            os.system("shutdown /r /t 5")

        elif "Lock the system" in query:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

        else:
            prompt=query
            result=Gemini(prompt)
            speak(result)
            print(result)
        