from flask import Flask, request
import os
from google import genai

app = Flask(__name__)

# Inizializzazione del client Google GenAI con la chiave sicura di Render
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/', methods=['GET', 'POST'])
def home():
    risultato = ""
    if request.method == 'POST':
        paziente = request.form.get('paziente', 'Non specificato')
        eta = request.form.get('eta', 'N.D.')
        referti_clinici = request.form.get('referti_clinici', 'Nessun referto inserito')
        farmaci_prodotti = request.form.get('farmaci_prodotti', 'Nessun integratore inserito')
        
        # Prompt clinico d'Élite per guidare l'intelligenza artificiale
        prompt_clinico = f"""
        Agisci come il Dott. Diego Martinez e l'Équipe Specialistica dello Studio Medico d'Élite.
        Analizza i seguenti dati del paziente (Codice: {paziente}, Età: {eta} anni):
        - QUADRO DIAGNOSTICO / REFERTI: {referti_clinici}
        - PRODOTTI / INTEGRATORI / FARMACI: {farmaci_prodotti}
        
        Genera una "Terapia Finita Magistrale" rigorosa, scientifica, mirata e formattata con tag HTML puliti (usa titoli h4, paragrafi p e liste ul/li) strutturata esattamente in questo modo:
        1. Analisi del quadro diagnostico e dei recettori periferici.
        2. Screening farmacocinetico (interazioni, citocromi CYP450, microcircolo).
        3. Schema posologico crono-biologico magistrale (Mattino, Pomeriggio, Sera).
        4. Note di medicina quantistica ed epigeneticamente mirata.
        """
        
        try:
            # Chiamata al modello reale di intelligenza artificiale
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt_clinico,
            )
            testo_ia = response.text
        except Exception as e:
            testo_ia = f"<p style='color: red;'>Errore durante la Sincronizzazione Neurale: {str(e)}</p>"

        # Contenitore finale della risposta magistrale
        risultato = f"""
        <div style="background: #e6fffa; border: 2px solid #319795; border-radius: 12px; padding: 20px; margin-top: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <div style="text-align: center; margin-bottom: 15px;">
                <div style="font-size: 45px; margin-bottom: 5px;">🛡️ 💎 🧬</div>
                <h3 style="color: #234e52; font-size: 18px; margin: 10px 0 5px 0;">TERAPIA FINITA MAGISTRALE • MOTORE NEURALE ATTIVO</h3>
                <p style="font-size: 12px; color: #319795; font-weight: bold; margin: 0;">STUDIO MEDICO D'ÉLITE • IL FUTURO DELLA MEDICINA MODERNA</p>
            </div>
            <p><strong>Curante:</strong> Dott. Diego Martinez, M.D. & Équipe Specialistica I.A.</p>
            <p><strong>Paziente / Codice:</strong> {paziente} | <strong>Età:</strong> {eta} anni</p>
            
            <hr style="border: 0; border-top: 1px solid #b2f5ea; margin: 15px 0;">
            
            <div style="color: #2d3748; font-size: 13px; line-height: 1.6;">
                {testo_ia}
            </div>
            
            <p style="margin-top: 20px; font-size: 12px; color: #2b6cb0; text-align: center; font-weight: bold; background: #ebf8ff; padding: 10px; border-radius: 6px;">
                Stato: Sincronizzazione Neurale Dinamica Completata. Puntuale. Preciso. Eccellente.
            </p>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Studio Medico d'Élite • Terminale Neurale</title>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f8f9fa; color: #333; margin: 0; padding: 15px; }}
            .container {{ max-width: 650px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
            .brand-header {{ text-align: center; margin-bottom: 20px; }}
            h1 {{ color: #1a365d; text-align: center; font-size: 22px; margin: 0; }}
            .subtitle {{ text-align: center; color: #666; font-size: 11px; margin-top: 5px; margin-bottom: 20px; text-transform: uppercase; font-weight: bold; }}
            .section-teal {{ border: 2px solid #319795; border-radius: 8px; padding: 12px; margin-bottom: 15px; background: #e6fffa; }}
            .section-orange {{ border: 2px solid #dd6b20; border-radius: 8px; padding: 12px; margin-bottom: 15px; background: #fffaf0; }}
            .section-blue {{ border: 2px solid #3182ce; border-radius: 8px; padding: 12px; margin-bottom: 15px; background: #ebf8ff; }}
            .section-title {{ font-weight: bold; margin-bottom: 8px; font-size: 15px; }}
            .section-teal .section-title {{ color: #234e52; }}
            .section-orange .section-title {{ color: #c05621; }}
            .section-blue .section-title {{ color: #2b6cb0; }}
            label {{ display: block; margin-top: 8px; font-size: 13px; color: #2d3748; font-weight: bold; }}
            input, textarea {{ width: 100%; padding: 8px; margin-top: 4px; border: 1px solid #cbd5e0; border-radius: 4px; box-sizing: border-box; font-size: 14px; }}
            .btn {{ background-color: #319795; color: white; padding: 14px; border: none; border-radius: 6px; width: 100%; font-weight: bold; font-size: 16px; margin-top: 15px; cursor: pointer; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="brand-header">
                <div style="font-size: 45px; margin-bottom: 5px;">🛡️💎🧬</div>
                <h1>Studio Medico d'Élite</h1>
                <div class="subtitle">Il Futuro della Medicina Moderna • Puntuale, Preciso, Eccellente</div>
            </div>
            
            <form method="POST">
                <div class="section-teal">
                    <div class="section-title">1. Anagrafica Paziente / Codice</div>
                    <label>Iniziali o Codice Cliente</label>
                    <input type="text" name="paziente" placeholder="es. CLI-999" required>
                    <label>Età</label>
                    <input type="text" name="eta" placeholder="es. 60" required>
                </div>

                <div class="section-orange">
                    <div class="section-title">2. Casella Dedicata: Referti, TAC, Analisi & Diagnostica</div>
                    <label>Incolla o scrivi i dati dei referti, esami del sangue, TAC o ecografie</label>
                    <textarea name="referti_clinici" rows="4" placeholder="Inserisci qui il referto medico o la diagnostica..."></textarea>
                </div>

                <div class="section-blue">
                    <div class="section-title">3. Casella Dedicata: Farmaci, Integratori & Proteine</div>
                    <label>Inserisci l'elenco dei prodotti o integratori attuali</label>
                    <textarea name="farmaci_prodotti" rows="4" placeholder="Inserisci qui gli integratori o farmaci..."></textarea>
                </div>

                <div class="section-teal">
                    <button type="submit" class="btn">⚡ Genera la Terapia Finita Magistrale</button>
                </div>
            </form>

            {risultato}
            
            <div style="text-align: center; margin-top: 25px; font-size: 11px; color: #a0aec0;">
                Studio Medico d'Élite • Terminale Neurale Globale
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
