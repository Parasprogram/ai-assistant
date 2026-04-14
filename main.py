import speech_recognition as sr
import webbrowser
import pyttsx3
import music_library
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
import time

AUDIO_OK = True
try:
    pygame.mixer.init()
except Exception as e:
    AUDIO_OK = False
    print("Audio Init Error:", e)

engine = None
try:
    engine = pyttsx3.init('sapi5')
except Exception as e:
    print("TTS Init Error:", e)
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "1f843c7aa0324d108da548bee14dd215")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "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")


def fetch_top_headlines(api_key):
    url = "https://newsapi.org/v2/top-headlines"
    params = {"country": "us", "apiKey": api_key}
    headers = {"User-Agent": "ai-assistant/1.0"}

    # Ignore broken system proxy variables that can block outbound requests.
    session = requests.Session()
    session.trust_env = False
    return session.get(url, params=params, headers=headers, timeout=12)

def speak(text):
    if not text:
        return

    try:
        if not AUDIO_OK and engine is not None:
            engine.say(text)
            engine.runAndWait()
            return
        elif not AUDIO_OK:
            print(text)
            return

        filename = f"temp_{int(time.time())}.mp3"

        tts = gTTS(text=text, lang='en')
        tts.save(filename)

        print("Playing file:", filename)

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(1)

        pygame.mixer.music.unload()
        os.remove(filename)
        
    except Exception as e:
        print("Speech Error:", e)
        try:
            if engine is not None:
                engine.say(text)
                engine.runAndWait()
            else:
                print(text)
        except Exception:
            pass
    
def aiprocess(command):
    fallback_responses = {
        "hello": "Hello! I am here and listening.",
        "hi": "Hi! Tell me what you want me to do.",
        "how are you": "I am doing great and ready to help.",
        "who are you": "I am Jarvis, your voice assistant.",
        "thank you": "You're welcome.",
    }

    for key, value in fallback_responses.items():
        if key in command:
            return value

    try:
        if not OPENAI_API_KEY:
            return "I can do basic commands right now. Set OPENAI_API_KEY to enable full AI chat."

        client = OpenAI(api_key=OPENAI_API_KEY)
        completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role":"system","content":"you are the virtual assistant jarvis skilled in general task like alexa and google"},
            {"role":"user","content":command}
            ]
        )   
        return completion.choices[0].message.content
    except Exception as e:
        print("OpenAI Error:", e)
        return "I had trouble reaching AI service. I can still open websites, play songs, and read news."
    
def processcommand(c):
    
    c = c.lower()
    print("Command received:", c)
    
    if "open google" in c:
        webbrowser.open("http://google.com")
      
    elif "open linkedin" in c:
        webbrowser.open("http://www.linkedin.com")
        
    elif "open youtube" in c:
        webbrowser.open("http://www.youtube.com")  
        
    elif c.startswith("play"):
        song = c.replace("play ", "", 1).strip().lower()
        link = music_library.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak(f"I could not find {song} in your music library.")
        
        
    elif "news" in c:
        try:
            if not NEWS_API_KEY:
                speak("NEWS_API_KEY is not set.")
                return

            r = fetch_top_headlines(NEWS_API_KEY)
            r.raise_for_status()
            data = r.json()

            if data.get("status") != "ok":
                message = data.get("message", "Unknown News API error.")
                print("News API Error:", message)
                speak(f"News service error: {message}")
                return

            articles = data.get("articles", [])
            if not articles:
                speak("No headlines found right now.")
                return

            speak("Top headlines")

            print("Top Headlines:\n")

            for article in articles:
                title = article.get("title")
                if title:
                    speak(title)
                
        except Exception as e:
            print("News Error:", e)
            speak("Unable to fetch news")        
    else:
        output = aiprocess(c)
        speak(output)    
                 
    
if __name__=="__main__": 
    speak("initializing")    
        
    while True:
        r=sr.Recognizer()
        print("recognizing...")
        
        try:
            with sr.Microphone() as source:
                print("listening...")
                r.adjust_for_ambient_noise(source, duration=1)
                audio = r.listen(source, timeout=2, phrase_time_limit=2)

            word = r.recognize_google(audio)
            print("Heard:", word)

            if "jarvis" in word.lower():
                speak("ya") 
                with sr.Microphone() as source:
                    print("activated")
                    
                    r.adjust_for_ambient_noise(source, duration=2)
                    audio=r.listen(source) 
                command=r.recognize_google(audio)
                processcommand(command)
                
                
        except Exception as e:
            print("Error;{0}".format(e))  
