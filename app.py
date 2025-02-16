import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.window import Window

import speech_recognition as sr
import pyttsx3
import Bard

class Ashwa(BoxLayout):
    def __init__(self, **kwargs):
        super(Ashwa, self).__init__(**kwargs) 

        self.orientation = 'vertical'

        # Set the background image
        self.background = Image(source='ashwa.jpeg', allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background)

        self.result_label = Label(text="Hello I'm Ashwathama", size_hint=(1, None), height=Window.height * 0.5)
        self.result_label.bind(texture_size=self.result_label.setter('size'))
        self.result_label.bind(size=self.result_label.setter('text_size'))
        self.result_label.text_size = (Window.width * 0.9, None)
        self.add_widget(self.result_label)

        self.button = Button(text='Start Recording')
        self.button.bind(on_press=self.start_recording)
        self.add_widget(self.button)

        self.engine = pyttsx3.init()
        self.ashwa = Bard.Chatbot("ZAiBP4NcCkB18KWHOFqLOxXRu0nArS5xfUcHMAgU1kzuerFD8RtAirwLtGw7DPUEuv8-Ww.")


    def start_recording(self, instance):
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source,timeout=10,phrase_time_limit=10)

        try:
            recognized_text = recognizer.recognize_google(audio)
            print(recognized_text)
            self.result_label.text = self.result(recognized_text+", your reply wordlimit is 75 WORDS only!")
            self.speak_text(self.result_label.text)
        except sr.UnknownValueError:
            self.result_label.text = "Could not understand audio"
        except sr.RequestError as e:
            self.result_label.text = "Could not request results; {0}".format(e)

    def speak_text(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
    def result(self, text):
        
        res=self.ashwa.ask(text)
        return res['content']
    

    
class Ashwathama(App):
    def build(self):
        Window.size=(300,600)
        return Ashwa()

if __name__ == '__main__':
    Ashwathama().run()



