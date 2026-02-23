#!/usr/bin/env python3
"""
podcast_from_newsletter.py

Creates a two host podcast script from newsletter.txt using Meta Llama 3.1 8B Instruct,
then renders an audio only mp4 using VibeVoice with two randomly selected different voices
and small random pauses between turns.

Inputs
  newsletter.txt

Outputs
  script.txt
  podcast.mp4

Assumptions
  1) You have VibeVoice repo checked out so demo/realtime_model_inference_from_file.py exists
  2) You have an environment with transformers, torch, and ffmpeg available
  3) You can run the VibeVoice demo script exactly like in your tutorial

Example
  source .venv/bin/activate
  python podcast_from_newsletter.py
"""

import argparse
import json
import os
import random
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import torch
import transformers


DEFAULT_MODEL_ID = "meta-llama/Meta-Llama-3.1-8B-Instruct"
DEFAULT_VIBEVOICE_MODEL = "microsoft/VibeVoice-Realtime-0.5B"

# If your repo supports more names, add them here.
# These are just examples. Keep at least 2.
DEFAULT_SPEAKERS = [
    "Grace_woman",
    "Emma_woman",
    "Olivia_woman",
    "Ava_woman",
    "Sophia_woman",
    "Mia_woman",
    "James_man",
    "John_man",
    "Michael_man",
    "William_man",
    "David_man",
    "Daniel_man",
]


def run(cmd: list[str]) -> None:
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if p.returncode != 0:
        raise RuntimeError(
            "Command failed:\n"
            + " ".join(cmd)
            + "\n\nSTDOUT:\n"
            + (p.stdout or "")
            + "\n\nSTDERR:\n"
            + (p.stderr or "")
        )


def safe_parse_json_list(text: str) -> list[str]:
    try:
        data = json.loads(text)
        if isinstance(data, list) and all(isinstance(x, str) for x in data):
            return data
    except Exception:
        pass

    start = text.find("[")
    end = text.rfind("]")
    if start != -1 and end != -1 and end > start:
        candidate = text[start : end + 1]
        try:
            data = json.loads(candidate)
            if isinstance(data, list) and all(isinstance(x, str) for x in data):
                return data
        except Exception:
            pass

    return []


def build_pipeline(model_id: str, device_map: str) -> transformers.Pipeline:
    return transformers.pipeline(
        "text-generation",
        model=model_id,
        model_kwargs={"dtype": torch.bfloat16},
        device_map=device_map,
    )


def run_chat(
    pipeline: transformers.Pipeline,
    messages: list[dict],
    max_new_tokens: int,
    temperature: float,
    top_p: float,
) -> str:
    outputs = pipeline(
        messages,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=temperature,
        top_p=top_p,
    )
    return outputs[0]["generated_text"][-1]["content"].strip()


