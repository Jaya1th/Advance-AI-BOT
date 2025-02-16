import openai
import gradio as gr
import easyocr
from gtts import gTTS


openai.api_key = "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"

def extract_products(image):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image)
    terms = ""
    for i in range(len(result)):
        terms+=(result[i][1])+" "
    print(terms)
    return terms.lower()

def ASHWAGPT(image,info):
    terms=""
    terms=extract_products(image)

    prompt="You are Medical Brands and Products Expert;wordset is ("+terms+"); when the user gives input ,first reply about information of your known brand product only!(which is close to any word in wordset) ,in around 40 words ; then in next paragraph ,reply based on that product or any medicinal information ,according to user input,in about 40 words"

    messages = [{"role": "system", "content": prompt}]
    messages.append({"role": "user", "content": info})
    
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    
    ASHWAGPT_reply = response["choices"][0]["message"]["content"]

    tts = gTTS(ASHWAGPT_reply, lang='en')
    tts.save('info.mp3')

    messages.append({"role": "assistant", "content": ASHWAGPT_reply})
    return ASHWAGPT_reply

inputs = [gr.inputs.Image(label="Please upload the medicine photo here"),gr.inputs.Textbox(label="Type ('specific_info' of this),to give specific information; If not,press submit")]
outputs = gr.outputs.Textbox(label="The audio of this Information is stored locally as info.mp3 file")


demo = gr.Interface(fn=ASHWAGPT, inputs = inputs, outputs = outputs, title = "Ashwatthama")
demo.launch()