import os
import openai
from dotenv import load_dotenv
import json

load_dotenv()  # Load environment variables from .env
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_ai_explanations(user_input, recommendations):
    """
    Uses the OpenAI API to generate personalized explanations for the supplement plan.
    Returns a list of JSON objects: [{"name": ..., "explanation": ...}, ...]
    """
    # Build the user context summary
    user_context = []
    for key, value in user_input.items():
        if value:
            formatted_key = key.replace('_', ' ').capitalize()
            user_context.append(f"{formatted_key}: {value}")
    user_summary = "\n".join(user_context)

    # Build the supplement list
    supplement_list = ", ".join([rec["name"] for rec in recommendations])

    # Create the AI prompt asking for JSON output
    prompt = (
        f"The user has shared the following health and lifestyle information:\n"
        f"{user_summary}\n\n"
        f"The recommended supplements are: {supplement_list}.\n\n"
        f"Output a JSON array where each object has:\n"
        f"1. 'name': the exact name of the supplement from the list\n"
        f"2. 'explanation': a concise, science-backed explanation of why this supplement was recommended.\n\n"
        f"Example format:\n"
        f"[{{\"name\": \"Magnesium Glycinate\", \"explanation\": \"Explanation here.\"}}, ...]\n\n"
        f"Do not add numbering, markdown, or any text outside the JSON array."
    )

    try:
        # OpenAI API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful, science-backed health and wellness assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        ai_output = response.choices[0].message.content.strip()

        # Parse the JSON response
        explanations_json = json.loads(ai_output)
        return explanations_json

    except Exception as e:
        print("Error with OpenAI API:", e)
        return [{"name": rec["name"], "explanation": "There was an error generating the explanation."} for rec in recommendations]

if __name__ == "__main__":
    # Optional test run
    test_input = {"sleep_quality": "poor", "diet": "vegan", "routine_style": "balanced"}
    test_recommendations = [
        {"name": "Magnesium Glycinate", "benefit": "Supports relaxation & sleep", "usage": "200–400mg before bed", "notes": ""},
        {"name": "L-Theanine", "benefit": "Promotes calm focus", "usage": "100–200mg as needed", "notes": ""}
    ]
    explanations = generate_ai_explanations(test_input, test_recommendations)
    print(explanations)