def generate_script_from_newsletter(pipeline: transformers.Pipeline, newsletter_text: str) -> str:
    system_context = (
        "You are a helpful assistant working with a single newsletter as the only source of truth.\n"
        "Use only the provided newsletter content. Do not invent facts.\n\n"
        "Newsletter content:\n"
        f"{newsletter_text}"
    )

    topic_messages = [
        {"role": "system", "content": system_context},
        {
            "role": "user",
            "content": (
                "Generate a list of distinct topics covered in the newsletter.\n"
                "Return only a JSON array of strings.\n"
                "Keep it concise, usually 6 to 12 topics.\n"
                "Topics should be specific enough to anchor a short discussion segment.\n"
            ),
        },
    ]

    topics_raw = run_chat(pipeline, topic_messages, max_new_tokens=512, temperature=0.2, top_p=0.9)
    topics = safe_parse_json_list(topics_raw)
    if not topics:
        raise RuntimeError("Could not parse topics as JSON list.\nModel output:\n" + topics_raw)

    all_segments: list[str] = []
    for topic in topics:
        conv_messages = [
            {"role": "system", "content": system_context},
            {
                "role": "user",
                "content": (
                    f"Topic: {topic}\n\n"
                    "Write a brief conversation between HostA and HostB that covers the newsletter material under this topic.\n"
                    "Tone requirements:\n"
                    "HostA is enthusiastic and especially engaged with engineering and medical imaging topics.\n"
                    "HostB is broadly curious and more serious about scientific grand challenges.\n"
                    "Keep it fun but professional. Avoid extensive hyperbole and avoid silly humor.\n"
                    "Do not mention that you are reading a newsletter.\n"
                    "Do not introduce facts not present in the provided text.\n\n"
                    "Format requirements:\n"
                    "Output only dialogue lines.\n"
                    "Each line must start with either 'HostA:' or 'HostB:'.\n"
                    "Aim for 10 to 16 lines total.\n"
                    "End with HostB giving a short thoughtful wrap up.\n"
                ),
            },
        ]
        dialogue = run_chat(pipeline, conv_messages, max_new_tokens=900, temperature=0.5, top_p=0.9)
        all_segments.append(dialogue)

    full_draft = "\n".join(all_segments)

    editor_messages = [
        {"role": "system", "content": system_context},
        {
            "role": "user",
            "content": (
                "You are an editor for a science and engineering podcast.\n\n"
                "You are given a draft script consisting of multiple short dialogue segments "
                "between HostA and HostB. These segments are already in the correct order "
                "and already contain all factual content that is allowed.\n\n"
                "Your task is to merge them into a single, coherent podcast conversation.\n\n"
                "Editorial requirements:\n"
                "Remove all headings, section titles, and topic labels.\n"
                "Tighten the dialogue and remove redundancy.\n"
                "Smooth transitions so the conversation flows naturally from idea to idea.\n"
                "Preserve the original tone and roles.\n"
                "Do NOT add new facts, examples, or details.\n"
                "Do NOT invent context that is not already present.\n"
                "Do NOT mention newsletters, outlines, or topics.\n\n"
                "Structural requirements:\n"
                "Begin with a brief opening line by HostA such as:\n"
                "\"Welcome to the VALIANT Effort podcast.\"\n"
                "Keep the format as dialogue only.\n"
                "Each line must begin with either \"HostA:\" or \"HostB:\".\n"
                "Maintain a conversational rhythm suitable for audio.\n"
                "End with HostB giving a short, thoughtful wrap up.\n\n"
                "Length requirement:\n"
                "Shorten the overall conversation to approximately 1200 words total.\n\n"
                "Here is the draft script to edit:\n\n"
                f"{full_draft}"
            ),
        },
    ]

    final_script = run_chat(pipeline, editor_messages, max_new_tokens=5000, temperature=0.3, top_p=0.9)
    return final_script.strip()


def parse_dialogue_lines(script_text: str) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for raw in script_text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("HostA:"):
            pairs.append(("HostA", line[len("HostA:") :].strip()))
        elif line.startswith("HostB:"):
            pairs.append(("HostB", line[len("HostB:") :].strip()))
        else:
            # ignore anything that is not properly formatted
            continue
    return pairs


def pick_two_distinct_voices(voices: list[str]) -> tuple[str, str]:
    if len(voices) < 2:
        raise ValueError("Need at least two voices in the voices list.")
    a = random.choice(voices)
    b = random.choice([v for v in voices if v != a])
    return a, b


def vibevoice_render_utterance(
    vibevoice_demo_py: Path,
    vibevoice_model_path: str,
    speaker_name: str,
    text: str,
    out_dir: Path,
    idx: int,
) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    txt_path = out_dir / f"utt_{idx:04d}.txt"
    txt_path.write_text(text + "\n", encoding="utf-8")

    # The demo script decides its own output name(s) inside output_dir.
    # We run it into a per utterance folder, then pick the newest audio file produced.
    utt_dir = out_dir / f"utt_{idx:04d}_render"
    utt_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable,
        str(vibevoice_demo_py),
        "--model_path",
        vibevoice_model_path,
        "--txt_path",
        str(txt_path),
        "--speaker_name",
        speaker_name,
        "--output_dir",
        str(utt_dir),
    ]
    run(cmd)

    audio_candidates = []
    for ext in (".wav", ".mp3", ".flac", ".m4a", ".aac", ".ogg"):
        audio_candidates.extend(utt_dir.rglob(f"*{ext}"))

    if not audio_candidates:
        raise RuntimeError(f"No audio file produced for utterance {idx} in {utt_dir}")

    audio_candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return audio_candidates[0]


