import os
import shutil
import datetime
import webbrowser
import speech_recognition as sr
import pyttsx3

# Voice Engine Setup
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Sir!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Sir!")
    else:
        speak("Good Evening Sir!")

    speak("I am your assistant. Ready to help you.")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}\n")
    except Exception as e:
        print("Error:", e)
        print("Unable to Recognize your voice.")
        return "None"
    return query.lower()

# Mapping voice commands to URLs
voice_url_map = {
    "open home screen": "http://127.0.0.1:8000/main_page/",
    "open coupon list": "http://127.0.0.1:8000/main_page/maincoupon_list/",
    "create coupon": "http://127.0.0.1:8000/main_page/create_coupon/",
    "claim coupon": "http://127.0.0.1:8000/main_page/claim/1/",  # Example with coupon_id = 1
    "login": "http://127.0.0.1:8000/main_page/login/",
    "logout": "http://127.0.0.1:8000/main_page/logout/",
    "user profile": "http://127.0.0.1:8000/main_page/user_profile_view/",
    "manager profile": "http://127.0.0.1:8000/main_page/manager_profile_view/",
    "open dashboard": "http://127.0.0.1:8000/main_page/coupon_dashboard_view",
    "register": "http://127.0.0.1:8000/main_page/register_view/",
    "generate promo code": "http://127.0.0.1:8000/main_page/generate_promo_code/",
    "use promo code": "http://127.0.0.1:8000/main_page/use_promo_code/",
    "food page": "http://127.0.0.1:8000/main_page/swiggy/",
    "add category": "http://127.0.0.1:8000/main_page/add-category/",
    "add food item": "http://127.0.0.1:8000/main_page/add-food-item/",
    "checkout": "http://127.0.0.1:8000/main_page/checkout/",
    "order history": "http://127.0.0.1:8000/main_page/order_history/",
    "view cart": "http://127.0.0.1:8000/main_page/cart/",
    "listings": "http://127.0.0.1:8000/main_page/listings",
    "realtor list": "http://127.0.0.1:8000/main_page/realtor_list",
    "realtor dashboard": "http://127.0.0.1:8000/main_page/realtors_dashboard",
    "real index": "http://127.0.0.1:8000/main_page/realindex",
    "about": "http://127.0.0.1:8000/main_page/about",
}

def open_mapped_url(query):
    for command, url in voice_url_map.items():
        if command in query:
            speak(f"Opening {command}")
            print(f"Opening URL: {url}")
            webbrowser.open(url)
            return
    speak("Sorry, I could not find a matching page.")

if __name__ == "__main__":
    clear = lambda: os.system("cls" if os.name == "nt" else "clear")
    clear()
    wishMe()

    while True:
        query = takeCommand()
        if query == "none":
            continue

        if "exit" in query or "quit" in query or "stop" in query:
            speak("Goodbye Sir!")
            break

        elif "open" in query:
            open_mapped_url(query)

        elif "wikipedia" in query:
            import wikipedia
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
