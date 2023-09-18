import queue, os, threading
import sounddevice as sd
import soundfile as sf
import numpy as np

q = queue.Queue()
recorder = False
recording = False

def complicated_record():
    frames_recorded = 0
    with sf.SoundFile("temp.wav", mode='w', samplerate=16000, subtype='PCM_16', channels=1) as file:
        with sd.InputStream(samplerate=16000, dtype='int16', channels=1, callback=complicated_save):
            while recording:
                data = q.get()
                file.write(data)
                frames_recorded += len(data)
                if frames_recorded >= 16000 * 6:  # 2 seconds of audio
                    break

def complicated_save(indata, frames, time, status):
    q.put(indata.copy())

def start():
    global recorder
    global recording
    recording = True
    recorder = threading.Thread(target=complicated_record)
    print('start recording')
    recorder.start()

def stop():
    global recorder
    global recording
    recording = False
    recorder.join()
    print('stop recording')

def split_audio():
    data, samplerate = sf.read("temp.wav")
    duration = len(data) / samplerate
    chunk_size = int(len(data) / 3)
    print()
    for i in range(3):
        chunk = data[i * chunk_size: (i + 1) * chunk_size]
        output_filename = f"output{i + 1}.wav"
        sf.write(output_filename, chunk, samplerate)