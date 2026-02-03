# Repeatable workflow to generate an LLM newsletter outline on ACCRE

This is a cleaned up walkthrough of my key steps. 

## 1 Connect to the GPU node you are allocated

From your laptop, connect through the local port forward you used

```bash
ssh -p 2222 localhost
```

Sample output

```text
Authorized uses only. All activity may be monitored and reported. Vanderbilt University - Advanced Computing Center for Research & Education
GPU Node - x86_64v4
[<VUID>@<gpu####> ~]$
```

Note
This connection only works when you have an active job on that node

## 2 Enter a shell and activate your Conda environment

```bash
bash
conda activate huggingface
```

Sample output

```text
(huggingface) bash-5.1$
```

## 3 Confirm GPUs are visible

```bash
nvidia-smi
```

Sample output

```text
Tue Feb 3 14:32:28 2026
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 560.35.05 Driver Version: 560.35.05 CUDA Version: 12.6                       |
| GPU  Name            Memory-Usage         GPU-Util                                      |
| 0    NVIDIA RTX A6000 8066MiB / 49140MiB  52%                                          |
+-----------------------------------------------------------------------------------------+
```

This matches the kind of check you ran before launching the model

## 4 Point Hugging Face cache to nobackup

You created a dedicated cache directory and set** **`HF_HOME`

```bash
mkdir -p /nobackup/user/<VUID>/hf
export HF_HOME=/nobackup/user/<VUID>/hf
```

Optional but recommended if you want it set automatically each login
Add the export line to your shell startup file

```bash
nano ~/.bash_profile
```

Then add

```bash
export HF_HOME=/nobackup/user/<VUID>/hf
```

## 5 Authenticate to Hugging Face once per environment

Your history shows a successful login where the token was saved under your** **`HF_HOME`

```bash
huggingface-cli login
```

Sample output

```text
Enter your token (input will not be visible):
Add token as git credential? (Y/n) y
Token is valid (permission: fineGrained).
The token `accre2` has been saved to /nobackup/user/<VUID>/hf/stored_tokens
```

## 6 Prepare the input text file

In your example run, the script read a local** **`newsletter.txt` file

Create or update it in the working directory where you will run the script

```bash
nano newsletter.txt
```

## 7 Run your script from your GitHub scripts directory

You said the script lives in your GitHub scripts directory as** **`makeLLMoutline.py`
From anywhere, run it like this

```bash
python ~/GitHub/scripts/makeLLMoutline.py
```

If the script expects** **`newsletter.txt` in the current directory, run it from the folder that contains** **`newsletter.txt`

```bash
cd ~/newsletter
python ~/GitHub/scripts/makeLLMoutline.py
```

Sample output from a successful run in your history

```text
Loading checkpoint shards: 100%|████████████████████████████████████████████████| 4/4 [00:06<00:00, 1.57s/it]
Device set to use cuda:0
Setting `pad_token_id` to `eos_token_id`:128001 for open-end generation.

Here's a bulleted list summarizing the sections of the newsletter:

• Community Reflections: Gratitude for community support during Winter Storm Fern and highlighting Vanderbilt's efforts in energy and security.
• Upcoming Events:
  - Launch of VALIANT AI calendar
  - VALIANT Deep Dive seminar series
  - Discover AI event on April 24, 2026
• VALIANT Ventures: Updates on researchers and their achievements, including awards and publications.
• VALIANT on the Move: News about travel grants and presentations at international conferences.
• Deeper Dive: Upcoming seminars on AI methods and neurodegenerative disease research.
• Shared Resources: Introduction to VALIANT's shared AI calendar and faculty-only Spring Discussion Series on teaching with AI.
• Research Highlights: Selection of recent publications from the Vanderbilt community.
```

## Quick checklist you can reuse

1. `ssh -p 2222 localhost` into the allocated GPU node
2. `conda activate huggingface`
3. `export HF_HOME=/nobackup/user/<VUID>/hf`
4. `huggingface-cli login` once if needed
5. Put your newsletter text in** **`newsletter.txt`
6. `python ~/GitHub/scripts/makeLLMoutline.py`
