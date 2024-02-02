#  Python AI Virtual Desktop Assistant
# Python AI Virtual Desktop Assistant
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib


print("Initializing Eva")

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

Master = "Twisha"


def speak(text):
    engine.say(text)
    engine.runAndWait()


def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("Hello I am Eva and How are you? How may I help you?")


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Sorry, I didn't catch that.")
        query = None

    return query


def sendEmail(to, content):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login('hema.dashboard@gmail.com', 'Hema@1990')
    server.sendmail('suraj199208@gmail.com', to, content)
    server.close()


def main():
    speak("Initializing Eva")
    wishMe()
    query = takecommand()

    if 'wikipedia' in query.lower():
        speak('Searching Wikipedia....')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        print(results)
        speak(results)

    elif 'open youtube' in query.lower():
        url = "youtube.com"
        Chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(Chrome_path).open(url)

    elif 'google' in query.lower():
        url = "google.com"
        Chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(Chrome_path).open(url)

    elif 'play music on Wynk' in query.lower():
        url = "https://wynk.in"
        Chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe %s'
        webbrowser.get(Chrome_path).open(url)


    elif 'the time' in query.lower():
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"{Master}, the time is {strTime}")

    elif 'open code' in query.lower():
        codepath = "C:\\Users\\suraj\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Visual Studio Code\\Visual Studio Code.lnk"
        os.startfile(codepath)

    elif 'email' in query.lower():
        try:
            speak("What should I send")
            content = takecommand()
            to = 'hema.dashboard@gmail.com'
            sendEmail(to, content)
            speak("Email has been sent successfully")
        except Exception as e:
            print(e)


main()







                