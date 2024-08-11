import speech_recognition as sr
import webbrowser
import platform
import time
import pywhatkit
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pyttsx3

recognition = sr.Recognizer()
engine = pyttsx3.init()

contacts = {
    "papa": "+919335234317",
}

def speak(text):
    engine.say(text)
    engine.runAndWait()

# def open_google_maps(location=None):
#     """Open Google Maps with a specific location or directions."""
#     if location:
#         location_query = "+".join(location.split())
#         maps_url = f"https://www.google.com/maps/search/?api=1&query={location_query}"
#     else:
#         maps_url = "https://www.google.com/maps"
    
#     try:
#         webbrowser.open(maps_url)
#         speak(f"Opening Google Maps for {location}.")
#     except Exception as e:
#         speak(f"An error occurred while opening Google Maps: {e}")

# def get_directions(source, destination):
#     """Get directions from one location to another using Google Maps."""
#     source_query = "+".join(source.split())
#     destination_query = "+".join(destination.split())
#     directions_url = f"https://www.google.com/maps/dir/{source_query}/{destination_query}"
    
#     try:
#         webbrowser.open(directions_url)
#         speak(f"Getting directions from {source} to {destination}.")
#     except Exception as e:
#         speak(f"An error occurred while getting directions: {e}")

def play_specific_song():
    """Play a specific song on YouTube."""
    song_name = listen_for_input("Please tell me the name of the song")
    if song_name:
        try:
            pywhatkit.playonyt(song_name)
            speak(f"Playing {song_name} on YouTube.")
        except Exception as e:
            speak(f"An error occurred while playing the song: {e}")

