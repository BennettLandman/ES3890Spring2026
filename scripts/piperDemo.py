import os
import re
import subprocess
from pydub import AudioSegment

SCRIPT_FILE = "script.txt"
OUTPUT_FILE = "valiant_podcast.wav"

PIPER_PATH = "./piper"

HOST_A_MODEL = "en_US-lessac-high.onnx"
HOST_B_MODEL = "en_US-ryan-high.onnx"

def enhance(text):
    text = re.sub(r"\.\s+", "... ", text)
    text = re.sub(r"\?\s+", "? ... ", text)
    text = re.sub(r"!\s+", "! ... ", text)
    return text.strip()

def parse_script(file_path):
    segments = []
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("HostA:"):
            segments.append(("HostA", line.replace("HostA:", "").strip()))
        elif line.startswith("HostB:"):
            segments.append(("HostB", line.replace("HostB:", "").strip()))
        else:
            segments.append(("HostA", line))

    return segments

def generate_tts(text, model, output_file):
    subprocess.run(
        f'echo "{text}" | {PIPER_PATH} --model {model} --output_file {output_file}',
        shell=True,
        check=True
    )

def main():
    segments = parse_script(SCRIPT_FILE)
    combined = AudioSegment.empty()

    for i, (speaker, text) in enumerate(segments):
        print(f"Generating {speaker}...")
        enhanced = enhance(text)

        temp_file = f"temp_{i}.wav"
        model = HOST_A_MODEL if speaker == "HostA" else HOST_B_MODEL

        generate_tts(enhanced, model, temp_file)

        audio = AudioSegment.from_file(temp_file)
        combined += audio
        combined += AudioSegment.silent(duration=350)

        os.remove(temp_file)

    combined.export(OUTPUT_FILE, format="wav")
    print(f"\nNeural podcast created locally: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
