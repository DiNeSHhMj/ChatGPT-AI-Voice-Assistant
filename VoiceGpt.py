import speech_recognition as sr
import pyttsx3
import openai
import tkinter as tk

openai.api_key = "OPEN-AI API KEY"

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[1].id)

r = sr.Recognizer()
mic = sr.Microphone(device_index=1)

conversation = ""
user_name = "Dinesh"
bot_name = "ChatGPT"

# Function to handle user input and generate bot response
def handle_question():
    global conversation
    with mic as source:
        print("\nAsk me a question...")
        engine.say("Ask me a question")
        engine.runAndWait()
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source)
    print("Synthesizing your question...")
    try:
        user_input = r.recognize_google(audio)

        if "stop" in user_input:
            print("Ok, ending the conversation. Have a great day!!!")
            engine.say("Ok, ending the conversation. Have a great day!!!")
            engine.runAndWait()
            return
        
        input_box.delete(0, tk.END)
        input_box.insert(0, user_input)
        prompt = f"{user_name}: {user_input}\n{bot_name}:"
        conversation += prompt
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=conversation,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        response_str = response["choices"][0]["text"].replace("\n", "")
        response_str = response_str.split(
            f"{user_name}:", 1)[0].split(f"{bot_name}:", 1)[0]
        conversation += response_str + "\n"
        output_box.configure(state='normal')
        output_box.insert('end', prompt + ' ' + response_str + '\n\n')
        output_box.configure(state='disabled')
        engine.say(response_str)
        engine.runAndWait()
        refresh_button.pack(pady=10)
    except:
        print("Sorry, I didn't understand that.")
        engine.say("Sorry, I didn't understand that.")
        engine.runAndWait()

# Function to clear the input and output boxes and allow the user to ask another question
def ask_again():
    input_box.delete(0, tk.END)
    output_box.configure(state='normal')
    output_box.delete(1.0, tk.END)
    output_box.configure(state='disabled')
    refresh_button.pack_forget()
    

# Create main window
root = tk.Tk()
root.title('ChatGPT AI Voice Assistant')

# Set font sizes for user and bot names
name_font = ('Arial', 12)

# Create input box
input_box = tk.Entry(root, width=50)
input_box.pack(pady=10)

# Create output box
output_box = tk.Text(root, width=60, height=20, state='disabled')
output_box.configure(background='#212122')
output_box.configure(foreground='white')
output_box.pack(pady=10)

# Create "Ask" button
ask_button = tk.Button(root, text='Ask me a question...', command=handle_question)
ask_button.pack(pady=10)
ask_button.configure(background='#212122')
ask_button.configure(foreground='white')

# Create "Ask Again" button (initially hidden)
refresh_button = tk.Button(root, text='Refresh', command=ask_again)
refresh_button.configure(background='#212122')
refresh_button.configure(foreground='white')
root.mainloop()

