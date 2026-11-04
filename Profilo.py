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
            body { font-family: Arial, sans-serif; background-color: #f8f9fa; color: #333; margin: 0; padding: 20px; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            h1 { color: #1a365d; text-align: center; font-size: 24px; }
            .subtitle { text-align: center; color: #666; font-size: 14px; margin-bottom: 20px; }
            .section { border: 2px solid #4fd1c5; border-radius: 8px; padding: 15px; margin-bottom: 15px; background: #e6fffa; }
            .section-title { font-weight: bold; color: #2c7a7b; margin-bottom: 10px; }
            label { display: block; margin-top: 10px; font-size: 14px; color: #2d3748; }
            input, select, textarea { width: 100%; padding: 8px; margin-top: 5px; border: 1px solid #cbd5e0; border-radius: 4px; box-sizing: border-box; }
            .section-orange { border: 2px solid #ed8936; border-radius: 8px; padding: 15px; margin-bottom: 15px; background: #fffaf0; }
            .section-orange .section-title { color: #c05621; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Studio Medico d'Élite</h1>
            <div class="subtitle">Protocollo Permanente • Piattaforma Specialistica Globale</div>
            
            <div class="section">
                <div class="section-title">1. Rubrica & Funzione Accesso Cliente</div>
                <label>Seleziona o Cerca Profilo Cliente</label>
                <select>
                    <option>+ Registra / Nuovo Cliente</option>
                </select>
                
                <label>Codice Identificativo Cliente / Iniziali</label>
                <input type="text" placeholder="es. CLI-998 o M.R.">
                
                <label>Anagrafica ed Età</label>
                <input type="text" placeholder="es. 45">
            </div>

            <div class="section-orange">
                <div class="section-title">2. Archivio Storico & Cartelle Cliniche Digitali</div>
                <label>Storico Terapie (In corso / Sospese) & Anamnesi</label>
                <textarea rows="4" placeholder="Inserisci o carica lo storico delle terapie precedenti, interventi e anamnesi passata..."></textarea>
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run()
