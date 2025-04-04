from flask import Flask, request, jsonify
from openai import OpenAI
from flask_cors import CORS

print("Starting Flask server...")

app = Flask(__name__)
CORS(app)

try:
    client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lm-studio")
    print("Connected to LM Studio API")
except Exception as e:
    print("Error connecting to LM Studio:", e)
    client = None

@app.route("/")
def home():
    return "AI Chatbot API is running!"

@app.route("/chat", methods=["POST"])
def chat():
    if not client:
        return jsonify({"error": "AI service is unavailable"}), 503

    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()
        print("Received message:", user_message)

        if not user_message:
            return jsonify({"error": "Message field is required"}), 400

        print("Sending request to LM Studio...")
        response = client.chat.completions.create(
            model="mistral-7b-instruct-v0.3",
            messages=[{"role": "user", "content": user_message}],
            max_tokens=300,  # Increased limit to prevent truncation
            temperature=0.7  # Adjust response randomness
        )

        print("Full Response Object:", response)

        choices = getattr(response, "choices", [])
        if not choices or not choices[0].message:
            print("Error: No valid response received from LM Studio")
            return jsonify({"error": "Invalid response from AI"}), 500

        ai_response = choices[0].message.content.strip()
        if choices[0].finish_reason == "length":
            ai_response += " [Response truncated. Try rephrasing or requesting a summary.]"

        print("AI Response:", ai_response)
        return jsonify({"response": ai_response})

    except Exception as e:
        print("Error in /chat:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Running Flask server on http://127.0.0.1:5000")
    app.run(debug=True)
