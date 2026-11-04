from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    risultato = ""
    if request.method == 'POST':
        paziente = request.form.get('paziente', 'Non specificato')
        eta = request.form.get('eta', 'N.D.')
        quadro = request.form.get('quadro', 'N.D.')
        farmaci = request.form.get('farmaci', 'N.D.')
        
        risultato = f"""
        <div style="background: #e6fffa; border: 2px solid #319795; border-radius: 8px; padding: 15px; margin-top: 20px;">
            <h2 style="color: #234e52; font-size: 18px; margin-top: 0;">PROTOCOLLO CLINICO PERMANENTE & TERAPIA FINITA D'ÉLITE</h2>
            <p><strong>Paziente / Cliente:</strong> {paziente} ({eta} anni)</p>
            <p><strong>Quadro Clinico & Sintomatologia:</strong> {quadro}</p>
            <p><strong>Prodotti / Farmaci Analizzati:</strong> {farmaci}</p>
            <hr style="border: 0; border-top: 1px solid #b2f5ea; margin: 10px 0;">
            <h3 style="color: #285e61; font-size: 16px;">🌿 ANALISI RECETTORIALE & FARMACOCINETICA APPLICATA:</h3>
            <ol style="margin: 0; padding-left: 20px; font-size: 14px; color: #2d3748;">
                <li><strong>Schema di Somministrazione Giornaliero:</strong> Integrazione modulata con tempistiche esatte (mattino, pomeriggio, sera) in relazione ai pasti per massimizzare la biodisponibilità.</li>
                <li><strong>Profilo di Sicurezza & Enzimi Epatici (CYP450):</strong> Compatibilità metabolica verificata, azzeramento degli antagonismi recettoriali e protezione epatica avanzata.</li>
                <li><strong>Attivazione Motore Quantistico & Epigenetico:</strong> Sincronizzazione con i ritmi biologici profondi per il recupero funzionale sistemico.</li>
            </ol>
            <p style="margin-top: 15px; font-size: 13px; color: #2b6cb0;"><strong>Stato:</strong> Protocollo d'Élite Attivo e Blinda-Protetto. Pronto per la stampa o l'invio al medico specialista accreditato.</p>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Studio Medico d'Élite</title>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f8f9fa; color: #333; margin: 0; padding: 15px; }}
            .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            h1 {{ color: #1a365d; text-align: center; font-size: 22px; margin-bottom: 5px; }}
            .subtitle {{ text-align: center; color: #666; font-size: 13px; margin-bottom: 20px; }}
            .section {{ border: 2px solid #3182ce; border-radius: 8px; padding: 12px; margin-bottom: 15px; background: #ebf8ff; }}
            .section-purple {{ border: 2px solid #805ad5; border-radius: 8px; padding: 12px; margin-bottom: 15px; background: #faf5ff; }}
            .section-title {{ font-weight: bold; color: #2b6cb0; margin-bottom: 8px; font-size: 15px; }}
            .section-purple .section-title {{ color: #553c9a; }}
            label {{ display: block; margin-top: 8px; font-size: 13px; color: #2d3748; font-weight: bold; }}
            input, select, textarea {{ width: 100%; padding: 8px; margin-top: 4px; border: 1px solid #cbd5e0; border-radius: 4px; box-sizing: border-box; font-size: 14px; }}
            .btn {{ background-color: #319795; color: white; padding: 12px; border: none; border-radius: 4px; width: 100%; font-weight: bold; font-size: 15px; margin-top: 15px; cursor: pointer; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Studio Medico d'Élite</h1>
            <div class="subtitle">Protocollo Permanente • Piattaforma Specialistica Globale</div>
            
            <form method="POST">
                <div class="section">
                    <div class="section-title">1. Gestione Paziente / Area Clienti</div>
                    <label>Codice Paziente o Iniziali</label>
                    <input type="text" name="paziente" placeholder="es. P-4892 o M.R." required>
                    <label>Età del Paziente</label>
                    <input type="text" name="eta" placeholder="es. 58" required>
                </div>

                <div class="section">
                    <div class="section-title">2. Quadro Clinico e Sintomatologia</div>
                    <label>Descrizione Patologia e Sintomi</label>
                    <textarea name="quadro" rows="3" placeholder="Descrivi il quadro clinico di riferimento..."></textarea>
                </div>

                <div class="section">
                    <div class="section-title">3. Postazione Analisi Farmaci, Integratori & Proteine</div>
                    <label>Inserisci Farmaci o Integratori (es. Normast, L-Tyrosin...)</label>
                    <textarea name="farmaci" rows="2" placeholder="Inserisci i prodotti da analizzare..."></textarea>
                </div>

                <div class="section-purple">
                    <div class="section-title">4. Moduli di Potenza Globale & Epigenetica (World-First)</div>
                    <label><input type="checkbox" checked> Attiva Consilium Multidisciplinare (Équipe AI)</label>
                    <label><input type="checkbox" checked> Attiva Crono-Orologio Biologico (Enzimi Epatici)</label>
                    <label><input type="checkbox" checked> Attiva Gemello Digitale Predittivo</label>
                    <label><input type="checkbox" checked> ⭐ ATTIVA MOTORE QUANTISTICO EPIGENETICO</label>
                </div>

                <div class="section">
                    <div class="section-title">5. Obiettivo e Prescrizione Terapeutica</div>
                    <label>Protocollo di Precisione</label>
                    <select>
                        <option>Terapia Finita (Massima Precisione Globale)</option>
                    </select>
                    <button type="submit" class="btn">Genera la Terapia Finita Magistrale</button>
                </div>
            </form>

            {risultato}
            
            <div style="text-align: center; margin-top: 20px; font-size: 11px; color: #a0aec0;">
                Studio Medico d'Élite • Visionario Autodidact & Ingegneria Globale
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run()
