# Python AI Virtual Desktop Assistant
import pyttsx3
import speech_recognition as sr
import datetime
import time
import wikipedia
import webbrowser
import os
import smtplib
import cv2
import pywhatkit as kit
import pyautogui
import requests

print("Initializing Eva")

weather_api_key = '151ccc7ca90727802abcf0438fa8dccd'


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

Master = "Twisha"


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def takecommand():
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening....")
            r.pause_threshold = 1
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=10)
                print("Recognizing...")
                query = r.recognize_google(audio, language='en-in')
                print(f"User said: {query}\n")
                return query
            except sr.UnknownValueError:
                speak("Sorry, I didn't catch that. Could you please repeat?")
                continue
            except sr.RequestError as e:
                print(f"Error with the speech recognition service; {e}")
                speak("Sorry, there was an issue with the speech recognition service. Please try again later.")
                continue


def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("Hello I am Eva and How may I help you?")
    print("Hello I am Eva and How may I help you?")


def sendEmail(to, content):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login('hema.dashboard@gmail.com', 'Hema@1990')
    server.sendmail('hema.dashboard@gmail.com', to, content)
    server.close()

def select_voice():
    global engine
    voices = engine.getProperty('voices')

    print("Available voices:")
    for i, voice in enumerate(voices):
        print(f"{i + 1}. {voice.name}")

    voice_index = int(input("Enter the number corresponding to the voice you want to select: ")) - 1

    if 0 <= voice_index < len(voices):
        engine.setProperty('voice', voices[voice_index].id)
        print(f"Selected voice: {voices[voice_index].name}")
    else:
        print("Invalid voice index. Using the default voice.")

def get_horoscope(zodiac_sign):
    # Fetch today's horoscope for the given zodiac sign using the "aztro" API
    url = f'https://astrotalk.com/horoscope/daily-horoscope&day=today'
    response = requests.post(url)
    
    if response.status_code == 200:
        horoscope_data = response.json()
        return horoscope_data.get('description', 'Sorry, I could not fetch the horoscope for your sign.')
    else:
        return 'Sorry, there was an issue fetching the horoscope. Please try again later.'

def get_weather(city):
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'appid': weather_api_key,
        'units': 'metric',
    }

    try:
        response = requests.get(base_url, params=params)
        weather_data = response.json()

        if weather_data['cod'] == '404':
            return "City not found. Please provide a valid city name."

        main_weather = weather_data['weather'][0]['main']
        description = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']

        weather_info = f"The weather in {city} is {main_weather} ({description}). "
        weather_info += f"The temperature is {temperature}°C, and humidity is {humidity}%."
        return weather_info

    except Exception as e:
        print(f"Error fetching weather information: {e}")
        return "Sorry, I couldn't fetch the weather information at the moment."
    
def location_query():
    speak("Sure, please provide the city name or your current location.")
    city_name = takecommand()

    if 'current location' in city_name.lower():
        user_location = {'latitude': 28.6139, 'longitude': 77.2090}
        city_name = get_city_from_coordinates(user_location['latitude'], user_location['longitude'])

    weather_result = get_weather(city_name)
    speak(weather_result)

def get_city_from_coordinates(latitude, longitude):
    
    return "Delhi"

def set_reminder():
    
    speak("Got it. When should I remind you? Please provide the date and time.")
    reminder_datetime = takecommand()
    reminder_text= takecommand()

    # Logic to check if the day is Saturday or Sunday
    reminder_date = datetime.datetime.strptime(reminder_datetime, '%Y-%m-%d %H:%M:%S')
    if reminder_date.weekday() in [5, 6]:  # 5 is Saturday, 6 is Sunday
        speak("Sorry, reminders are not applicable on weekends.")
        return


    speak(f"Reminder set: {reminder_text} on {reminder_datetime}.")


    speak("Got it. When should I remind you? Please provide the date and time.")
    reminder_datetime = takecommand()

    speak(f"Reminder set: {reminder_text} on {reminder_datetime}.")

def view_reminders():
    
    reminders = ["Meeting at 11 AM", "Pick your daughter at 5 PM from day care"]
    if reminders:
        speak("Here are your reminders:")
        for reminder in reminders:
            speak(reminder)
    else:
        speak("You don't have any reminders.")

def delete_reminder():
    speak("Sure, what reminder would you like to delete?")
    reminder_text = takecommand()

    speak(f"Reminder '{reminder_text}' deleted.")

