from flask import Flask, render_template, request
from logic import get_recommendations
from ai_helper import generate_ai_explanations

app = Flask(__name__)

# Route for quiz form
@app.route("/")
def index():
    return render_template("index.html")

# Route for quiz submission and showing results
@app.route("/results", methods=["POST"])
def results():
    # Collect user input from the form
    user_input = {
        key: (request.form.get(key).strip().lower() if request.form.get(key) else None)
        for key in [
            "sleep_quality", "sleep_issues", "caffeine", "stress_level", "stress_response",
            "relaxation", "energy_peak", "energy_crash", "exercise_frequency", "exercise_type",
            "diet", "diet_restrictions", "bowel_issues", "hormonal_issues", "birth_control",
            "skin_concerns", "sunlight_exposure", "shift_work", "wellness_goals",
            "routine_focus", "screen_time", "daily_screen_hours", "plant_based_preference",
            "supplement_consistency", "routine_style"
        ]
    }

    print("User Input Received:", user_input)

    # Get supplement recommendations based on inputs
    recommendations = get_recommendations(user_input)
    print("Generated Recommendations:", recommendations)

    # Use AI to generate structured JSON explanations
    ai_explanations = generate_ai_explanations(user_input, recommendations)
    print("\n--- AI EXPLANATIONS JSON ---")
    print(ai_explanations)

    # Combine recommendations with their matching explanations (match by supplement name)
    combined = []
    for rec in recommendations:
        matching_expl = next(
            (e['explanation'] for e in ai_explanations if e['name'].lower() == rec['name'].lower()),
            "No explanation found."
        )
        combined.append({
            "name": rec["name"],
            "category": rec["category"],
            "benefit": rec["benefit"],
            "usage": rec["usage"],
            "notes": rec["notes"],
            "explanation": matching_expl
        })

    return render_template("results.html", results=combined)

if __name__ == "__main__":
    app.run(debug=True)

