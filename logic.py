# logic.py

import pandas as pd

# Load your CSV file into a DataFrame
SUPPLEMENT_DATA_PATH = "data/supplements.csv"

def load_supplement_data():
    """Reads the supplements CSV file into a pandas DataFrame."""
    return pd.read_csv(SUPPLEMENT_DATA_PATH)

def get_recommendations(user_input):
    """
    Returns a list of supplements based on the user_input from the quiz.
    :param user_input: dictionary of quiz responses
    :return: list of dictionaries with supplement details
    """
    df = load_supplement_data()
    
    # Map quiz answers to tags (you can expand this list as needed)
    answer_to_tags = {
    "sleep_quality": {
        "poor": ["sleep"],
        "average": ["sleep"]
    },
    "sleep_issues": {
        "falling_asleep": ["falling_asleep"],
        "waking_up": ["sleep"],
        "waking_early": ["sleep"],
        "racing_mind": ["anxious_mind", "stress"]
    },
    "caffeine": {
        "medium": ["sleep", "stress"],
        "high": ["sleep", "stress"]
    },
    "stress_level": {
        "high": ["stress"]
    },
    "stress_response": {
        "mental": ["anxious_mind", "focus"],
        "muscle": ["muscle_tension", "stress"],
        "fatigue": ["fatigue", "energy"],
        "digestive": ["digestion", "bloating", "gut"],
        "mood": ["mood", "hormone_balance"]
    },
    "relaxation": {
        "none": ["stress"],
        "meditation": ["stress_relief"],
        "yoga": ["stress_relief", "recovery"],
        "journaling": ["stress_relief"]
    },
    "energy_peak": {
        "rarely": ["energy", "fatigue"]
    },
    "energy_crash": {
        "yes": ["energy", "fatigue"]
    },
    "exercise_frequency": {
        "3_to_5": ["recovery"],
        "daily": ["recovery", "energy"]
    },
    "exercise_type": {
        "strength": ["muscle_tension", "recovery"],
        "cardio": ["energy", "recovery"],
        "yoga": ["recovery", "stress_relief"]
    },
    "diet": {
        "vegan": ["vegan", "b12", "iron", "omega-3"],
        "vegetarian": ["b12", "iron", "omega-3"]
    },
    "diet_restrictions": {
        "red_meat": ["iron"],
        "fish": ["omega-3"],
        "dairy": ["digestive_support"],
        "gluten": ["digestive_support"]
    },
    "bowel_issues": {
        "yes": ["digestion", "bloating"],
        "sometimes": ["digestion", "bloating"]
    },
    "hormonal_issues": {
        "yes": ["hormone_balance", "pms"],
        "sometimes": ["hormone_balance", "pms"]
    },
    "birth_control": {
        "yes": ["hormone_balance", "nutrient_depletion"]
    },
    "skin_concerns": {
        "acne": ["acne", "skin"],
        "dryness": ["skin", "hydration", "omega-3"],
        "redness": ["skin", "omega-3", "anti_inflammatory"],
        "dullness": ["skin", "collagen", "aging"]
    },
    "sunlight_exposure": {
        "rarely": ["low_sunlight", "vitamin_d", "immunity"]
    },
    "shift_work": {
        "yes": ["circadian_rhythm", "sleep", "stress"]
    },
    "wellness_goals": {
        "immune_support": ["immunity"],
        "balance_hormones": ["hormone_balance"],
        "boost_energy": ["energy", "focus"],
        "focus_brain": ["focus"],
        "longevity": ["aging"],
        "skin_health": ["skin"]
    },
    "routine_focus": {
        "fast_acting": ["adaptogens", "stress_relief"],
        "long_term": ["longevity", "preventative"],
        "balanced": ["adaptogens", "preventative", "longevity"]
    },
    "screen_time": {
        "always": ["sleep", "circadian_rhythm"],
        "sometimes": ["circadian_rhythm"]
    },
    "daily_screen_hours": {
        "over_8": ["sleep", "stress"],
        "4_to_8": ["stress"]
    },
    "plant_based_preference": {
        "yes": ["plant_based"],
        "no_preference": [],
        "open_to_all": []
    },
    "supplement_consistency": {
        "struggle": ["simplicity"],
        "somewhat_consistent": ["simplicity"]
    },
    
}


    matched_tags = []

    # Loop through the user inputs and collect matching tags
    for question, answer in user_input.items():
        if question in answer_to_tags:
            question_mapping = answer_to_tags[question]
            if answer in question_mapping:
                matched_tags.extend(question_mapping[answer])


    # Remove duplicates
    matched_tags = list(set(matched_tags))

    # Count tag matches for each supplement
    supplement_scores = []

    for _, row in df.iterrows():
        supplement_tags = [tag.strip() for tag in row['tags'].split(",")]
        match_count = sum(1 for tag in supplement_tags if tag in matched_tags)

        if match_count > 0:
            supplement_scores.append({
                "name": row["name"],
                "category": row["category"],
                "benefit": row["benefit"],
                "usage": row["usage"],
                "notes": row["notes"],
                "match_count": match_count
            })

    # Sort supplements by number of matching tags (highest first)
    supplement_scores.sort(key=lambda x: x["match_count"], reverse=True)

    # Handle routine_style logic
    routine_style = user_input.get("routine_style", "balanced")  # default to balanced if not specified

    if routine_style == "minimal":
        supplement_scores = supplement_scores[:3]
    elif routine_style == "balanced":
        supplement_scores = supplement_scores[:5]
    elif routine_style == "comprehensive":
        supplement_scores = supplement_scores  # no limit
    elif routine_style == "targeted":
        # Only keep supplements with 2 or more matching tags
        supplement_scores = [supp for supp in supplement_scores if supp["match_count"] >= 2]

    # Remove match_count from the final output
    recommended_supplements = []
    for supp in supplement_scores:
        supp.pop("match_count")  # remove internal scoring field
        recommended_supplements.append(supp)

    return recommended_supplements



if __name__ == "__main__":
    # Test the recommendation system with fake inputs
    sample_input = {
        "sleep_quality": "poor",
        "sleep_issues": "falling_asleep",
        "diet": "vegan",
        "routine_style": "balanced"
    }

    recs = get_recommendations(sample_input)
    print("Recommended Supplements:")
    for rec in recs:
        print(f"{rec['name']} - {rec['benefit']} - {rec['usage']}")
