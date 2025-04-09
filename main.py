from flask import Flask, request, jsonify
import google.generativeai as genai
from topics import ALLOWED_TOPICS

genai.configure(api_key="AIzaSyDbtRRb1oQrWjm_0TPA4wqLHmc4CVPZspk")  

app = Flask(__name__)



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