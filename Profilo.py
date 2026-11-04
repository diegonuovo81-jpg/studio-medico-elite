
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Studio Medico d'Élite</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f8f9fa; color: #333; margin: 0; padding: 15px; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            h1 { color: #1a365d; text-align: center; font-size: 22px; margin-bottom: 5px; }
            .subtitle { text-align: center; color: #666; font-size: 13px; margin-bottom: 20px; }
            .section { border: 2px solid #3182ce; border-radius: 8px; padding: 12px; margin-bottom: 15px; background: #ebf8ff; }
            .section-title { font-weight: bold; color: #2b6cb0; margin-bottom: 8px; font-size: 15px; }
            label { display: block; margin-top: 8px; font-size: 13px; color: #2d3748; font-weight: bold; }
            input, select, textarea { width: 100%; padding: 8px; margin-top: 4px; border: 1px solid #cbd5e0; border-radius: 4px; box-sizing: border-box; font-size: 14px; }
            .btn { background-color: #319795; color: white; padding: 12px; border: none; border-radius: 4px; width: 100%; font-weight: bold; font-size: 15px; margin-top: 15px; cursor: pointer; text-align: center; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Studio Medico d'Élite</h1>
            <div class="subtitle">Protocollo Permanente • Piattaforma Specialistica Globale</div>
            
            <div class="section">
                <div class="section-title">1. Gestione Paziente / Area Clienti</div>
                <label>Codice Paziente o Iniziali</label>
                <input type="text" placeholder="es. P-4892 o M.R.">
                
                <label>Età del Paziente</label>
                <input type="text" placeholder="es. 58">
            </div>

            <div class="section">
                <div class="section-title">2. Quadro Clinico e Sintomatologia</div>
                <label>Descrizione Patologia e Sintomi</label>
                <textarea rows="3" placeholder="Descrivi il quadro clinico di riferimento..."></textarea>
            </div>

            <div class="section">
                <div class="section-title">3. Hub Diagnostico (TAC, Risonanze, PET, Eco, RX)</div>
                <label>Carica Referti o Immagini Diagnostiche</label>
                <input type="file">
            </div>

            <div class="section">
                <div class="section-title">4. Postazione Analisi Farmaci, Integratori & Proteine</div>
                <label>Carica Foto / Elenco Prodotti (Farmaci, Integratori, Proteine)</label>
                <input type="file">
                <label>Note sui Prodotti da Analizzare</label>
                <textarea rows="3" placeholder="Inserisci i nomi o i dettagli dei farmaci/integratori da sottoporre ad analisi magistrale..."></textarea>
            </div>

            <div class="section">
                <div class="section-title">5. Obiettivo e Prescrizione Terapeutica</div>
                <label>Protocollo di Precisione</label>
                <select>
                    <option>Terapia Finita (Massima Precisione Globale)</option>
                    <option>Protocollo Personalizzato Avanzato</option>
                </select>
                <button class="btn">Genera la Terapia Finita Magistrale</button>
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run()
