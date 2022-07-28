import cProfile
import codeop
from sqlite3 import connect
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[0].id)
engine.setProperty('voices', voices[0].id)


def speak(audio):
    '''
    This function is used for speak
    '''
    engine.setProperty("rate", 172)
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    '''
    This function will greet
    '''
    hour = int(datetime.datetime.now().hour)
    if hour >=0 and hour <=12:
        print("Good Morning!")
        speak("Good Morning!")
    elif hour >=12 and hour <=18:
        print("Good Afternoon!")
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    print("I'm Jarvis. PLease tell me how may I help you?")
    speak("I'm Jarvis. PLease tell me how may I help you?")
# def sendEmail(to, content):  #we will be using smtplib, a preinstalled library used to send emails
#     #And we have to use "less secure apps" on gmail. Google does not supports this
#     with open('/python-projects/log_pass.txt', 'r') as f:
#         password = f.read()
#     server = smtplib.SMTP('smntp.gmail.com', 500)
#     server.ehlo()
#     server.starttls()
#     server.login(f'iamjervis0000@gmail.com', '{password}')
#     server.sendmail('iamjervis0000@gmail.com', to, content)
#     server.close()


def takeCommand():
    '''
    This function will recognise our speech and returning as a text string
    '''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Listening....")
        sr.energy_threshold = 300
        r.pause_threshold = 0.8 #Time taken tom complete a phrase as second.
        audio = r.listen(source)
    
    print("Recognising...")
    speak("Recognising")
    query = r.recognize_google(audio)
    print(f"Command: {query}\n")
    return query
    # except Exception as e:
    #     print(e)
    #     print("Say that again please...")
    #     speak("Say that again please")
    #     return "none"

if __name__=="__main__":
    wishMe()

    while True:
        try:
            query = takeCommand().lower() #Converts it in lower case string                                                                                                                                         
        #Logic for executing tasks based on query
        except Exception as e:
            query = 'none'
            speak("Say that again please")


        #Browsing Section
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences= 2) #Sentence defines that how many lines of wikioedia you want to listen
            speak("According to wikipedia")
            print(results)
            speak(results)

        elif 'google' in query:
            webbrowser.open("google.com")
            del query
        elif 'youtube' in query:
            webbrowser.open("youtube.com")
            del query
        elif 'facebook' in query:
            webbrowser.open("facebook.com")
            del query
        elif 'stackoverflow' in query:
            webbrowser.open("stackoverflow.com")
            del query
        elif 'twitter' in query:
            webbrowser.open("twitter.com")
            del query
        elif 'github' in query:
            webbrowser.open("github.com")
            del query
        #Action
        elif 'music' in query:
            music_dir = 'D:\\Audio\\Rock Music'     #need to add stop and next music functionality
            songs = os.listdir(music_dir)
            print(songs)
            del query
        
        elif 'copy file' in query:
            pass
        
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir the time is {strTime}")

        elif 'open vs code' in query:
            codePath = "C:\\Users\\Shouv\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)
        elif 'exit' or 'cancel' or 'quite' in query:
            exit()
        

        # elif 'email to pain' in query:
        #     try:
        #         speak("What should I say:")
        #         content = takeCommand()
        #         to = "iam789souvik@gmail.com"
        #         sendEmail(to, content)
        #         speak("Email has been sent!!")
        #     except Exception as e:
        #         print(e)
        #         speak("I'm Sorry")
        else:
            print("Say that again please...")
            speak("Say that again please...")
            




