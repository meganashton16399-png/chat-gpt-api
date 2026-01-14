import requests
import json
from flask import Flask, request, Response, abort

app = Flask(__name__)

# The Russian API Endpoint
API_URL = "https://chataibot.ru/api/promo-chat/messages"

# Headers that mimic a real Android phone to avoid being blocked
HEADERS = {
    "Content-Type": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 Chrome/127.0.0.0 Mobile Safari/537.36",
    "Referer": "https://chataibot.ru/app/free-chat",
    "Accept": "application/json"
}

def chat_with_bot(prompt, messages=None):
    if not prompt:
        abort(400, "Prompt is required")

    messages = messages or []
    # Combine history with the new prompt
    messages_to_send = messages + [{"role": "user", "content": prompt.strip()}]
    payload = {"messages": messages_to_send}

    try:
        # Send request to external API
        r = requests.post(API_URL, json=payload, headers=HEADERS, timeout=30)
        r.raise_for_status()
        
        data = r.json()
        if "answer" not in data:
            abort(502, "External API returned no answer")

        return {"result": data["answer"]}
    except Exception as e:
        abort(502, f"API Error: {str(e)}")

@app.route("/", methods=["POST"])
def handle_chat():
    # Get JSON data from the request
    data = request.get_json(silent=True) or {}
    prompt = data.get("prompt")
    messages = data.get("messages", [])

    if not prompt:
        abort(400, "Prompt is required in JSON body")

    # Call the helper function
    response_data = chat_with_bot(prompt, messages)

    return Response(
        json.dumps(response_data, ensure_ascii=False),
        mimetype="application/json"
    )

@app.route("/", methods=["GET"])
def index():
    return "Khush AI Server is Running! Send a POST request to use it."

if __name__ == "__main__":
    # This part runs only on your local machine, not on Render
    app.run(host="0.0.0.0", port=5000, debug=True)
