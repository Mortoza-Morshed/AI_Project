from flask import Flask, request, jsonify
import google.generativeai as genai

genai.configure(api_key="*google-api*")  

app = Flask(__name__)

ALLOWED_TOPICS = {
    "nutrition", "diet", "meal", "fitness", "mental", "health", "sleep", "exercise", 
    "wellness", "hydration", "lifestyle", "weight", "metabolism",
    "calories", "macronutrients", "micronutrients", "protein", "carbohydrates", "fats",
    "vitamins", "minerals", "gut", "digestion", "superfoods", "antioxidants",
    "meal planning", "portion control", "fasting", "vegan", "vegetarian",
    "keto", "paleo", "low-carb", "high-protein", "heart",
    "diabetes", "cholesterol", "blood", "pressure", "immune", "brain",
    "stress", "mindfulness", "yoga", "meditation", "posture", "mobility",
    "stretching", "cardio", "strength", "training", "aerobics", "workout",
    "home", "gym", "muscle", "recover", "supplements", "probiotic", "detox", 
    "energy", "circadian rhythm", "sleep", "hygiene", "rest", "recover", 
    "self-care", "clarity", "emotion", "well-being", "work-life balance",
    "hormonal", "hormone", "anti-aging", "hydration levels", "electrolytes", "mind-gut connection",
    "sports", "pregnancy", "child", "senior"
}

@app.route("/")
def home():
    return "Welcome to the AI Sustainable Living Coach API! Use the /chat endpoint to interact."



@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "Missing 'message' in request body"}), 400

        user_input = data["message"].strip().lower()
        if not user_input:
            return jsonify({"error": "Message cannot be empty"}), 400

        if not any(topic in user_input for topic in ALLOWED_TOPICS):
            return jsonify({
                "response": "I'm here to discuss health, fitness, and sustainable living. "
                            "Try asking about nutrition, exercise, or wellness!"
            })

        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(user_input)


        return jsonify({"response": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
