def handle_reminder_commands(query):
    if 'set reminder' in query.lower():
        set_reminder()

    elif 'view reminders' in query.lower():
        view_reminders()

    elif 'delete reminder' in query.lower():
        delete_reminder()


def main():
    wishMe()
    while True:
        query = takecommand()

        if 'wikipedia' in query.lower():
            speak('Searching Wikipedia....')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            print(results)
            speak(results)

        elif 'open notepad' in query.lower():
            npath = "C:\\Windows\\notepad.exe"
            os.startfile(npath)

        elif 'open camera' in query.lower():
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow('webcam', img)
                k = cv2.waitKey(50)
                if k == 27:
                    break
            cap.release()
            cv2.destroyAllWindows()

        elif 'open youtube' in query.lower():
            url = "youtube.com"
            Chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
            webbrowser.get(Chrome_path).open(url)

        elif 'open stackoverflow' in query.lower():
            webbrowser.open("www.stackoverflow.com")

        elif 'message' in query.lower():
            kit.sendwhatmsg("+91**********", 'testing message from virtual', datetime.datetime.now().hour,
                            datetime.datetime.now().minute + 2)

        elif 'google' in query.lower():
            url = "google.com"
            Chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
            webbrowser.get(Chrome_path).open(url)

        elif 'play song on youtube' in query.lower():
            kit.playonyt("chanda mamma ")

        elif 'the time' in query.lower():
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"{Master}, the time is {strTime}")

        elif 'open code' in query.lower():
            codepath = "C:\\Users\\suraj\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Visual Studio Code\\Visual Studio Code.lnk"
            os.startfile(codepath)

        elif 'email to hema' in query.lower():
            try:
                speak("What should I send")
                content = takecommand()
                to = 'hema.dashboard@gmail.com'
                sendEmail(to, content)
                speak("Email has been sent successfully")
            except Exception as e:
                print(e)
                speak("Sorry, I am unable to send the mail")

        elif "no thanks" in query.lower():
            speak("Thanks for using me, have a good day")

        elif "close notepad" in query.lower():
            speak('okay, closing notepad')
            os.system("taskkill /f /im notepad.exe")

        elif 'shut down the system' in query.lower():
            os.system("shutdown /s /t 5")

        elif 'restart the system' in query.lower():
            os.system("shutdown /r /t 5")

        elif 'switch the window' in query.lower():
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(2)
            pyautogui.keyUp('alt')

        elif 'set alarm' in query.lower():
            try:
                speak("What time should I set the alarm for? Please provide the time in HH:MM format.")
                alarm_time = takecommand()
                alarm_hour, alarm_minute = map(int, alarm_time.split(":"))
                now = datetime.datetime.now()
                alarm_datetime = datetime.datetime(now.year, now.month, now.day, alarm_hour, alarm_minute)

                time_difference = alarm_datetime - now
                time_seconds = time_difference.total_seconds()

                if time_seconds < 0:
                    speak("Sorry, the specified time has already passed.")
                    return
                speak(f"Alarm set for {alarm_time}")
                time.sleep(time_seconds)
                speak("Time to wake up!")

            except ValueError:
                speak("Invalid time format. Please provide the time in HH:MM format.")

        elif 'exit' in query.lower() or 'quit' in query.lower():
            speak("Goodbye!")
            break

        elif 'weather' in query.lower():
            speak("Sure, please provide the city name.")
            city_name = takecommand()
            weather_result = get_weather(city_name)
            speak(weather_result)

        elif 'reminder' in query.lower():
            handle_reminder_commands(query)
        
        elif 'horoscope' in query.lower():
            speak("Sure, please tell me your zodiac sign.")
            zodiac_sign = takecommand()
            horoscope_result = get_horoscope(zodiac_sign)
            speak(horoscope_result)

        elif 'horoscope all' in query.lower() or 'all zodiac signs' in query.lower():
            all_zodiac_signs = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']
            speak("Sure, here are today's horoscopes for all zodiac signs:")
            for sign in all_zodiac_signs:
                horoscope_result = get_horoscope(sign)
                speak(f"{sign.capitalize()}: {horoscope_result}")

        elif 'exit' in query.lower() or 'quit' in query.lower():
         break 

    else:
        speak("I'm sorry, I didn't understand that command. Can you please repeat?")


if __name__ == "__main__":
   main()