import sys
import keyboard
from time import sleep
from playsound import playsound
import speech_recognition
from gpiozero import DigitalOutputDevice, GPIOZeroError


class VoiceRecognition:
    def __init__(self):
        self.recognizer = speech_recognition.Recognizer()
        self.microphone = speech_recognition.Microphone()

    def listen(self):

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            command = self.recognizer.recognize_google(audio)
            return command

        except speech_recognition.UnknownValueError:
            return None

        except speech_recognition.RequestError:
            return None


class Translation:
    def __init__(self):
        self.MORSE_CODE_DICT = {'A': '.-', 'B': '-...',
                                'C': '-.-.', 'D': '-..', 'E': '.',
                                'F': '..-.', 'G': '--.', 'H': '....',
                                'I': '..', 'J': '.---', 'K': '-.-',
                                'L': '.-..', 'M': '--', 'N': '-.',
                                'O': '---', 'P': '.--.', 'Q': '--.-',
                                'R': '.-.', 'S': '...', 'T': '-',
                                'U': '..-', 'V': '...-', 'W': '.--',
                                'X': '-..-', 'Y': '-.--', 'Z': '--..',
                                '1': '.----', '2': '..---', '3': '...--',
                                '4': '....-', '5': '.....', '6': '-....',
                                '7': '--...', '8': '---..', '9': '----.',
                                '0': '-----', ', ': '--..--', '.': '.-.-.-',
                                '?': '..--..', '/': '-..-.', '-': '-....-',
                                '(': '-.--.', ')': '-.--.-'}

    def encrypt(self, message):
        cipher = ''

        for letter in message.upper():
            if letter != ' ':
                cipher += self.MORSE_CODE_DICT[letter] + ' '
            else:
                cipher += ' '

        return cipher

    def decrypt(self, message):
        message += ' '
        decipher = ''
        citext = ''

        for letter in message:
            if (letter != ' '):
                i = 0
                citext += letter
            else:
                i += 1

                if i == 2:
                    decipher += ' '
                else:
                    decipher += list(self.MORSE_CODE_DICT.keys())[list(self.MORSE_CODE_DICT
                                                                  .values()).index(citext)]
                    citext = ''

        return decipher


class Feedback:
    def __init__(self):
        self.feedback_device = DigitalOutputDevice(17, initial_value=False)

    def send(self, on_time, off_time):
        try:
            self.feedback_device.blink(on_time=on_time, off_time=off_time)
        except GPIOZeroError:
            pass


if __name__ == '__main__':
    # recognizer = VoiceRecognition()
    translate = Translation()
    # feedback = Feedback()

    while True:
        # print("Listening...")
        # command = recognizer.listen()
        command = input("Enter Command: ")

        if command is not None:
            morse_code = translate.encrypt(command)

            for signal in morse_code:
                if signal == ".":
                    # feedback.send(0.1, 0.3)
                    playsound('./beep_low_pitch.wav')
                    print("dot")
                    # sleep(0.1)

                elif signal == "-":
                    # feedback.send(0.3, 1)
                    playsound('./beep_high_pitch.wav')
                    print("hyphen")
                    # sleep(0.1)

                elif signal == " ":
                    sleep(0.5)
                    print("space")
