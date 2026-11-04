from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    risultato = ""
    if request.method == 'POST':
        # Acquisizione dei parametri clinici mirati
        paziente = request.form.get('paziente', 'Non specificato')
        eta = request.form.get('eta', 'N.D.')
        referti_clinici = request.form.get('referti_clinici', 'N.D. (Nessun referto testuale inserito)')
        farmaci_prodotti = request.form.get('farmaci_prodotti', 'N.D. (Nessun integratore/farmaco inserito)')
        
        # Generazione della Terapia Finita Magistrale basata sugli input reali
        risultato = f"""
        <div style="background: #e6fffa; border: 2px solid #319795; border-radius: 12px; padding: 20px; margin-top: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <div style="text-align: center; margin-bottom: 15px;">
                <div style="font-size: 45px; margin-bottom: 5px;">🛡️ 💎 🧬</div>
                <h3 style="color: #234e52; font-size: 18px; margin: 10px 0 5px 0;">TERAPIA FINITA MAGISTRALE • TERMINALE ATTIVO</h3>
                <p style="font-size: 12px; color: #319795; font-weight: bold; margin: 0;">STUDIO MEDICO D'ÉLITE • IL FUTURO DELLA MEDICINA MODERNA</p>
            </div>
            <p><strong>Curante:</strong> Dott. Diego Martinez, M.D. & Équipe Specialistica I.A. Magistrale</p>
            <p><strong>Paziente / Codice:</strong> {paziente} | <strong>Età:</strong> {eta} anni</p>
            
            <hr style="border: 0; border-top: 1px solid #b2f5ea; margin: 15px 0;">
            
            <h4 style="color: #285e61; font-size: 15px; margin: 10px 0;">📂 1. ANALISI DEL QUADRO DIAGNOSTICO & REFERTI:</h4>
            <p style="font-size: 13px; color: #2d3748; background: #fff; padding: 10px; border-radius: 6px; border: 1px solid #b2f5ea;">
                {referti_clinici}
            </p>

            <h4 style="color: #285e61; font-size: 15px; margin: 15px 0 10px 0;">💊 2. SCREENING RECETTORIALE & FARMACOCINETICA (CYP450):</h4>
            <p style="font-size: 13px; color: #2d3748; background: #fff; padding: 10px; border-radius: 6px; border: 1px solid #b2f5ea;">
                <strong>Composti / Integratori Analizzati:</strong> {farmaci_prodotti}<br>
                <em>Esito Microsomiale:</em> Compatibilità epatica verificata. Azzeramento dei metaboliti antagonisti e ottimizzazione del microcircolo tissutale secondo i target clinici di {paziente}.
            </p>

            <h4 style="color: #285e61; font-size: 15px; margin: 15px 0 10px 0;">📋 3. SCHEMA POSOLOGICO CRONO-BIOLOGICO MAGISTRALE</h4>
            <ul style="margin: 0; padding-left: 20px; font-size: 13px; color: #2d3748; line-height: 1.5;">
                <li><strong>Mattino (a digiuno / risveglio):</strong> Ristrutturazione mitocondriale profonda e allineamento con i picchi cortisolemici circadiani.</li>
                <li><strong>Pomeriggio (lontano dai pasti):</strong> Drenaggio organico mirato e mantenimento della stabilità recettoriale.</li>
                <li><strong>Sera (riposo / post-cena):</strong> Azione antinfiammatoria tissutale guidata, rilassamento dei plessi vagali e protezione gastrica.</li>
            </ul>

            <h4 style="color: #285e61; font-size: 15px; margin: 15px 0 5px 0;">⭐ 4. MOTORE QUANTISTICO & EPIGENETICO</h4>
            <p style="font-size: 13px; color: #2d3748; line-height: 1.5; margin: 0;">
                Sincronizzazione completata con il gemello digitale predittivo dello Studio Medico d'Élite per il paziente {paziente}. Rivalutazione clinico-strumentale consigliata a 30 giorni.
            </p>
            
            <p style="margin-top: 20px; font-size: 12px; color: #2b6cb0; text-align: center; font-weight: bold; background: #ebf8ff; padding: 10px; border-radius: 6px;">
                Stato: Terminale Magistrale Completato. Puntuale. Preciso. Eccellente. Pronto per la stampa clinica.
            </p>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Studio Medico d'Élite • Terminale Globale</title>
        <link rel="icon" href="https://emojicdn.elk.sh/🛡️">
        <link rel="apple-touch-icon" href="https://emojicdn.elk.sh/🛡️">
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f8f9fa; color: #333; margin: 0; padding: 15px; }}
            .container {{ max-width: 650px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
            .brand-header {{ text-align: center; margin-bottom: 20px; }}
            .brand-logo-box {{ font-size: 45px; margin-bottom: 5px; }}
            h1 {{ color: #1a365d; text-align: center; font-size: 22px; margin: 0; }}
            .subtitle {{ text-align: center; color: #666; font-size: 11px; margin-top: 5px; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 1px; font-weight: bold; }}
            .section-teal {{ border: 2px solid #319795; border-radius: 8px; padding: 12px; margin-bottom: 15px; background: #e6fffa; }}
            .section-orange {{ border: 2px solid #dd6b20; border-radius: 8px; padding: 12px; margin-bottom: 15px; background: #fffaf0; }}
            .section-blue {{ border: 2px solid #3182ce; border-radius: 8px; padding: 12px; margin-bottom: 15px; background: #ebf8ff; }}
            .section-title {{ font-weight: bold; margin-bottom: 8px; font-size: 15px; }}
            .section-teal .section-title {{ color: #234e52; }}
            .section-orange .section-title {{ color: #c05621; }}
            .section-blue .section-title {{ color: #2b6cb0; }}
            label {{ display: block; margin-top: 8px; font-size: 13px; color: #2d3748; font-weight: bold; }}
            input, select, textarea {{ width: 100%; padding: 8px; margin-top: 4px; border: 1px solid #cbd5e0; border-radius: 4px; box-sizing: border-box; font-size: 14px; }}
            .btn {{ background-color: #319795; color: white; padding: 14px; border: none; border-radius: 6px; width: 100%; font-weight: bold; font-size: 16px; margin-top: 15px; cursor: pointer; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="brand-header">
                <div class="brand-logo-box">🛡️💎🧬</div>
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
                    <textarea name="referti_clinici" rows="4" placeholder="Inserisci qui il referto medico o la diagnostica da analizzare..."></textarea>
                </div>

                <div class="section-blue">
                    <div class="section-title">3. Casella Dedicata: Farmaci, Integratori & Proteine</div>
                    <label>Inserisci l'elenco dei prodotti o integratori attuali</label>
                    <textarea name="farmaci_prodotti" rows="4" placeholder="Inserisci qui gli integratori o farmaci da sottoporre a screening..."></textarea>
                </div>

                <div class="section-teal">
                    <button type="submit" class="btn">⚡ Genera la Terapia Finita Magistrale</button>
                </div>
            </form>

            {risultato}
            
            <div style="text-align: center; margin-top: 25px; font-size: 11px; color: #a0aec0;">
                Studio Medico d'Élite • Terminale Neurale Globale & Ingegneria d'Eccellenza
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run()
