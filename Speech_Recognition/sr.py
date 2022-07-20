import speech_recognition as sr

#Obtain audio from the microphone
'''
if you are using your laptop mic array, then reduce the mic volume to lower the noise
So that this system can work properly
'''
r = sr.Recognizer()
r.pause_threshold = 1

with sr.Microphone() as source:
    print("Listening...")

    audio = r.listen(source)

#Speech recognition using Google
try:
    print("You said:" + r.recognize_google(audio))

except sr.UnknownValueError:
    print("Could not understand")
except sr.RequestError as e:
    print(e)
