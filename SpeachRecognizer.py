import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os
import time

def recognize_mic(recognizer, microphone):
    """
    Turn an audio
    """
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")


    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        #API unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"
    
    return response

def createAudio(text, fileName):
    """
    Turns text response into mp3 and then plays audio for user

    Args: str response
    """
    language = 'en'
    fileName = "response.mp3"
    ttsObj = gTTS(text=text, lang=language, slow=False)
    ttsObj.save(fileName)
    return fileName
    
def speak(audioFile):    
    print("speaking...")
    playsound(audioFile)
    print("sleeping")
    time.sleep(1)

def speechHandler(text, fileName = "response.mp3"):
    print("handler")
    audioFileName = createAudio(text, fileName)
    print("speak")
    speak(audioFileName)
    os.remove(fileName)

if __name__ == "__main__":
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    fulfilled = False
    while fulfilled == False:
        attempts = 3
        # get the command from the user
        # if a transcription is returned, break out of the loop and
        #     continue
        # if no transcription returned and API request failed, break
        #     loop and continue
        # if command is stop, break loop and continue
        #
        # if API request succeeded but no transcription was returned,
        #     re-prompt the user to say their command again untill 
        for j in range(attempts):
            speechHandler('How can I help you?')
            command = recognize_mic(recognizer, mic)
            if command["transcription"]:
                if command["transcription"].lower() == "stop":
                    fulfilled = True
                    speechHandler("Goodbye")
                break
            if not command["success"]:
                break
            speechHandler("I didn't catch that. Could you repeat that?")

        # if there was an error speechHandler and end
        if command["error"]:
            speechHandler("ERROR: {}".format(command["error"]))
        else:
            # show the user the transcription
            speechHandler("You said: {}".format(command["transcription"]))