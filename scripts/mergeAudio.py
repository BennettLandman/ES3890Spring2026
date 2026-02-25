#!/usr/bin/env python3

import sys
import os
import tempfile
import subprocess
import numpy as np
import soundfile as sf
import pyloudnorm as pyln
from scipy.signal import butter, lfilter
import random

TARGET_LUFS = -19.0
SAMPLE_RATE = 48000

SILENCE_THRESHOLD = 0.01
GAP_MIN = 0.25
GAP_MAX = 0.6

# De-esser settings
DEESS_LOW = 5000
DEESS_HIGH = 10000
DEESS_THRESHOLD = 0.02
DEESS_RATIO = 4.0


def convert_to_wav(input_path, output_path):
    subprocess.run([
        "ffmpeg", "-y",
        "-i", input_path,
        "-ac", "1",
        "-ar", str(SAMPLE_RATE),
        output_path
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)


def trim_silence(audio):
    abs_audio = np.abs(audio)
    mask = abs_audio > SILENCE_THRESHOLD

    if not np.any(mask):
        return audio

    start = np.argmax(mask)
    end = len(mask) - np.argmax(mask[::-1])

    return audio[start:end]


def highpass_filter(audio, sr, cutoff=80):
    b, a = butter(2, cutoff / (sr / 2), btype='high')
    return lfilter(b, a, audio)


def bandpass_filter(audio, sr, low, high):
    b, a = butter(2, [low / (sr / 2), high / (sr / 2)], btype='band')
    return lfilter(b, a, audio)


def deesser(audio, sr):
    sibilant_band = bandpass_filter(audio, sr, DEESS_LOW, DEESS_HIGH)

    envelope = np.abs(sibilant_band)
    gain = np.ones_like(envelope)

    over_threshold = envelope > DEESS_THRESHOLD
    gain[over_threshold] = 1 / DEESS_RATIO

    smoothed_gain = lfilter([0.1], [1, -0.9], gain)

    return audio * smoothed_gain


def normalize_loudness(audio, sr):
    meter = pyln.Meter(sr)
    loudness = meter.integrated_loudness(audio)
    normalized = pyln.normalize.loudness(audio, loudness, TARGET_LUFS)

    peak = np.max(np.abs(normalized))
    if peak > 0.99:
        normalized = normalized / peak * 0.99

    return normalized


def random_gap(sr):
    duration = random.uniform(GAP_MIN, GAP_MAX)
    return np.zeros(int(duration * sr))


def main():
    if len(sys.argv) < 3:
        print("Usage: python stitch_podcast_pro.py output.mp4 input1.mp4 input2.wav ...")
        sys.exit(1)

    output_file = sys.argv[1]
    input_files = sys.argv[2:]

    temp_dir = tempfile.mkdtemp()
    segments = []

    print("\nProcessing files...\n")

    for i, input_file in enumerate(input_files):
        print(f"→ {input_file}")

        temp_wav = os.path.join(temp_dir, f"temp_{i}.wav")
        convert_to_wav(input_file, temp_wav)

        audio, sr = sf.read(temp_wav)

        print("   Trimming silence...")
        audio = trim_silence(audio)

        print("   High-pass filtering...")
        audio = highpass_filter(audio, sr)

        print("   Applying de-esser...")
        audio = deesser(audio, sr)

        print("   Normalizing to -19 LUFS...")
        audio = normalize_loudness(audio, sr)

        segments.append(audio)

        if i < len(input_files) - 1:
            segments.append(random_gap(sr))

    print("\nConcatenating...")
    final_audio = np.concatenate(segments)

    combined_wav = os.path.join(temp_dir, "final.wav")
    sf.write(combined_wav, final_audio, SAMPLE_RATE)

    print("Encoding final MP4...")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", combined_wav,
        "-c:a", "aac",
        "-b:a", "192k",
        output_file
    ], check=True)

    print(f"\nDone. Podcast exported to {output_file}\n")


if __name__ == "__main__":
    main()