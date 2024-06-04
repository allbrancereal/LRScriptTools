import pyaudio
import wave
import os
import sys
import keyboard
import numpy as np
import psutil
import wavefile
# Set the file names
running_file = "_running"
final_file = "temp.wav"

# Set the audio parameters
chunk = 1024  # Record in chunks of 1024 samples
# Set the audio parameters
use_24bit = False  # Set to True for 24-bit audio, False for 16-bit

if use_24bit:
    sample_format = pyaudio.paInt24  # 24 bits per sample
else:
    sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 48000  # Record at 48000 samples per second
volume = 1.0  # Start with max volume

p = pyaudio.PyAudio()
# Global counter for message IDs
message_id_counter = 0

# Custom print function
class CustomPrint:
    def __init__(self):
        self.log = []
        self.ids = []

    def print(self, message, id=None):
        global message_id_counter
        if id is None:
            id = str(message_id_counter)
            message_id_counter += 1
        if id in self.ids:
            index = self.ids.index(id)
            if self.log[index][1] != message:
                self.log[index] = (id, message)
        else:
            self.log.append((id, message))
            self.ids.append(id)

    def flush_print(self):
        for id, message in self.log:
            print(f"{id} - {message}", flush=True)
            sys.stdout.flush()


# Instantiate the custom print function
printer = CustomPrint()

# Define the hotkeys
def increase_volume(e):
    global volume
    volume = min(volume + 0.1, 1.0)

def decrease_volume(e):
    global volume
    volume = max(volume - 0.1, 0.0)
# Define a function for dynamic range compression
def compress_dynamic_range(data, threshold=0.5, ratio=3.0):
    # Calculate the absolute value of the data
    abs_data = np.abs(data)
    # Find where the data exceeds the threshold
    over_threshold = abs_data > threshold
    # Apply the compression ratio to data over the threshold
    data[over_threshold] = (data[over_threshold] - threshold) / ratio + threshold
    return data

keyboard.on_press_key("up", increase_volume)
keyboard.on_press_key("down", decrease_volume)

stream = None
try:
    # Create a dummy running file
    open(running_file, 'w').close()

    # Open the final file in write mode
    wf = wave.open(final_file, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)

    # Start the recording
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    printer.print('start', 'Recording started')
    
    # Recording function
    while os.path.exists(running_file):
        data = stream.read(chunk)
        # Adjust the volume
        if use_24bit:
            # Interpret the data as 24-bit PCM
            numpydata = np.frombuffer(data, dtype='<i3').astype(np.int32)
            # Adjust the volume
            numpydata = (numpydata * volume).astype(np.int32)
        else:
            numpydata = np.frombuffer(data, dtype=np.int16)
            numpydata = (numpydata * volume).astype(np.int16)
        # Apply dynamic range compression
        numpydata = compress_dynamic_range(numpydata)
        # Normalize the audio to prevent clipping, only if volume is not at max and audio is above a certain level
        if volume != 1.0 and np.max(np.abs(numpydata)) > 0.1:
            numpydata = ((numpydata / np.max(np.abs(numpydata))) * (2**23 if use_24bit else 2**15)).astype(np.int32 if use_24bit else np.int16)
        # Separate the left and right channels
        right_channel = numpydata[1::2]
        # Duplicate the right channel to the left
        numpydata_stereo = np.column_stack((right_channel, right_channel)).ravel()
        wf.writeframes(numpydata_stereo.tobytes())
        # Calculate dB level
        volume_norm = np.linalg.norm(numpydata) * 10
        db = 20 * np.log10(volume_norm)
        printer.print('db', "dB level: " + str(db))
        printer.flush_print()



    # Set the process to real-time priority
    p = psutil.Process()
    p.nice(psutil.REALTIME_PRIORITY_CLASS)

except KeyboardInterrupt:
    printer.print('stop', 'Recording stopped')

    # Stop and close the stream 
    if stream is not None:
        stream.stop_stream()
        stream.close()

    # Close the file
    if wf is not None:
        wf.close()

    # Terminate the PortAudio interface
    p.terminate()

    # Delete the running file
    if os.path.exists(running_file):
        os.remove(running_file)

    # Print all messages
    printer.flush_print()

except Exception as e:
    printer.print('error', f"An error occurred: {e}")
    sys.exit(1)
