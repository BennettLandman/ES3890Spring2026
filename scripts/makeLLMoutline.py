
import transformers
import torch

#model_id = "meta-llama/Llama-3.3-70B-Instruct"
model_id = "meta-llama/Meta-Llama-3.1-8B-Instruct"
# Load newsletter text
with open("newsletter.txt", "r", encoding="utf-8") as f:
    newsletter_text = f.read()

pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto",
)

messages = [
    {
        "role": "system",
        "content": (
            "You are tasked with summarizing newsletters. \n\n" 
            "Here is background context from a newsletter that you should use "
            "when responding:\n\n"
            f"{newsletter_text}"
        ),
    },
    {
        "role": "user",
        "content": "Provide a simple bulleted listed that summarizes the sections of the newsletter",
    },
]

outputs = pipeline(
    messages,
    max_new_tokens=2560,
)

response = outputs[0]["generated_text"][-1]["content"].strip()
print("\n" + response + "\n")

