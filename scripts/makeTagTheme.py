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

def run_chat(messages, max_new_tokens=512, temperature=0.3, top_p=0.9):
    outputs = pipeline(
        messages,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=temperature,
        top_p=top_p,
    )
    return outputs[0]["generated_text"][-1]["content"].strip()


system_context = (
    "You are a helpful assistant working with a single newsletter as the only source of truth.\n"
    "Use only the provided newsletter content. Do not invent facts.\n\n"
    "Newsletter content:\n"
    f"{newsletter_text}"
)

tag_theme_messages = [
    {
        "role": "system",
        "content": system_context,
    },
    {
        "role": "user",
        "content": (
            "Generate podcast metadata based only on the newsletter content.\n\n"
            "Requirements:\n"
            "- Create 8 to 15 concise tags.\n"
            "- Tags should be specific, relevant, and useful for podcast discovery.\n"
            "- Avoid redundancy.\n"
            "- Create exactly one single-sentence theme capturing the central idea.\n"
            "- The theme must be one sentence only.\n\n"
            "Output format EXACTLY as:\n"
            "Tags: tag1, tag2, tag3\n"
            "Theme: single sentence theme\n\n"
            "Do not include anything else.\n"
        ),
    },
]

result = run_chat(tag_theme_messages, max_new_tokens=512, temperature=0.2, top_p=0.9)

print(result)