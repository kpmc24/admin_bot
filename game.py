import random
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import os

word = ""

words_by_level = {
    "easy": ["кот", "собака", "яблоко", "молоко", "солнце"],
    "medium": ["банан", "школа", "друг", "окно", "жёлтый"],
    "HARD": ["технология", "университет", "информация", "произношение", "воображение"]
}

level = int(input("Введите уровень сложности: 1 - easy, 2 - medium, 3 - HARD "))
if level == 1:
    word = random.choice(words_by_level["easy"])
elif level == 2:
    word = random.choice(words_by_level["medium"])
elif level == 3:
    word = random.choice(words_by_level["HARD"])

print(f"Скажи слово {word} на английском ")


duration = 5  # секунды записи
sample_rate = 44100
print("Говори...")
recording = sd.rec(
  int(duration * sample_rate), # длительность записи в сэмплах
  samplerate=sample_rate,      # частота дискретизации
  channels=1,                  # 1 — это моно
  dtype="int16")               # формат аудиоданных
sd.wait()
wav.write("output.wav", sample_rate, recording)
print("Запись завершена, теперь распознаём...")
recognizer = sr.Recognizer()

print(recognizer)
with sr.AudioFile("output.wav") as source:
    audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language="en-EN")
        text = text.lower()
        print("Ты сказал:", text)
        translator = Translator()
        translated = translator.translate(text, dest='ru')  # здесь 'en' — это английский
        if translated.text == word:
            print(" Ты угадал слово ")
        else:
            print(" Ты не угадал слово ")   
    except sr.UnknownValueError:             # - если Google не понял речь (шум, молчание)
        print("Не удалось распознать речь.")
    except sr.RequestError as e:             # - если нет интернета или API недоступен
        print(f"Ошибка сервиса: {e}")