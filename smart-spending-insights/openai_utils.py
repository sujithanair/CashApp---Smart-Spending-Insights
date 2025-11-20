
import os
from dotenv import load_dotenv
import openai
from typing import Dict, Any, Optional

load_dotenv()

def get_openai_api_key() -> str:
    return os.environ.get("OPENAI_API_KEY", "")

def build_prompt(insights: Dict[str, Any]) -> str:
    parts = [
        "Here are analytics from a user's transactions:",
        f"Total spend: ${insights.get('total_spend', 0):,.2f}",
        "Category totals:",
    ]
    for cat, amt in insights.get("categories_ranked", {}).items():
        parts.append(f"- {cat}: ${amt:,.2f}")

    parts.append(f"Biggest category: {insights.get('biggest_category')}")
    parts.append(f"Fastest growing category: {insights.get('fastest_growing_category')}")
    parts.append("\nPlease produce:\n1) Three concise, actionable insights (1-2 sentences each) based on these numbers.\n2) One short practical tip to reduce spending.\nKeep language friendly and succinct.")
    return "\n".join(parts)

def generate_insights_nl(insights: Dict[str, Any], model: Optional[str] = None, max_tokens: int = 300) -> str:
    """Generate human-readable insights using OpenAI ChatCompletion API.

    Requires OPENAI_API_KEY env var. Model defaults to environment variable OPENAI_MODEL or
    "gpt-3.5-turbo" if not provided.
    """
    api_key_local = get_openai_api_key()
    if not api_key_local:
        raise RuntimeError("OPENAI_API_KEY not set in environment")

    client = openai.OpenAI(api_key=api_key_local)
    model = model or os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
    prompt = build_prompt(insights)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that turns numeric spending analytics into concise, actionable human-readable insights for a personal finance app."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=max_tokens,
        temperature=0.7,
    )

    choices = response.choices or []
    if not choices:
        return "(no response)"
    message = choices[0].message
    return message.content.strip()
