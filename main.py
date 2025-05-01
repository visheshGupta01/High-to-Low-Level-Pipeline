from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

MODEL_NAME = "google/flan-t5-large"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

def generate_response(prompt: str, max_new_tokens: int = 512) -> str:
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.7,
            num_beams=4,
            repetition_penalty=1.1
        )
    return tokenizer.decode(output[0], skip_special_tokens=True)

def analyze_requirement(requirement: str) -> dict:
    requirement = requirement.strip()
    if not requirement:
        raise ValueError("Requirement is empty.")

    modules_prompt = f"What are the main modules in this software system: '{requirement}'?"
    schema_prompt = f"Design the database schema for this system: '{requirement}'. Output in JSON-like format."
    pseudocode_prompt = f"Write pseudocode for the core features of this requirement: '{requirement}'."

    modules = generate_response(modules_prompt)
    schema = generate_response(schema_prompt)
    pseudocode = generate_response(pseudocode_prompt)

    return {
        "modules": modules,
        "schemas": schema,
        "pseudocode": pseudocode
    }

if __name__ == "__main__":
    requirement = input("Enter High Level Requirement")
    result = analyze_requirement(requirement)
    print("\nModules")
    print(result["modules"])
    print("\nSchemas")
    print(result["schemas"])
    print("\nPseudocode")
    print(result["pseudocode"])
