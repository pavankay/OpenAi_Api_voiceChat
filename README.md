# Voice chat
We utilize Open AI's whisper v2 model for transcription, Open AI gpt 4 for processing, and Open AI's Text To Speech (TTS) model.
## Getting started

- Clone this respostory

- Python 3.12. [Download here](https://www.python.org/downloads/release/python-3120/) and make sure it's added to PATH. 

- Run the following command to install the necessary Python packages:
```bash
pip install pyaudio wave pygame speech_recognition python-dotenv
```

- Get and [Open AI api key](Openai.com) you must have an acount to do so.

- Paste the key into the .env file

- Make a new folder in the same direcotry called:"speech_files"

- Run this command to start:
```bash
pip install pyaudio wave pygame speech_recognition python-dotenv
```


## Important notes

- In the code provided I use GPT-4 however if you dont have a paid acount with Open AI you will have to switch the model. More info [here](https://platform.openai.com/docs/models).

