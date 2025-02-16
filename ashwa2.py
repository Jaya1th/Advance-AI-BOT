import pyttsx3
import speech_recognition as sr
from Bard import Chatbot
from EdgeGPT.EdgeUtils import ImageQuery
import json
# from pyfirmata import Arduino,SERVO
# import threading
# import time
cookies = json.loads(open("bing_cookies_file.json", encoding="utf-8").read())
token = "ZAiBP4NcCkB18KWHOFqLOxXRu0nArS5xfUcHMAgU1kzuerFD8RtAirwLtGw7DPUEuv8-Ww."
ashwa = Chatbot(token)

# port = 'Com3'
# pin =10
# board=Arduino(port)
# board.digital[pin].mode = SERVO

engine  = pyttsx3.init()

start_word = "ashwathama"
image_word = "imagine"
close_word = "sleep"
recognizer = sr.Recognizer()

# def rotateservo(m,pin=10):
#     for i in range(0,m*55):
#         board.digital[pin].write(i%45)
#         time.sleep(0.001)

def speak(text,rate=180):
    engine.setProperty('rate',rate)
    engine.say(text)
    engine.runAndWait()

def prompt_ashwa(prompt):
    ashwa_response = ashwa.ask(prompt)
    return ashwa_response['content']

def verify_start_word(user_said):
    if start_word in user_said.lower():
        return start_word
    elif close_word in user_said.lower():
        print("Ashwathama : Goodbye, see you next time!")
        # t1 = threading.Thread(target=rotateservo,args=[3])
        # t1.start()
        speak('Goodbye, see you next time')
        # t1.join()
        exit(0)
    else:
        return None
    
def main():
    counter=0
    while True:
        with sr.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic)
            recognizer.pause_threshold=2
            start_counter = 0
            
            if counter == 0:
                while (start_counter < 3):
                    print(f"Try saying 'Ashwathama' to activate else 'Sleep' to exit' .... ")
                    start_word_audio = recognizer.listen(mic,timeout=10,phrase_time_limit=5)
                    user_said = recognizer.recognize_google(start_word_audio,language='en-in')
                    print(f"You : {user_said}")
                    user_start_word = verify_start_word(user_said)
                    if user_start_word is not None:
                        break
                    else:
                        print("I didn't recognize 'Ashwathama'! ...")
                        start_counter+=1
                    
            if(start_counter == 3):
                print("Unable to activate...terminating this session.")
                exit()
            if counter==0:
                # t1 = threading.Thread(target=rotateservo,args=[4])
                # t1.start()
                speak("Hello I'm Ashwatthama. How can I help you ?")
                # t1.join()
                 
            else:
                # t1 = threading.Thread(target=rotateservo,args=[4])
                # t1.start()
                speak("If you wish to continue, ask or say anything")
                # t1.join()
            counter+=1
            print("Ashwathama : Ask any questions, or say 'Imagine' to generate images, or 'Sleep' to exit...(listening for 10s.)")
            user_audio = recognizer.listen(mic,timeout=10,phrase_time_limit=10)

            user_input = recognizer.recognize_google(user_audio,language='en-in')
            print(f"You : {user_input}")
            

            if close_word in user_input[0:5].lower():
                verify_start_word("sleep")
            elif image_word in user_input[0:7].lower():
                # t2 = threading.Thread(target=rotateservo,args=[4])
                # t2.start()
                speak("Sure. Please describe the image to be generated")
                # t2.join()            
                print("Ashwathama : Describe the image....(listening for 10 seconds)")
                user_image_audio = recognizer.listen(mic,timeout=10,phrase_time_limit=10)
                user_image_input = recognizer.recognize_google(user_image_audio,language='en-in')
                print(f"You : {user_image_input}")
                ImageQuery(user_image_input)
                ashwa_response="I have generated the images in the current directory    "
            else:
                ashwa_response = prompt_ashwa("answer wordlimit is 50 WORDS ONLY! :, "+user_input)
        print("Ashwathama :", ashwa_response)
        # t3 = threading.Thread(target=rotateservo,args=[len(ashwa_response)//13])
        # t3.start()
        speak(ashwa_response)
        # t3.join()
       
if __name__ == "__main__":
    main()