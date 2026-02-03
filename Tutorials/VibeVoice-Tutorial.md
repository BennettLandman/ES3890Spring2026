# VibeVoice Setup and Text to Speech Generation Tutorial

## Overview

This tutorial shows how to set up Microsoft’s VibeVoice and generate speech from text using different speaker voices on an Ubuntu system with NVIDIA GPU support.

## Prerequisites

* Ubuntu 22.04 or newer with NVIDIA GPU (tested on RTX 6000 Ada)
* SSH access to a compatible server
* Python 3.10 or newer
* CUDA 12.1 compatible system

## Step by Step Setup

### 1. Connect to Server and Create Working Directory

<pre class="overflow-visible! px-0!" data-start="706" data-end="782"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(var(--sticky-padding-top)+9*var(--spacing))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>ssh your_server.domain.edu
</span><span>cd</span><span> /tmp
</span><span>mkdir</span><span> landmaba && </span><span>cd</span><span> landmaba
</span></span></code></div></div></pre>

### 2. Create Python Virtual Environment

<pre class="overflow-visible! px-0!" data-start="826" data-end="885"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(var(--sticky-padding-top)+9*var(--spacing))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>python3 -m venv .venv
</span><span>source</span><span> .venv/bin/activate
</span></span></code></div></div></pre>

### 3. Install Flash Attention (Critical for Performance)

<pre class="overflow-visible! px-0!" data-start="946" data-end="1027"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(var(--sticky-padding-top)+9*var(--spacing))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>pip install flash-attn --no-build-isolation
pip install --upgrade pip
</span></span></code></div></div></pre>

### 4. Clone VibeVoice Repository

<pre class="overflow-visible! px-0!" data-start="1064" data-end="1141"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(var(--sticky-padding-top)+9*var(--spacing))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>git </span><span>clone</span><span> https://github.com/microsoft/VibeVoice.git
</span><span>cd</span><span> VibeVoice
</span></span></code></div></div></pre>

### 5. Install Core Dependencies

<pre class="overflow-visible! px-0!" data-start="1177" data-end="1288"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(var(--sticky-padding-top)+9*var(--spacing))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>pip install -U transformers accelerate scipy soundfile </span><span>"pandas<3"</span><span></span><span>"scikit-learn<2"</span><span>
pip install -e .
</span></span></code></div></div></pre>

## Generate Speech from Text

### Basic Usage (Pre built Voices)

<pre class="overflow-visible! px-0!" data-start="1356" data-end="1568"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(var(--sticky-padding-top)+9*var(--spacing))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>python demo/realtime_model_inference_from_file.py \
  --model_path microsoft/VibeVoice-Realtime-0.5B \
  --txt_path demo/text_examples/1p_abs.txt \
  --speaker_name Carter \
  --output_dir ./audio_out
</span></span></code></div></div></pre>

### Parameters

* `--model_path`
  Use** **`microsoft/VibeVoice-Realtime-0.5B` (recommended for stability)
* `--txt_path`
  Path to text file to synthesize
* `--speaker_name`
  Speaker voice (e.g., Carter, Grace_woman, Emma_woman)
* `--output_dir`
  Directory to save generated audio
* `--device`
  Specify device:** **`cuda`,** **`mps`, or** **`cpu` (default: cuda)
* `--cfg_scale`
  Generation guidance scale (default: 1.5)

## Available Built in Voices

**English**

* Carter
* Davis
* Emma
* Frank
* Grace
* Mike

**German**

* Spk0 (man)
* Spk1 (woman)

**French**

* Spk0 (man)
* Spk1 (woman)

**Other languages available**
Japanese, Korean, Dutch, Polish, Portuguese, Spanish

## Download Additional Experimental Voices

<pre class="overflow-visible! px-0!" data-start="2324" data-end="2386"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(var(--sticky-padding-top)+9*var(--spacing))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>cd</span><span> demo
bash download_experimental_voices.sh
</span><span>cd</span><span> ..
</span></span></code></div></div></pre>

## Output

* Generated audio files are saved to** **`--output_dir` as** **`.wav` files
* Audio quality: 16 kHz mono, optimized for voice synthesis
* Generation time: typically 0.25x to 0.33x real time factor

## Troubleshooting

### If Using 1.5B Model Causes Tensor Size Errors

Use the 0.5B model instead. It is more stable and still produces high quality output.

### If Audio File Conversion Is Needed (e.g., m4a to wav)

<pre class="overflow-visible! px-0!" data-start="2812" data-end="2894"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(var(--sticky-padding-top)+9*var(--spacing))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>sudo</span><span> apt install ffmpeg
ffmpeg -i input.m4a -ac 1 -ar 16000 output.wav
</span></span></code></div></div></pre>

## Key Points to Remember

* Use** **`microsoft/VibeVoice-Realtime-0.5B` for best stability
* Install** **`flash-attn` for GPU optimization
* Text files should be UTF 8 encoded
* GPU with 24 GB or more VRAM recommended
* Output audio is WAV format at 16 kHz

## Example Workflow

<pre class="overflow-visible! px-0!" data-start="3178" data-end="3460"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(var(--sticky-padding-top)+9*var(--spacing))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span># Activate environment</span><span>
</span><span>source</span><span> .venv/bin/activate

</span><span># Generate speech</span><span>
python demo/realtime_model_inference_from_file.py \
  --model_path microsoft/VibeVoice-Realtime-0.5B \
  --txt_path demo/text_examples/1p_abs.txt \
  --speaker_name Grace_woman \
  --output_dir ./output
</span></span></code></div></div></pre>

Output file:

<pre class="overflow-visible! px-0!" data-start="3476" data-end="3517"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(var(--sticky-padding-top)+9*var(--spacing))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-text"><span><span>./output/1p_abs_generated.wav
</span></span></code></div></div></pre>
