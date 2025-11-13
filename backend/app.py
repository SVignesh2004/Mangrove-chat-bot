from flask import Flask, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
from flask_cors import CORS
import os

load_dotenv()

API_KEY_2 = os.getenv("GEMINI_API_KEY")
API_KEY_1 = os.getenv("GEMINI_API_KEY_2")

if not API_KEY_1:
    raise ValueError("Missing GEMINI_API_KEY in .env file")

MODEL_NAME = "gemini-2.0-flash"

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": [
    "http://localhost:5173", "https://mangrove-chat-bot.vercel.app"
]}})


def generate_reply(system_prompt, user_message, api_key):
    """Generate model reply safely using the correct Gemini format."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(MODEL_NAME)


    chat_input = [
        {"role": "user", "parts": [
            f"{system_prompt}\n\nQuestion: {user_message}"
        ]}
    ]

    response = model.generate_content(chat_input)
    return response.text.strip() if hasattr(response, "text") else str(response)


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
        user_message = (data.get("message") or "").strip()

        if not user_message:
            return jsonify({"error": "Empty message provided."}), 400
        greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
        if any(greet in user_message.lower() for greet in greetings):
            return jsonify({
                "reply": "👋 Hello there! How can I help you learn about forests or Mangrove ecosystems today?"
            }), 200
        
        farewells = ["bye", "goodbye", "see you", "take care", "thank you", "thanks"]
        if any(word in user_message.lower() for word in farewells):
            reply = "😊 You're most welcome! Glad I could help!" if "thank" in user_message.lower() \
                    else "🌿 Goodbye! Hope you learned something new today. See you soon!"
            return jsonify({"reply": reply}), 200

        # System prompt
        system_prompt = (
            "You are a helpful educational assistant who explains environmental and forest topics clearly. "
            "If the question mentions Mangrove, focus only on Mangrove details. "
            "If it's general (like 'What is flora?', 'Define fauna', etc.), give a general explanation first, "
            "then end with one short Mangrove example. "
            "Keep replies friendly, simple, under 6 lines, and use 2 emojis for readability."
        )

        try:
            reply_text = generate_reply(system_prompt, user_message, API_KEY_1)
            return jsonify({"reply": reply_text, "key_used": "primary"}), 200

        except Exception as e:
            err = str(e)
            if "429" in err or "quota" in err.lower() or "404" in err:
                reply_text = generate_reply(system_prompt, user_message, API_KEY_2)
                return jsonify({"reply": reply_text, "key_used": "backup"}), 200
            else:
                raise e

    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
