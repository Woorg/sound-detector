import os
import random
import numpy as np
import pygame
import pyaudio
import time

# Инициализация pygame для воспроизведения музыки
pygame.mixer.init()

# Путь к папке с аудиофайлами
sounds_folder = './sounds/'

# Список файлов от '(2).mp3' до '(38).mp3'
sound_files = [f"({i}).mp3" for i in range(2, 39)]

# Проверка наличия файлов
available_files = []
for f in sound_files:
    full_path = os.path.join(sounds_folder, f)
    if os.path.exists(full_path):
        available_files.append(f)
    else:
        print(f"Файл не найден: {full_path}")

print(f"Доступные файлы: {available_files}")

# Настройки для микрофона
CHUNK = 1024  # Количество фреймов в буфере
FORMAT = pyaudio.paInt16  # Формат аудио
CHANNELS = 1  # Количество каналов (моно)
RATE = 44100  # Частота дискретизации (samples per second)

# Инициализация PyAudio
p = pyaudio.PyAudio()

# Открываем поток для микрофона
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Прослушивание микрофона...")

def detect_sound(data, threshold=1500):
    """Определение, превышает ли звук заданный порог"""
    audio_data = np.frombuffer(data, dtype=np.int16)
    peak = np.abs(audio_data).max()
    return peak > threshold

# Флаг для отслеживания, был ли звук воспроизведен
sound_played = False

def play_random_sound():
    """Воспроизводит случайный аудиофайл из папки"""
    if not available_files:
        print("Нет доступных файлов для воспроизведения.")
        return

    random_sound = random.choice(available_files)
    sound_path = os.path.join(sounds_folder, random_sound)

    print(f"Воспроизводим: {random_sound}")
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()

    # Ожидание окончания воспроизведения
    while pygame.mixer.music.get_busy():
        continue

# Основной цикл прослушивания микрофона
try:
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)

        if detect_sound(data) and not sound_played:
            print("Звук обнаружен! Воспроизведение случайного трека...")
            sound_played = True  # Устанавливаем флаг, что звук воспроизводится
            play_random_sound()  # Воспроизводим трек
            
            # Ждем некоторое время перед следующей проверкой
            time.sleep(4)  # Убедитесь, что вы меняете это значение в зависимости от ситуации
        else:
            # Если звук не обнаружен, сбрасываем флаг
            sound_played = False

except KeyboardInterrupt:
    print("Завершение программы...")
finally:
    # Очищаем ресурсы
    stream.stop_stream()
    stream.close()
    p.terminate()
