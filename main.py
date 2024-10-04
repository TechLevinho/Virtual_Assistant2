import speech_recognition as sr
import datetime
import pyttsx3
import subprocess
import pywhatkit
import pyjokes
import webbrowser
import wikipedia
import smtplib
import requests
import os
import eel

eel.init("www")
os.system('start msedge.exe --app="http://localhost:8000/index.html"')
eel.start('index.html', mode=None, host='localhost',block=True)

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
recognizer = sr.Recognizer()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your Virtual Assistant. Please tell me how may I help you?")

def cmd():
    with sr.Microphone() as source:
        print('Clearing background noises..Please wait')
        recognizer.adjust_for_ambient_noise(source, duration=0.2)
        print('Ask me anything')
        recordedaudio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(recordedaudio, language='en_US')
        text = text.lower()
        print('Your message:', format(text))

        if 'chrome' in text:
            a = 'Opening chrome..'
            engine.say(a)
            engine.runAndWait()
            programName = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            subprocess.Popen([programName])

        elif 'time' in text:
            time = datetime.datetime.now().strftime('%I:%M %p')
            print(time)
            engine.say(time)
            engine.runAndWait()

        elif 'play' in text:
            a = 'Opening YouTube..'
            engine.say(a)
            engine.runAndWait()
            pywhatkit.playonyt(text)

        elif 'youtube' in text:
            b = 'Opening YouTube'
            engine.say(b)
            engine.runAndWait()
            webbrowser.open('www.youtube.com')

 

        elif 'weather' in text:
           
            city = 'New York'  
            api_key = '7b2e5f4365da4910bba132527240205'
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                temperature = data['main']['temp']
                weather_desc = data['weather'][0]['description']
                speak(f"The temperature in {city} is {temperature} degrees Celsius with {weather_desc}.")
            else:
                speak("Sorry, I couldn't retrieve the weather information at the moment. Please try again later.")


        elif 'reminder' in text:
            
            speak("What should I remind you about?")
            reminder_text = recognizer.recognize_google(recordedaudio, language='en_US')
    
    
            with open('reminders.txt', 'a') as f:
                f.write(reminder_text + '\n')
    
                speak(f"Okay, I will remind you to {reminder_text}")
    
        elif 'list' in text:
            print("Command to list reminders recognized")
            if os.path.exists('reminders.txt'):
                with open('reminders.txt', 'r') as f:
                    reminders = f.readlines()
            if reminders:
                speak("Here are your reminders:")
            for reminder in reminders:
                speak(reminder.strip())  
            else:
                speak("You don't have any reminders.")


        elif 'search' in text:
            
            query = text.replace('search', '').strip()
            result = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia:")
            speak(result)

        elif 'send email' in text:
            
            
            speak("Who is the recipient?")
            recipient = recognizer.recognize_google(recordedaudio, language='en_US')
            speak("What should I say?")
            content = recognizer.recognize_google(recordedaudio, language='en_US')
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            
            server.login('your_email@gmail.com', 'your_password')
            server.sendmail('your_email@gmail.com', recipient, content)
            server.close()
            speak("Email has been sent!")
            
        elif 'joke' in text:
         speak(pyjokes.get_joke())  

    except Exception as ex:
        print("An error occurred:", ex)

wishMe()  

while True:
    try:
        cmd()
    except KeyboardInterrupt:
        print("Program stopped by user")
        break
    except Exception as e:
        print("An error occurred:", e)