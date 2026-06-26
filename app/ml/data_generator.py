from google import genai
from google.genai import errors
import json
import time
from app.core.config import Settings
settings = Settings()

client = genai.Client(api_key=settings.GEMINI_API_KEY)

CLASSES = ["factual", "research", "comparison", "how_to", "news"]

def generate_examples(intent: str, count: int = 100) -> list[str]:
    prompt = f"""Generate exactly {count} different search engine queries that represent the intent: "{intent}".

Rules:
- One query per line
- No numbering, no bullets, no extra text
- Vary the phrasing and topics
- Make them realistic search queries a real user would type

Intent definitions:
- factual: simple questions with a direct answer
- research: questions needing deep explanation
- comparison: questions comparing two or more things
- how_to: questions asking for steps or instructions
- news: questions about recent events or updates
"""
    for attempt in range(3):
        try:
            response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt
             )
        
            lines = response.text.strip().split("\n")
            return [line.strip() for line in lines if line.strip()]

        except errors.ClientError as e:
            if "429" in str(e):
                wait = 60 * (attempt + 1)
                print(f"  Rate limit hit. Waiting {wait}s...")
                time.sleep(wait)
            else:
                raise
    return []


def build_dataset():
    dataset = []

    for intent in CLASSES:
        print(f"Generating examples for: {intent}...")
        examples = generate_examples(intent, count=100)

        for text in examples:
            dataset.append({"text": text, "label": intent})

        print(f"  Got {len(examples)} examples")
        time.sleep(2)

    with open("app/ml/training_data.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Total examples: {len(dataset)}")


if __name__ == "__main__":
    build_dataset()