def tell_system_info():
    """Provide information about the system."""
    os_info = platform.system()
    version_info = platform.version()
    uptime = time.time() - time.monotonic()
    uptime_str = str(int(uptime // 3600)) + " hours " + str(int((uptime % 3600) // 60)) + " minutes"
    
    speak(f"You are running {os_info} version {version_info}. The system has been up for {uptime_str}.")

def open_youtube_video():
    """Open a specific video on YouTube."""
    video_name = listen_for_input("Please tell me the name of the video")
    if video_name:
        try:
            pywhatkit.playonyt(video_name)
            speak(f"Opening {video_name} on YouTube.")
        except Exception as e:
            speak(f"An error occurred while opening the video: {e}")

def listen_for_input(prompt):
    """Listen for user input and return it as text."""
    speak(prompt)
    with sr.Microphone() as source:
        recognition.adjust_for_ambient_noise(source)
        audio = recognition.listen(source)
        try:
            text = recognition.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Please try again.")
        except sr.RequestError:
            speak("Sorry, I'm having trouble connecting to the recognition service.")
    return None

def send_whatsapp_message():
    """Send a WhatsApp message to a contact from the list."""
    contact_name = listen_for_input("Please tell me the contact name")
    if contact_name:
        contact_name = contact_name.lower().strip()
        if contact_name in contacts:
            message = listen_for_input("Please tell me the message")
            if message:
                try:
                    pywhatkit.sendwhatmsg_instantly(contacts[contact_name], message)
                    speak("WhatsApp message sent successfully.")
                except Exception as e:
                    speak(f"An error occurred while sending the message: {e}")
        else:
            speak("Sorry, I couldn't find that contact in your list. Please try again.")


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com/")
        speak("Google opened")

    elif "open" in c.lower():
        # Extract the website name from the command
        website_name = c.lower().replace("open", "").strip()
        if website_name:
            url = f"https://www.{website_name}.com"
            try:
                webbrowser.open(url)
                speak(f"{website_name.capitalize()} opened")
            except Exception as e:
                speak(f"An error occurred while trying to open {website_name}: {e}")
        else:
            speak("Sorry, I didn't catch the website name.")
    if "open email" in c.lower():
        webbrowser.open("https://www.gmail.com/")
        speak("Email opened")
    
    elif "system info" in c.lower():
        tell_system_info()



    # if "show" in c.lower() and "on google maps" in c.lower():
    #     location = c.lower().replace("show", "").replace("on google maps", "").strip()
    #     open_google_maps(location)

    # elif "direction" in c.lower() and "to" in c.lower():
    #     try:
    #         parts = c.lower().split(" to ")
    #         source = parts[0].replace("direction", "").strip()
    #         destination = parts[1].strip()
    #         get_directions(source, destination)
    #     except IndexError:
    #         speak("Sorry, I didn't catch the source or destination. Please try again.")




    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com/")
        speak("Facebook opened")
    elif "open pw" in c.lower():
        webbrowser.open("https://www.pw.live/study/batches/study/my-batches")
        speak("PW opened")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com/")
        speak("YouTube opened")
    elif "open spotify" in c.lower():
        webbrowser.open("https://open.spotify.com/")
        speak("Spotify opened")
    elif "play song on spotify" in c.lower():
        speak("Please tell me the name of the song")
        with sr.Microphone() as source:
            print("Listening for song name...")
            recognition.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            audio = recognition.listen(source)
            try:
                song_name = recognition.recognize_google(audio)
                query = '+'.join(song_name.split())
                url = f"https://open.spotify.com/search/{query}"
                webbrowser.open(url)
                speak(f"Playing {song_name} on Spotify")
            except sr.UnknownValueError:
                speak("Sorry, I didn't catch that. Please try again.")
            except sr.RequestError:
                speak("Sorry, I'm having trouble connecting to the recognition service.")
    elif "send whatsapp message" in c.lower():
        send_whatsapp_message()

    elif "play song" in c.lower():
        play_specific_song()

    elif "open youtube" in c.lower():
        open_youtube_video()

    elif "exit" in c.lower() or "quit" in c.lower():
        speak("Goodbye!")
        return False  # Indicate that the loop should stop
    else:
        speak("Sorry, I didn't understand the command.")
    
    return True  # Indicate that the loop should continue

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        r = sr.Recognizer()

        try:
            with sr.Microphone() as source:
                print("Listening...")
                r.adjust_for_ambient_noise(source)  # Adjust for ambient noise
                audio = r.listen(source, timeout=2, phrase_time_limit=10)
            try:
                word = r.recognize_google(audio)
                if word.lower() == "jarvis":
                    speak("Yes?")
                    # Listen for command
                    with sr.Microphone() as source:
                        print("Jarvis Active...")
                        r.adjust_for_ambient_noise(source)  # Adjust for ambient noise
                        audio = r.listen(source, timeout=2, phrase_time_limit=10)
                        try:
                            command = r.recognize_google(audio)
                            if not processCommand(command):  # Check if the loop should continue
                                break  # Exit the loop
                        except sr.UnknownValueError:
                            speak("Sorry, I didn't catch that. Could you please repeat?")
                        except sr.RequestError:
                            speak("Sorry, I'm having trouble connecting to the recognition service.")
            except sr.UnknownValueError:
                print("Listening Error: Speech not understood")
            except sr.RequestError:
                print("Listening Error: Recognition service error")
        except Exception as e:
            print(f"Error: {e}")

# import kivy
# from kivy.app import App
# from kivy.uix.button import Button
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.label import Label
# from kivy.uix.textinput import TextInput
# import speech_recognition as sr
# import pyttsx3
# import pywhatkit
# import webbrowser

# recognition = sr.Recognizer()
# engine = pyttsx3.init()

# contacts = {
#     "papa": "+919335234317",
# }

# def speak(text):
#     engine.say(text)
#     engine.runAndWait()

# class JarvisApp(App):
#     def build(self):
#         self.layout = BoxLayout(orientation='vertical')
        
#         self.label = Label(text="Press the button and say 'Jarvis' to give a command")
#         self.layout.add_widget(self.label)
        
#         self.button = Button(text="Activate Jarvis")
#         self.button.bind(on_press=self.listen_for_activation)
#         self.layout.add_widget(self.button)
        
#         return self.layout

#     def listen_for_activation(self, instance):
#         speak("Listening...")
#         with sr.Microphone() as source:
#             recognition.adjust_for_ambient_noise(source)
#             audio = recognition.listen(source)
#             try:
#                 word = recognition.recognize_google(audio)
#                 if word.lower() == "jarvis":
#                     self.label.text = "Jarvis Activated, listening for command..."
#                     speak("Yes?")
#                     self.listen_for_command()
#                 else:
#                     self.label.text = "Say 'Jarvis' to activate."
#             except sr.UnknownValueError:
#                 self.label.text = "Speech not understood, please try again."
#             except sr.RequestError:
#                 self.label.text = "Recognition service error."

#     def listen_for_command(self):
#         with sr.Microphone() as source:
#             recognition.adjust_for_ambient_noise(source)
#             audio = recognition.listen(source)
#             try:
#                 command = recognition.recognize_google(audio)
#                 self.label.text = f"Command: {command}"
#                 self.process_command(command)
#             except sr.UnknownValueError:
#                 speak("Sorry, I didn't catch that. Could you please repeat?")
#             except sr.RequestError:
#                 speak("Sorry, I'm having trouble connecting to the recognition service.")

#     def process_command(self, command):
#         if "open google" in command.lower():
#             webbrowser.open("https://www.google.com/")
#             speak("Google opened")
#         elif "open" in command.lower():
#             website_name = command.lower().replace("open", "").strip()
#             if website_name:
#                 url = f"https://www.{website_name}.com"
#                 webbrowser.open(url)
#                 speak(f"{website_name.capitalize()} opened")
#             else:
#                 speak("Sorry, I didn't catch the website name.")
#         elif "send whatsapp message" in command.lower():
#             self.send_whatsapp_message()
#         elif "play song" in command.lower():
#             self.play_specific_song()
#         elif "open youtube" in command.lower():
#             self.open_youtube_video()
#         elif "exit" in command.lower() or "quit" in command.lower():
#             speak("Goodbye!")
#             App.get_running_app().stop()
#         else:
#             speak("Sorry, I didn't understand the command.")

#     def listen_for_input(self, prompt):
#         speak(prompt)
#         with sr.Microphone() as source:
#             recognition.adjust_for_ambient_noise(source)
#             audio = recognition.listen(source)
#             try:
#                 text = recognition.recognize_google(audio)
#                 return text
#             except sr.UnknownValueError:
#                 speak("Sorry, I didn't catch that. Please try again.")
#             except sr.RequestError:
#                 speak("Sorry, I'm having trouble connecting to the recognition service.")
#         return None

#     def play_specific_song(self):
#         song_name = self.listen_for_input("Please tell me the name of the song")
#         if song_name:
#             try:
#                 pywhatkit.playonyt(song_name)
#                 speak(f"Playing {song_name} on YouTube.")
#             except Exception as e:
#                 speak(f"An error occurred while playing the song: {e}")

#     def open_youtube_video(self):
#         video_name = self.listen_for_input("Please tell me the name of the video")
#         if video_name:
#             try:
#                 pywhatkit.playonyt(video_name)
#                 speak(f"Opening {video_name} on YouTube.")
#             except Exception as e:
#                 speak(f"An error occurred while opening the video: {e}")

#     def send_whatsapp_message(self):
#         contact_name = self.listen_for_input("Please tell me the contact name")
#         if contact_name:
#             contact_name = contact_name.lower().strip()
#             if contact_name in contacts:
#                 message = self.listen_for_input("Please tell me the message")
#                 if message:
#                     try:
#                         pywhatkit.sendwhatmsg_instantly(contacts[contact_name], message)
#                         speak("WhatsApp message sent successfully.")
#                     except Exception as e:
#                         speak(f"An error occurred while sending the message: {e}")
#             else:
#                 speak("Sorry, I couldn't find that contact in your list. Please try again.")

# if __name__ == "__main__":
#     JarvisApp().run()
