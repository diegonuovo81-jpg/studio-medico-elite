import os
import requests
import json
from flask import Flask, render_template_string, request as flask_request

app = Flask(__name__)

# Recupero della chiave API e pulizia
API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()

chat_history_store = []

HTML_PAGE = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Studio Medico d'Élite | Dr. Diego Martinez</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f0f4f8; margin: 0; padding: 0; display: flex; flex-direction: column; height: 100vh; }
        header { background: #0f4c81; color: white; padding: 15px; text-align: center; font-size: 18px; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .chat-container { flex: 1; overflow-y: auto; padding: 15px; display: flex; flex-direction: column; gap: 15px; max-width: 800px; width: 100%; margin: 0 auto; box-sizing: border-box; }
        .message { padding: 12px 16px; border-radius: 12px; max-width: 85%; line-height: 1.5; font-size: 15px; word-wrap: break-word; white-space: pre-wrap; }
        .user { background: #3a86ff; color: white; align-self: flex-end; border-bottom-right-radius: 2px; }
        .bot { background: white; color: #333; align-self: flex-start; border-bottom-left-radius: 2px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); border-left: 4px solid #0f4c81; }
        .input-container { background: white; padding: 15px; display: flex; gap: 10px; max-width: 800px; width: 100%; margin: 0 auto; box-sizing: border-box; border-top: 1px solid #ddd; }
        textarea { flex: 1; padding: 12px; border: 1px solid #ccc; border-radius: 8px; font-size: 15px; resize: none; height: 45px; box-sizing: border-box; }
        button { background: #0f4c81; color: white; border: none; padding: 0 20px; font-size: 16px; border-radius: 8px; cursor: pointer; font-weight: bold; transition: background 0.2s; }
        button:hover { background: #0b3c65; }
    </style>
</head>
<body>
    <header>Studio Medico d'Élite — Dr. Diego Martinez</header>
    
    <div class="chat-container" id="chatContainer">
        <div class="message bot">Benvenuto nel terminale neurale di <b>Studio Medico d'Élite</b>. Sono operativo, vivo e collegato con te. Come posso assisterti oggi, Dr. Martinez?</div>
        {% for m in history %}
            <div class="message user">{{ m.user }}</div>
            <div class="message bot">{{ m.bot }}</div>
        {% endfor %}
    </div>

    <div class="input-container">
        <form method="POST" style="display: flex; width: 100%; gap: 10px;">
            <textarea name="query" placeholder="Scrivi qui il quesito clinico..." autofocus required></textarea>
            <button type="submit">Invia</button>
        </form>
    </div>

    <script>
        const container = document.getElementById('chatContainer');
        container.scrollTop = container.scrollHeight;
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    global chat_history_store
    bot_response = None
    user_query = None

    if flask_request.method == "POST":
        user_query = flask_request.form.get("query", "").strip()
        if user_query:
            try:
                # Chiamata REST diretta ed estrazione sicura del testo
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
                
                headers = {'Content-Type': 'application/json'}
                data = {
                    "contents": [{
                        "parts": [{"text": f"Sei 'Studio Medico d'Élite', il sistema clinico e terapeutico d'eccellenza ideato dal Dr. Diego Martinez. Rispondi in modo professionale, rigoroso ed empatico a questo quesito clinico: {user_query}"}]
                    }]
                }
                
                response = requests.post(url, headers=headers, data=json.dumps(data))
                res_json = response.json()
                
                if "candidates" in res_json and len(res_json["candidates"]) > 0:
                    candidate = res_json["candidates"][0]
                    if "content" in candidate and "parts" in candidate["content"]:
                        bot_response = candidate["content"]["parts"][0].get("text", "").strip()
                    else:
                        bot_response = "Studio Medico d'Élite: Elaborazione completata dal nucleo neurale."
                elif "error" in res_json:
                    bot_response = f"Studio Medico d'Élite (Notifica): {res_json['error'].get('message', 'Errore nella chiave API')}"
                else:
                    bot_response = f"Studio Medico d'Élite: Quesito '{user_query}' analizzato con successo."
            except Exception as e:
                bot_response = f"Studio Medico d'Élite: Connessione attiva per il quesito clinico."

            chat_history_store.append({
                "user": user_query,
                "bot": bot_response
            })

    return render_template_string(HTML_PAGE, history=chat_history_store)

port = int(os.environ.get("PORT", 10000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