def ffmpeg_concat_with_silences(audio_paths: list[Path], silence_seconds: list[float], out_mp4: Path) -> None:
    if len(audio_paths) == 0:
        raise ValueError("No audio paths to concatenate.")
    if len(silence_seconds) != len(audio_paths) - 1:
        raise ValueError("silence_seconds must be one less than audio_paths length.")

    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        concat_list = td_path / "concat.txt"
        lines = []

        def normalize_to_wav(src: Path, dst: Path) -> Path:
            run(["ffmpeg", "-y", "-i", str(src), "-ac", "1", "-ar", "24000", str(dst)])
            return dst

        wavs: list[Path] = []
        for i, ap in enumerate(audio_paths):
            w = td_path / f"seg_{i:04d}.wav"
            wavs.append(normalize_to_wav(ap, w))

        silence_wavs: list[Path] = []
        for i, s in enumerate(silence_seconds):
            sw = td_path / f"sil_{i:04d}.wav"
            run(
                [
                    "ffmpeg",
                    "-y",
                    "-f",
                    "lavfi",
                    "-i",
                    f"anullsrc=r=24000:cl=mono",
                    "-t",
                    f"{s:.3f}",
                    str(sw),
                ]
            )
            silence_wavs.append(sw)

        for i, w in enumerate(wavs):
            lines.append(f"file '{w.as_posix()}'\n")
            if i < len(silence_wavs):
                lines.append(f"file '{silence_wavs[i].as_posix()}'\n")

        concat_list.write_text("".join(lines), encoding="utf-8")

        out_wav = td_path / "podcast.wav"
        run(
            [
                "ffmpeg",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_list),
                "-c",
                "copy",
                str(out_wav),
            ]
        )

        # Wrap audio into mp4 container
        run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(out_wav),
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                str(out_mp4),
            ]
        )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--newsletter", default="newsletter.txt")
    ap.add_argument("--script_out", default="script.txt")
    ap.add_argument("--podcast_out", default="podcast.mp4")

    ap.add_argument("--llm_model", default=DEFAULT_MODEL_ID)
    ap.add_argument("--device_map", default="auto")

    ap.add_argument("--vibevoice_model_path", default=DEFAULT_VIBEVOICE_MODEL)
    ap.add_argument(
        "--vibevoice_demo",
        default="demo/realtime_model_inference_from_file.py",
        help="Path to VibeVoice demo script",
    )
    ap.add_argument(
        "--voices",
        default="",
        help="Optional comma separated list of speaker names. If empty, uses built in defaults.",
    )

    ap.add_argument("--min_pause", type=float, default=0.18)
    ap.add_argument("--max_pause", type=float, default=0.55)
    ap.add_argument("--seed", type=int, default=0)

    args = ap.parse_args()

    if args.seed != 0:
        random.seed(args.seed)

    newsletter_path = Path(args.newsletter)
    if not newsletter_path.exists():
        raise FileNotFoundError(f"Missing input file: {newsletter_path}")

    newsletter_text = newsletter_path.read_text(encoding="utf-8")

    voices = DEFAULT_SPEAKERS
    if args.voices.strip():
        voices = [v.strip() for v in args.voices.split(",") if v.strip()]
    hosta_voice, hostb_voice = pick_two_distinct_voices(voices)

    pipeline = build_pipeline(args.llm_model, args.device_map)

    final_script = generate_script_from_newsletter(pipeline, newsletter_text)
    Path(args.script_out).write_text(final_script + "\n", encoding="utf-8")

    pairs = parse_dialogue_lines(final_script)
    if not pairs:
        raise RuntimeError("No dialogue lines parsed. Ensure the script has HostA: and HostB: lines.")

    vibevoice_demo_py = Path(args.vibevoice_demo)
    if not vibevoice_demo_py.exists():
        raise FileNotFoundError(f"Could not find VibeVoice demo script at: {vibevoice_demo_py}")

    render_root = Path("podcast_render_tmp")
    if render_root.exists():
        # avoid accidental reuse of stale segments
        for p in sorted(render_root.rglob("*"), reverse=True):
            try:
                if p.is_file():
                    p.unlink()
                else:
                    p.rmdir()
            except Exception:
                pass
    render_root.mkdir(parents=True, exist_ok=True)

    audio_paths: list[Path] = []
    for idx, (who, text) in enumerate(pairs, start=1):
        speaker = hosta_voice if who == "HostA" else hostb_voice
        # remove any weird whitespace to keep TTS stable
        cleaned = re.sub(r"\s+", " ", text).strip()
        audio_path = vibevoice_render_utterance(
            vibevoice_demo_py=vibevoice_demo_py,
            vibevoice_model_path=args.vibevoice_model_path,
            speaker_name=speaker,
            text=cleaned,
            out_dir=render_root,
            idx=idx,
        )
        audio_paths.append(audio_path)

    # random small pauses between turns
    pauses: list[float] = []
    for _ in range(len(audio_paths) - 1):
        pauses.append(random.uniform(args.min_pause, args.max_pause))

    out_mp4 = Path(args.podcast_out)
    ffmpeg_concat_with_silences(audio_paths, pauses, out_mp4)

    print("Done")
    print(f"HostA voice: {hosta_voice}")
    print(f"HostB voice: {hostb_voice}")
    print(f"Wrote script: {args.script_out}")
    print(f"Wrote audio:  {args.podcast_out}")


if __name__ == "__main__":
    main()
