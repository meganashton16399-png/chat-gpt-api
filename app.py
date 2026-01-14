import requests
import json
from flask import Flask, request, Response, abort

app = Flask(__name__)

API_URL = "https://chataibot.ru/api/promo-chat/messages"
HEADERS = {
    "Content-Type": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 Chrome/127.0.0.0 Mobile Safari/537.36",
    "Referer": "https://chataibot.ru/app/free-chat",
    "Accept": "application/json"
}

def chat_with_bot(prompt, messages=None):
    if not prompt: return {"result": "Prompt cannot be empty"}
    messages = messages or []
    payload = {"messages": messages + [{"role": "user", "content": prompt.strip()}]}
    
    try:
        r = requests.post(API_URL, json=payload, headers=HEADERS, timeout=30)
        r.raise_for_status()
        return {"result": r.json().get("answer", "No answer found")}
    except Exception as e:
        return {"error": str(e)}

# 1. ORIGINAL POST ROUTE (Keep this for your Flutter Apps)
@app.route("/", methods=["POST"])
def handle_post():
    data = request.get_json(silent=True) or {}
    response = chat_with_bot(data.get("prompt"), data.get("messages", []))
    return Response(json.dumps(response, ensure_ascii=False), mimetype="application/json")

# 2. NEW GET ROUTE (For Browser URL usage)
# This catches anything you type after the "/"
@app.route("/<path:user_query>", methods=["GET"])
def handle_url_query(user_query):
    # Convert "whats+the+capital" -> "whats the capital"
    clean_prompt = user_query.replace("+", " ")
    
    response = chat_with_bot(clean_prompt)
    
    # Return JSON so it looks nice in browser
    return Response(json.dumps(response, ensure_ascii=False), mimetype="application/json")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
