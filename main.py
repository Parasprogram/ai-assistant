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

pygame.mixer.init()
recognizer=sr.Recognizer()
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
newsapi="1f843c7aa0324d108da548bee14dd215"

def speak(text):
    try:
        filename = f"temp_{int(time.time())}.mp3"

        tts = gTTS(text=text, lang='en')
        tts.save(filename)

        print("Playing file:", filename)

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.music.unload()
        os.remove(filename)
        
    except Exception as e:
        print("OpenAI Error:", e)
        return "Sorry, I could not process that."    
    
def aiprocess(command):
    try:
        client = OpenAI (api_key="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")
        completion = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role":"system","content":"you are the virtual assistant jarvis skilled in general task like alexa and google"},
            {"role":"user","content":command}
            ]
        )   

        return completion.output[0].message.content 
    except Exception as e:
        print("OpenAI Error:", e)
        return "Sorry, I could not process that."
    
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
        song = c.lower().replace("play ", "")
        link=music_library.music[song]
        webbrowser.open(music_library.music[song])   
        
        
    elif "news" in c.lower():
        try:
            r=requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=1f843c7aa0324d108da548bee14dd215") 
            r = requests.get(r)       
            data = r.json()

            articles = data.get["articles"]
            speak(" top headlines")

            print("Top Headlines:\n")

            for article in articles:
                speak( article["title"])
                
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
            with sr.Microphone(device_index=1) as source:
                print("listening...")
                r.adjust_for_ambient_noise(source, duration=1)
                audio = r.listen(source, timeout=3, phrase_time_limit=3)

            word = r.recognize_google(audio)
            print("Heard:", word)

            if "jarvis" in word.lower():
                speak("ya") 
                with sr.Microphone(device_index=1) as source:
                    print("activated")
                    
                    r.adjust_for_ambient_noise(source, duration=1)
                    audio=r.listen(source) 
                command=r.recognize_google(audio)
                processcommand(command)
                
                
        except Exception as e:
            print("Error;{0}".format(e))  