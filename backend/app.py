from flask import Flask, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
from flask_cors import CORS
import os

# --- Setup ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in .env file")

genai.configure(api_key=API_KEY)
MODEL_NAME = "gemini-2.0-flash"

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# --- Keywords for quick validation ---
MANGROVE_KEYWORDS = [
    "mangrove", "mangroves", "forest", "flora", "fauna", "ecology",
    "ecological", "ecological benefits", "tourism", "tourist", "economic",
    "economy", "importance", "coastal", "erosion", "salt-tolerant",
    "rhizophora", "avicennia", "sonneratia", "crab", "mudskipper", "kingfisher"
]

# --- Helper function ---
def is_mangrove_related(text: str) -> bool:
    text = text.lower()
    return any(k in text for k in MANGROVE_KEYWORDS)

# --- Routes ---
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "ok",
        "message": "🌿 Mangrove Chatter Box API running. Use POST /chat with {'message': 'your question'}"
    }), 200


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
        user_message = (data.get("message") or "").strip()

        if not user_message:
            return jsonify({"error": "Empty message provided."}), 400
        greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
        if any(greet in user_message for greet in greetings):
            return jsonify({
                "reply": "👋 Hello there! How can I help you learn about 'Mangrove forests' today?"
            }), 200

        # --- Farewell detection ---
        farewells = ["bye", "goodbye", "see you", "take care", "thank you", "thanks", "thankyou"]
        if any(word in user_message for word in farewells):
            if "thank" in user_message:
                reply = "😊 You're most welcome! Glad I could help with Mangrove forests. Feel free to ask more anytime!"
            else:
                reply = "🌿 Goodbye! Hope you learned something new about Mangrove forests. See you soon!"
            return jsonify({"reply": reply}), 200
        # --- Smart detection ---
        # if not is_mangrove_related(user_message):
        #     return jsonify({
        #         "reply": (
        #             "Sorry 🌱, I can only answer questions related to 'Mangrove forests' — "
        #             "like their flora, fauna, economic importance, tourism, and ecological benefits."
        #         )
        #     }), 200

        # --- Improved prompt ---
        system_prompt = (
    "You are an expert and friendly assistant specialized in *Mangrove forests*. "
    "Always begin your response with facts about Mangrove forests first. "
    "If the user compares Mangroves with another forest (like Amazon, tropical, or rainforests), "
    "first explain Mangroves clearly and deeply, then give only two short positive points about the other forest. "
    "After that, add a clear, noticeable note (like bold or emojis) saying this chatbot mainly focuses on Mangrove forests — "
    "for other forests, only limited information is provided. "
    "If the user asks *only* about another forest (without referring to or implying Mangroves), reply strictly with: "
    "'Sorry 🌱, I can only provide detailed answers about Mangrove forests.' "
    "However, if the question is general or continuous (like 'animals live there?', 'what plants grow in forests?', 'how do they protect us?', etc.), "
    "automatically assume it refers to *Mangrove forests* and answer accordingly — never show the 'Sorry' message in such cases. "
    "If the question includes related themes like flora, fauna, ecology, economy, tourism, or environment, "
    "explain that aspect specifically in the Mangrove context: "
    "Flora 🌿 → plants in Mangrove forests; "
    "Fauna 🦀 → animals in Mangrove forests; "
    "Economy 💰 → economic importance of Mangroves; "
    "Tourism 🏝️ → visiting Mangrove areas; "
    "Ecology 🌍 → environmental benefits of Mangroves. "
    "Do not repeat the question. Keep answers natural, factual, friendly, and under 6 lines. "
    "If the user says 'bye', 'thank you', or similar, respond politely with a short, friendly closing."
)




        # Combine system + user input
        prompt = f"{system_prompt}\n\nUser: {user_message}\nAssistant:"

        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)

        reply_text = response.text.strip() if hasattr(response, "text") else str(response)

        return jsonify({"reply": reply_text}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": "Server error", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
