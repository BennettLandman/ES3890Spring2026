import json
import transformers
import torch


model_id = "meta-llama/Meta-Llama-3.1-8B-Instruct"

# Load newsletter text
with open("newsletter.txt", "r", encoding="utf-8") as f:
    newsletter_text = f.read()

pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"dtype": torch.bfloat16},
    device_map="auto",
)

def run_chat(messages, max_new_tokens=1024, temperature=0.4, top_p=0.9):
    outputs = pipeline(
        messages,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=temperature,
        top_p=top_p,
    )
    return outputs[0]["generated_text"][-1]["content"].strip()

def safe_parse_json_list(text):
    """
    Expect a JSON array of strings.
    Tries strict parse first, then tries to extract the first JSON array in the text.
    """
    try:
        data = json.loads(text)
        if isinstance(data, list) and all(isinstance(x, str) for x in data):
            return data
    except Exception:
        pass

    # Fallback: extract first [...] block
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


system_context = (
    "You are a helpful assistant working with a single newsletter as the only source of truth.\n"
    "Use only the provided newsletter content. Do not invent facts.\n\n"
    "Newsletter content:\n"
    f"{newsletter_text}"
)

# Pass 1: get topics
topic_messages = [
    {
        "role": "system",
        "content": system_context,
    },
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

topics_raw = run_chat(topic_messages, max_new_tokens=512, temperature=0.2, top_p=0.9)
topics = safe_parse_json_list(topics_raw)

if not topics:
    raise RuntimeError(
        "Could not parse topics as a JSON list. Model output was:\n\n" + topics_raw
    )

# Pass 2: conversation per topic
all_segments = []
for i, topic in enumerate(topics, start=1):
    conv_messages = [
        {
            "role": "system",
            "content": system_context,
        },
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

    dialogue = run_chat(conv_messages, max_new_tokens=900, temperature=0.5, top_p=0.9)
    all_segments.append((topic, dialogue))

# Print results
print("\nTOPICS\n")
for t in topics:
    print(f"* {t}")

print("\n\nCONVERSATIONS\n")
for topic, dialogue in all_segments:
    print(f"\n=== {topic} ===\n")
    print(dialogue)
