import google.generativeai as genai
import speech_recognition as sr
import pyttsx3

# 🔑 Set your Gemini API key here
genai.configure(api_key="AIzaSyC5MmOeelrkLALUVPN7SRSKQibCdfyH5X8")

# 🎙️ Speech recognizer and mic
recognizer = sr.Recognizer()
mic = sr.Microphone()

# 🧠 Load Gemini model (free)
model = genai.GenerativeModel('gemini-1.5-flash')

# 🔊 Text-to-speech engine
engine = pyttsx3.init()

print("Say something... (Ctrl+C to stop)")
while True:
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = recognizer.listen(source)

        user_input = recognizer.recognize_google(audio)
        print("You said:", user_input)

        # Get Gemini response
        response = model.generate_content(user_input)
        reply = response.text
        print("Gemini:", reply)

        # Speak the reply
        engine.say(reply)
        engine.runAndWait()

    except sr.UnknownValueError:
        print("Sorry, I didn’t catch that.")
    except KeyboardInterrupt:
        print("\nExiting...")
        break

