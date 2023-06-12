import speech_recognition as sr
import webbrowser
import pyttsx3
import os
import subprocess
import requests
import json
from win10toast_persist import ToastNotifier
from datetime import date
import tinytuya
d = tinytuya.OutletDevice(
    dev_id= 'DEVICE_ID',
    address ='DEVICE_IP_ADDRESS', #or Auto
    local_key= 'DEVICE_LOCAL_KEY'
)

engine = pyttsx3.init()
engine.setProperty('volume', 0.5)
engine.setProperty('rate', 100)

def search_application(application_name):
    """Funkcja do wyszukiwania aplikacji na komputerze"""
    for root, dirs, files in os.walk('C:\\'):  # Możesz zmienić ścieżkę początkową, jeśli chcesz przeszukać inną lokalizację
        for file in files:
            if file.lower() == application_name.lower():  # Sprawdź, czy nazwa pliku odpowiada poszukiwanej nazwie aplikacji (ignorując wielkość liter)
                return os.path.join(root, file)  # Jeśli tak, zwróć pełną ścieżkę do pliku
    return None  # Jeśli nie znaleziono aplikacji, zwróć None

def recognize(msg="Jestem : "):
    r= sr.Recognizer()

    with sr.Microphone() as source:
        print(msg)
        audio = r.listen(source)
        try:
            recognize_text= r.recognize_google(audio, language="pl-PL")
            print(f"Powiedziałeś {recognize_text}")
            return recognize_text.lower()
        except sr.UnknownValueError:
            print("Nie zrozumiałem co powiedziałeś")
        except sr.AttributeError:
            print("Nie wykryłem polecenia")
        except sr.RequestError as e:
            print(f"ERROR: {e}")


text = recognize()
word_list= text.split(" ")

if ("otwórz" in text and word_list[0] =="otwórz") or ("uruchom" in text and word_list[0] == "uruchom"):
    if "przeglądarkę" in text:
        engine.say("Otwieram przeglądarkę")
        engine.runAndWait()
        webbrowser.open_new_tab("https://www.google.com")
    elif  "program" in text:
     nazwa_aplikacji = word_list[2] +".exe"  # Podaj nazwę aplikacji, której szukasz
     sciezka = search_application(nazwa_aplikacji)
     if sciezka:
         engine.say(f"uruchamiam {nazwa_aplikacji}".replace(".exe",""))
         engine.runAndWait()
         subprocess.run(sciezka)
     else:
         print(f"Apliakcja {nazwa_aplikacji} nie została znaleziona")

elif "wyłącz" in text and word_list[0] == "wyłącz":
    if "komputer" in text:
        engine.say("Wyłączam komputer")
        engine.runAndWait()
        os.system("shutdown /s /t 0")
    if "światło" in text:
        engine.say("Wyłączam światło")
        engine.runAndWait()
        d.set_status(False)
elif "włącz" in text and word_list[0] == "włącz":
    if "światło" in text:
        engine.say("Włączam światło")
        engine.runAndWait()
        d.set_status(True)


# elif text == "jaka jest pogoda":
#     subprocess.call("explorer.exe shell:appsFolder\\Microsoft.BingWeather_Bwekyb3d8bbwe!App", shell=True,
#                     stdout=subprocess.PIPE)