import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os



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
        speak("Good Morning!")
    elif hour >=12 and hour <=18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("I'm Jarvis. PLease tell me how may I help you?")

def takeCommand():
    '''
    This function will recognise our speech and returning as a text string
    '''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        sr.energy_threshold = 300
        r.pause_threshold = 1 #Time taken tom complete a phrase as second.
        audio = r.listen(source)
    try:
        print("Recognising...")
        query = ''
        query = r.recognize_google(audio)
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        print("Say that again please...")
        return "None"
    return query
if __name__=="__main__":
    wishMe()
    while True:
        query = takeCommand().lower() #Converts it in lower case string                                                                                                                                         
        #Logic for executing tasks based on query
        
        #Browsing Section
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences= 2) #Sentence defines that how many lines of wikioedia you want to listen
            speak("According to wikipedia")
            print(results)
            speak(results)
            query = query.replace(query, "")

        elif 'open youtube' or 'youtube' in query:
            webbrowser.open("youtube.com")
            query = query.replace(query, "")

        elif 'open google' or 'google' in query:
            webbrowser.open("google.com")
            query = query.replace(query, "")
        elif 'open fcebook' or 'fcebook' in query:
            webbrowser.open("fcebook.com")
            query = query.replace(query, "")
        elif 'open stackoverflow' or 'stackoverflow' in query:
            webbrowser.open("stackoverflow.com")
            query = query.replace(query, "")
        elif 'open twitter' or 'twitter' in query:
            webbrowser.open("twitter.com")
            query = query.replace(query, "")
        elif 'open github' or 'github' in query:
            webbrowser.open("github.com")
            query = query.replace(query, "")


        #Action
        elif 'play music' or 'music' in query:
            music_dir = 'D:\\Audio\\Rock Music'
            songs = os.listdir(music_dir)
            print(songs)




