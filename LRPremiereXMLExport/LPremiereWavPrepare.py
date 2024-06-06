import os
import json
import tkinter as tk
from tkinter import filedialog
import soundfile as sf
import numpy as np
import shutil
import wave
from scipy.io import wavfile as sci_wavfile
import csv
import argparse

import re
from concurrent.futures import ThreadPoolExecutor

sample_rate = 48000  # sample rate in Hz
clip_length_seconds = 5  # length of each clip in seconds
clip_length_frames = clip_length_seconds * sample_rate  # length of each clip in frames

def get_audio_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.wav')]

def load_json_file(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def format_time(time_seconds, decimal_places=3):
    hours, remainder = divmod(time_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}:{int((seconds - int(seconds)) * 10**decimal_places):0{decimal_places}}"

def create_dummy_audio_file(wav_file_path, duration_seconds):
    num_frames = int(duration_seconds * sample_rate)  # calculate number of frames based on duration
    data = np.zeros((num_frames, 2))  # 2 channels for stereo
    sf.write(wav_file_path, data, sample_rate, subtype='PCM_24')
    print(f"Created or overwrote {wav_file_path}")

def create_srt_from_json(srt_file_path, text, start_time_seconds, duration_seconds):
    start_time_formatted = format_time(start_time_seconds)
    end_time_formatted = format_time(start_time_seconds + duration_seconds)
    with open(srt_file_path, 'w') as f:
        f.write(f"1\n{start_time_formatted} --> {end_time_formatted}\n{text}\n\n")
    print(f"Created or overwrote {srt_file_path}")

def generate_markers(subtitles, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        for index, subtitle in enumerate(subtitles, start=1):
            start_time_seconds = subtitle['start_time']
            duration_seconds = subtitle['duration']
            csvfile.write(f"{start_time_seconds:.3f};{duration_seconds:.3f};Rose;segmentation;\"Take {index}\";\"{subtitle['text']}\";\n")

def generate_alternative_markers(subtitles, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        writer.writerow(['Name', 'Start', 'Duration', 'Time Format', 'Type', 'Description'])

        for index, subtitle in enumerate(subtitles, start=1):
            start_time_seconds = subtitle['start_time']
            duration_seconds = subtitle['duration']
            writer.writerow([
                f'Marker {index:02d}',
                f'{start_time_seconds:.3f}',
                f'{duration_seconds:.3f}',
                'decimal',
                'Cue',
                subtitle["text"]
            ])

def sanitize_text(text):
    # Replace any character that is not a-z, A-Z, 0-9, space, !, ., -, or : with a dash (-)
    sanitized_text = re.sub(r'[^a-zA-Z0-9 !.:-]', '-', text)
    # Remove any leading symbols other than space
    sanitized_text = re.sub(r'^[^a-zA-Z0-9 ]+', '', sanitized_text)
    return sanitized_text

def main():
    parser = argparse.ArgumentParser(description='Prepare dummy audio files and subtitle files for use in Adobe Premiere.')
    parser.add_argument('-file', metavar='file', type=str, help='the path to the JSON file')
    parser.add_argument('-time_per_word', metavar='time_per_word', type=float, default=0.6, help='the time per word in seconds')
   
    args = parser.parse_args()
    
    if args.time_per_word is not None:
        duration_per_word = args.time_per_word
    else:
        duration_per_word = 0.6  # default value

    if args.file:
        json_file_path = args.file
    else:
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        json_file_path = filedialog.askopenfilename()

    data = load_json_file(json_file_path)
    audio_files = get_audio_files(os.path.dirname(json_file_path))
    filename = os.path.splitext(os.path.basename(json_file_path))[0]
    dummy_files_folder = os.path.join(os.path.dirname(json_file_path), f'{filename}_dummy')
    os.makedirs(dummy_files_folder, exist_ok=True)
    base_dir = os.path.dirname(json_file_path)
    cumulative_duration_frames = 0  # cumulative duration of all previous clips in frames
    subtitles_folder = os.path.join(dummy_files_folder, 'subtitles')
    os.makedirs(subtitles_folder, exist_ok=True)  # create 'subtitles' subfolder if it doesn't exist

    cumulative_duration_seconds = 0
    
    def process_subtitle(subtitle):
        sanitized_text = sanitize_text(subtitle['text'])
        wav_file_path = os.path.join(dummy_files_folder, f"{filename}_dummy{subtitle['id']}.wav")
        srt_file_path = os.path.join(subtitles_folder, f"{filename}_dummy{subtitle['id']}.srt")
        if not os.path.exists(wav_file_path):
            create_dummy_audio_file(wav_file_path, subtitle['duration'])
        with wave.open(wav_file_path, 'rb') as wav_file:
            frames = wav_file.getnframes()
            rate = wav_file.getframerate()
            duration_seconds = frames / float(rate)
        create_srt_from_json(srt_file_path, sanitized_text, subtitle['start_time'], duration_seconds)

    subtitles = []
    cumulative_duration_seconds = 0
    sorted_data = sorted(data.items())
    data_length = len(sorted_data)
    i = 0
    while i < data_length:
        key, value = sorted_data[i]
        print(value)
        if isinstance(value, list) and len(value) > 0 and isinstance(value[0], str):
            text = value[0].replace('\n', ' ')
        else:
            print(f"Unexpected value at index {i}: {value}")
            text = ""
        num_words = len(text.split())
        duration_seconds = num_words * duration_per_word
        subtitles.append({
            'id': i + 1,
            'text': text,
            'start_time': cumulative_duration_seconds,
            'duration': duration_seconds,
        })
        cumulative_duration_seconds += duration_seconds
        i += 1


    # Create .srt and .wav files based on the subtitles list
    with ThreadPoolExecutor() as executor:
        executor.map(process_subtitle, subtitles)

    filename, _ = os.path.splitext(os.path.basename(json_file_path))

    markers_filename = f"{filename}_markers.csv"
    markers_audio_filename = f"{filename}_markers_audio.csv"

    generate_markers(subtitles, os.path.join(os.path.dirname(json_file_path), markers_filename))
    generate_alternative_markers(subtitles, os.path.join(os.path.dirname(json_file_path), markers_audio_filename))

    os.startfile(os.path.dirname(json_file_path))
        # Do not add the duration to the cumulative duration
        # cumulative_duration_seconds += duration_seconds

if __name__ == "__main__":
    main()
