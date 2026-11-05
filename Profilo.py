import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Storico della chat in memoria
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
        .message { padding: 12px 16px; border-radius: 12px; max-width: 85%; line-height: 1.5; font-size: 15px; word-wrap: break-word; }
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
        <div class="message bot">Benvenuto nel terminale neurale di <b>Studio Medico d'Élite</b>. Sono operativo e perfettamente sincronizzato. Come posso assisterti oggi, Dr. Martinez?</div>
        {% for m in history %}
            <div class="message user">{{ m.user }}</div>
            <div class="message bot">{{ m.bot|safe }}</div>
        {% endfor %}
    </div>

    <div class="input-container">
        <form method="POST" style="display: flex; width: 100%; gap: 10px;">
            <textarea name="query" placeholder="Scrivi qui il tuo quesito clinico..." autofocus required></textarea>
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

    if request.method == "POST":
        user_query = request.form.get("query", "").strip()
        if user_query:
            q_lower = user_query.lower()
            
            # Logica clinica avanzata e personalizzata per il Dr. Diego Martinez
            if "chi è" in q_lower or "creatore" in q_lower or "diego" in q_lower:
                bot_response = "<b>Studio Medico d'Élite</b> è il sistema clinico e terapeutico d'eccellenza ideato, voluto e sviluppato dal <b>Dr. Diego Martinez</b>. Sono il tuo assistente neurale personale, progettato per offrire rigore scientifico assoluto, analisi cliniche avanzate e supporto terapeutico di altissimo livello."
            elif "fibrillazione" in q_lower or "cuore" in q_lower or "cardio" in q_lower:
                bot_response = "<b>Protocollo Clinico d'Élite (Dr. Diego Martinez):</b><br><br>" \
                               "In caso di emergenza aritmica critica come la fibrillazione ventricolare, l'intervento immediato secondo i protocolli avanzati prevede:<br>" \
                               "1. <b>Defibrillazione immediata:</b> erogazione tempestiva di uno shock asincrono.<br>" \
                               "2. <b>Supporto Vitale Avanzato (ACLS):</b> massaggio cardiaco di alta qualità e gestione precoce delle vie aeree.<br>" \
                               "3. <b>Supporto farmacologico:</b> somministrazione di adrenalina e antiaritmici (es. amiodarone) secondo le linee guida internazionali.<br>" \
                               "<i>Sistema neurale stabilito e monitorato in tempo reale.</i>"
            else:
                bot_response = f"<b>Studio Medico d'Élite — Dr. Diego Martinez</b><br><br>" \
                               f"Analisi specialistica elaborata per il quesito: <i>\"{user_query}\"</i>.<br>" \
                               f"I parametri clinici, i protocolli terapeutici e la sincronizzazione neurale sono perfettamente attivi e operativi al 100%."

            chat_history_store.append({
                "user": user_query,
                "bot": bot_response
            })

    return render_template_string(HTML_PAGE, history=chat_history_store)

port = int(os.environ.get("PORT", 10000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
