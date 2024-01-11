import os
import pyaudio
import wave
from openai import OpenAI
import pygame
import speech_recognition as sr
from dotenv import load_dotenv
load_dotenv()

# OpenAI API Key
#api_key_openai = os.getenv('OPENAI_API_KEY')
client = OpenAI()#if having errors add this api_key=api_key_openai inside

# Rest of your code...

def select_voice():
    voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    print("Please select a voice for the TTS response:")
    for i, voice in enumerate(voices):
        print(f"{i+1}. {voice}")

    choice = 0
    while choice not in range(1, len(voices)+1):
        try:
            choice = int(input("Enter your choice (1-6): "))
        except ValueError:
            pass

    return voices[choice - 1]

def main(selected_voice):
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        # Adjust for ambient noise and start recording
        print('Adjusting for ambient noise. Please wait.')
        recognizer.adjust_for_ambient_noise(source)

        print('Please start speaking.')
        audio = recognizer.listen(source)  # Listen until pause in speech

    print('Finished recording')

    # Save the recorded data as a WAV file
    wav_file_path = 'speech_files/userSpeech.wav'
    with open(wav_file_path, "wb") as file:
        file.write(audio.get_wav_data())

    print('Finished recording and saved to', wav_file_path)

    # Processing the speech with OpenAI
    with open(wav_file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
    print("User: " + transcript.text)

    # Removing the temporary WAV file
    os.remove(wav_file_path)

    # Getting response from OpenAI
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "assistant", "content": "You are a helpful assistant."},
            {"role": "user", "content": transcript.text}
        ]
    )
    response = completion.choices[0].message.content
    print("AI: "+ response)

    # Text-to-Speech
    systemSpeech_file_path = 'speech_files/systemSpeech.mp3'
    response = client.audio.speech.create(
        model="tts-1-hd",
        voice=selected_voice,
        input=response
    )
    response.stream_to_file(systemSpeech_file_path)

    # Play the response
    pygame.mixer.init()
    pygame.mixer.music.load(str(systemSpeech_file_path))
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.stop()
    pygame.mixer.quit()

    # Remove temporary MP3 file
    os.remove(systemSpeech_file_path)

selected_voice = select_voice()
while True:
    main(selected_voice)
