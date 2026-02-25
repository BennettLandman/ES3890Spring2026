# Podcast Audio Stitching Tutorial

This tutorial demonstrates how to merge multiple audio files into a polished podcast style output using a Python pipeline.

The script performs:

* Silence trimming
* High pass filtering to remove low frequency rumble
* De-essing to reduce harsh sibilance
* Loudness normalization to podcast standard
* Randomized pauses between speakers
* Mono conversion at 48 kHz
* AAC encoded output

This produces a clean, broadcast ready spoken word result.

---

## Files in This Directory

* `mergeAudio.py`
* `audio1.m4a`
* `audio2.m4a`
* `audio3.m4a`

Example input files:

* [audio1.m4a](audio1.m4a)
* [audio2.m4a](audio1.m4a)
* [audio3.m4a](audio1.m4a)

The output file in this tutorial example is:

* [merge.m4a](merge.m4a)

---

## What The Script Does

For each input file:

1. Converts to mono 48 kHz WAV
2. Trims leading and trailing silence
3. Applies high pass filter at 80 Hz
4. Applies a gentle de-esser
5. Normalizes to −19 LUFS mono podcast standard
6. Applies peak limiting
7. Inserts a small randomized pause between clips
8. Concatenates and exports to AAC

This workflow is appropriate for:

* Academic podcast production
* Lecture stitching
* Interview editing
* Clean spoken word narration

---

## Installation

Install required packages:

<pre class="overflow-visible! px-0!" data-start="1549" data-end="1605"><div class="relative w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-6 bottom-6"><div class="sticky z-1!"><div class="bg-token-bg-elevated-secondary sticky"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>pip install numpy soundfile pyloudnorm scipy</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

Install ffmpeg:

<pre class="overflow-visible! px-0!" data-start="1624" data-end="1655"><div class="relative w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-6 bottom-6"><div class="sticky z-1!"><div class="bg-token-bg-elevated-secondary sticky"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>brew install ffmpeg</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

or on Linux:

<pre class="overflow-visible! px-0!" data-start="1671" data-end="1706"><div class="relative w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-6 bottom-6"><div class="sticky z-1!"><div class="bg-token-bg-elevated-secondary sticky"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span class="ͼs">sudo</span><span> apt install ffmpeg</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

---

## Usage

From inside this directory:

<pre class="overflow-visible! px-0!" data-start="1752" data-end="1827"><div class="relative w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-6 bottom-6"><div class="sticky z-1!"><div class="bg-token-bg-elevated-secondary sticky"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>python mergeAudio.py merge.m4a audio1.m4a audio2.m4a audio3.m4a</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

This will create:

<pre class="overflow-visible! px-0!" data-start="1848" data-end="1869"><div class="relative w-full my-4"><div class=""><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border corner-superellipse/1.1 border-token-border-light bg-token-bg-elevated-secondary rounded-3xl"><div class="pointer-events-none absolute inset-x-4 top-12 bottom-4"><div class="pointer-events-none sticky z-40 shrink-0 z-1!"><div class="sticky bg-token-border-light"></div></div></div><div class="pointer-events-none absolute inset-x-px top-6 bottom-6"><div class="sticky z-1!"><div class="bg-token-bg-elevated-secondary sticky"></div></div></div><div class="corner-superellipse/1.1 rounded-3xl bg-token-bg-elevated-secondary"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼk ͼy"><div class="cm-scroller"><div class="cm-content q9tKkq_readonly"><span>merge.m4a</span></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></pre>

in the same folder.

---

## Podcast Standard Used

* Mono output
* 48 kHz sample rate
* −19 LUFS integrated loudness
* AAC 192 kbps

This matches common spoken word distribution standards for mono podcasts.

---

## Why These Steps Matter

Silence trimming
Prevents long dead air between clips.

High pass filtering
Removes microphone rumble and low frequency noise.

De-essing
Reduces harsh s and sh sounds in the 5 to 10 kHz range.

LUFS normalization
Balances perceived loudness between speakers.

Randomized pauses
Creates natural conversational pacing rather than abrupt edits.

---

## Suggested Extensions

You may extend this pipeline to include:

* Background music ducking
* Adaptive silence detection
* Crossfades instead of hard joins
* Chapter markers
* Automatic intro and outro fades
* Breath reduction rather than full silence removal

---

## Intended Use

This tutorial is designed for use in the Tutorials section of this repository as an example of:

* Practical digital signal processing
* Podcast post production automation
* Applied audio normalization
* End to end Python plus ffmpeg workflow
