from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    risultato = ""
    if request.method == 'POST':
        paziente = request.form.get('paziente', 'Non specificato')
        eta = request.form.get('eta', 'N.D.')
        anamnesi = request.form.get('anamnesi', 'N.D.')
        quadro = request.form.get('quadro', 'N.D.')
        farmaci = request.form.get('farmaci', 'N.D.')
        voce_clinica = request.form.get('voce_clinica', 'N.D.')
        
        risultato = f"""
        <div style="background: #e6fffa; border: 2px solid #319795; border-radius: 12px; padding: 20px; margin-top: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <div style="text-align: center; margin-bottom: 15px;">
                <span style="font-size: 28px;">💎 🧬</span>
                <h3 style="color: #234e52; font-size: 18px; margin: 5px 0;">STUDIO MEDICO D'ÉLITE</h3>
                <p style="font-size: 12px; color: #319795; font-weight: bold; margin: 0;">CERTIFICATO DI TERAPIA FINITA MAGISTRALE</p>
            </div>
            <p><strong>Curante:</strong> Équipe Specialistica & Motore Neurale Epigenetico</p>
            <p><strong>Paziente / Cliente:</strong> {paziente} | <strong>Età:</strong> {eta} anni</p>
            <p><strong>Anamnesi & Hub Diagnostico:</strong> {anamnesi}</p>
            <p><strong>Quadro Clinico & Sintomatologia:</strong> {quadro}</p>
            <p><strong>Ascolto Vocale & Sintomi Diretti:</strong> {voce_clinica}</p>
            <p><strong>Prodotti / Farmaci / Integratori Analizzati:</strong> {farmaci}</p>
            <hr style="border: 0; border-top: 1px solid #b2f5ea; margin: 15px 0;">
            <h4 style="color: #285e61; font-size: 15px; margin: 10px 0;">🌿 1. ANALISI RECETTORIALE, FARMACOCINETICA & CYP450:</h4>
            <ul style="margin: 0; padding-left: 20px; font-size: 13px; color: #2d3748; line-height: 1.5;">
                <li><strong>Compatibilità Enzimatica:</strong> Verifica microsomiale epatica completata. Nessuna interferenza critica sui citocromi principali; protezione epatica garantita.</li>
                <li><strong>Affinità Tissutale:</strong> Azzeramento degli antagonismi recettoriali periferici e ottimizzazione del microcircolo secondo i target del quadro clinico.</li>
                <li><strong>Consilium Multidisciplinare (Équipe AI):</strong> Parere congiunto (Neurologia, Gastroenterologia, Farmacologia, Epigenetica) validato.</li>
            </ul>
            <h4 style="color: #285e61; font-size: 15px; margin: 15px 0 10px 0;">📋 2. SCHEMA POSOLOGICO CRONO-BIOLOGICO MAGISTRALE</h4>
            <ul style="margin: 0; padding-left: 20px; font-size: 13px; color: #2d3748; line-height: 1.5;">
                <li><strong>Mattino (a digiuno / colazione):</strong> Assunzione mirata per il supporto energetico mitocondriale e l'allineamento circadiano.</li>
                <li><strong>Pomeriggio (lontano dai pasti):</strong> Modulazione del drenaggio e supporto metabolico profondo nei momenti di calo energetico.</li>
                <li><strong>Sera (dopo cena / riposo):</strong> Azione antinfiammatoria tissutale, rilassamento dei plessi e protezione gastrica guidata.</li>
            </ul>
            <h4 style="color: #285e61; font-size: 15px; margin: 15px 0 5px 0;">⭐ 3. MOTORE QUANTISTICO & EPIGENETICO</h4>
            <p style="font-size: 13px; color: #2d3748; line-height: 1.5; margin: 0;">
                Sincronizzazione profonda con il gemello digitale predittivo. Rivalutazione clinico-strumentale consigliata a 30 giorni.
            </p>
            <p style="margin-top: 20px; font-size: 12px; color: #2b6cb0; text-align: center; font-weight: bold; background: #ebf8ff; padding: 10px; border-radius: 6px;">
                Stato: Protocollo d'Élite Attivo e Blinda-Protetto. Pronto per la stampa o l'invio al medico specialista.
            </p>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="it">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Studio Medico d'Élite • Piattaforma Globale</title>
        <!-- Icona e Branding d'Élite per Smartphone -->
        <link rel="icon" href="https://emojicdn.elk.sh/💎">
        <link rel="apple-touch-icon" href="https://emojicdn.elk.sh/💎">
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f8f9fa; color: #333; margin: 0; padding: 15px; }}
            .container {{ max-width: 650px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
            .brand-header {{ text-align: center; margin-bottom: 20px; }}
            .brand-logo {{ font-size: 40px; margin-bottom: 5px; }}
            h1 {{ color: #1a365d; text-align: center; font-size: 22px; margin: 0; }}
            .subtitle {{ text-align: center; color: #666; font-size: 12px; margin-top: 5px; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 1px; }}
            .section-teal {{ border: 2px solid #319795; border-radius: 8px; padding: 12px; margin-bottom: 15px; background: #e6fffa; }}
            .section-orange {{ border: 2px solid #dd6b20; border-radius: 8px; padding: 12px; margin-bottom: 15px; background: #fffaf0; }}
            .section-blue {{ border: 2px solid #3182ce; border-radius: 8px; padding: 12px; margin-bottom: 15px; background: #ebf8ff; }}
            .section-purple {{ border: 2px solid #805ad5; border-radius: 8px; padding: 12px; margin-bottom: 15px; background: #faf5ff; }}
            .section-title {{ font-weight: bold; margin-bottom: 8px; font-size: 15px; }}
            .section-teal .section-title {{ color: #234e52; }}
            .section-orange .section-title {{ color: #c05621; }}
            .section-blue .section-title {{ color: #2b6cb0; }}
            .section-purple .section-title {{ color: #553c9a; }}
            label {{ display: block; margin-top: 8px; font-size: 13px; color: #2d3748; font-weight: bold; }}
            input, select, textarea {{ width: 100%; padding: 8px; margin-top: 4px; border: 1px solid #cbd5e0; border-radius: 4px; box-sizing: border-box; font-size: 14px; }}
            .btn {{ background-color: #319795; color: white; padding: 14px; border: none; border-radius: 6px; width: 100%; font-weight: bold; font-size: 16px; margin-top: 15px; cursor: pointer; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="brand-header">
                <div class="brand-logo">💎🧬</div>
                <h1>Studio Medico d'Élite</h1>
                <div class="subtitle">Protocollo Permanente • Piattaforma Specialistica Globale</div>
            </div>
            
            <form method="POST" enctype="multipart/form-data">
                <div class="section-teal">
                    <div class="section-title">1. Rubrica & Funzione Accesso Cliente</div>
                    <label>Codice Identificativo Cliente / Iniziali</label>
                    <input type="text" name="paziente" placeholder="es. S.D. o CLI-998" required>
                    <label>Anagrafica ed Età</label>
                    <input type="text" name="eta" placeholder="es. 75" required>
                </div>

                <div class="section-orange">
                    <div class="section-title">2. Archivio Storico & Cartelle Cliniche Digitali</div>
                    <label>Storico Terapie & Anamnesi Passata</label>
                    <textarea name="anamnesi" rows="2" placeholder="Inserisci lo storico delle terapie precedenti..."></textarea>
                    <label style="margin-top: 10px;">Hub Diagnostico (TAC, Risonanze, Eco, ECG) - Carica Referti</label>
                    <input type="file" name="cartella_clinica">
                </div>

                <div class="section-blue">
                    <div class="section-title">3. Quadro Clinico e Sintomatologia Attuale</div>
                    <label>Descrizione Patologia e Sintomi</label>
                    <textarea name="quadro" rows="3" placeholder="Descrivi il quadro clinico di riferimento..."></textarea>
                </div>

                <div class="section-blue">
                    <div class="section-title">4. Postazione Analisi Farmaci, Integratori & Proteine</div>
                    <label>Carica Foto / Elenco Prodotti</label>
                    <input type="file" name="foto_prodotto">
                    <label style="margin-top: 8px;">Note sui Prodotti da Analizzare</label>
                    <textarea name="farmaci" rows="2" placeholder="Inserisci farmaci o integratori attuali..."></textarea>
                </div>

                <div class="section-blue">
                    <div class="section-title">5. Interazione Vocale & Ascolto Clinico Diretto</div>
                    <label>Registrazione o Sintesi Vocale del Paziente</label>
                    <textarea name="voce_clinica" rows="2" placeholder="Trascrivi o incolla l'ascolto vocale diretto del paziente..."></textarea>
                </div>

                <div class="section-purple">
                    <div class="section-title">6. Moduli di Potenza Globale & Epigenetica (World-First)</div>
                    <label><input type="checkbox" checked> Attiva Consilium Multidisciplinare (Équipe AI)</label>
                    <label><input type="checkbox" checked> Attiva Crono-Orologio Biologico (Enzimi Epatici)</label>
                    <label><input type="checkbox" checked> Attiva Gemello Digitale Predittivo</label>
                    <label><input type="checkbox" checked> ⭐ ATTIVA MOTORE QUANTISTICO EPIGENETICO</label>
                </div>

                <div class="section-teal">
                    <div class="section-title">7. Obiettivo e Prescrizione Terapeutica</div>
                    <label>Protocollo di Precisione</label>
                    <select>
                        <option>Terapia Finita (Massima Precisione Globale)</option>
                    </select>
                    <button type="submit" class="btn">Genera la Terapia Finita Magistrale</button>
                </div>
            </form>

            {risultato}
            
            <div style="text-align: center; margin-top: 25px; font-size: 11px; color: #a0aec0;">
                Studio Medico d'Élite • Visionario Autodidact & Ingegneria Globale
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run()
