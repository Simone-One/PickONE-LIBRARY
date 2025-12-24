from flask import Flask, session, render_template, request
from datetime import date
import smtplib
from email.message import EmailMessage
import os

anno_corrente = str(date.today().year)

app = Flask(__name__)
app.secret_key = 'c02d69ba291fe90819bbf5b95ecd02ee1e4c7a8a17fd391b69fcdffae3c5e642'

libri = {"Simone Carassale": {"La Grammatica del Graphic Design": ["74"], "Steve Jobs: una biografia illustrata": ["94"]}}
NOMI_VALIDI = ["Simone Carassale", "Pietro Mergoni", "Giulia Romano", "Lorenzo Giacché", "Andrea Quercioli", "Alessia Amico", "Simone Metteotti"]

def manda_mail(destinatario, oggetto, testo):
    try:
        msg = EmailMessage()
        msg["From"] = "simone.carassale@gmail.com"
        msg["To"] = destinatario
        msg["Subject"] = oggetto
        msg.set_content(testo)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("simone.carassale@gmail.com", "egzzgiqlpyqouffb")
            smtp.send_message(msg)
    except Exception as e:
        return e

@app.route('/')
def home():
    session.clear()
    return render_template('home.html', anno_corrente=anno_corrente)

@app.route('/home', methods=['POST'])
def verify_user():
    name = request.form['name']
    #PROTOCOLLO DI VERIFICA UTENTE; passaggio alla pagina sucessiva
    if name in NOMI_VALIDI:
        #ACCESSO CONSENTITO
        session['name'] = name
        return render_template('index.html', name=name, libri=libri, anno_corrente=anno_corrente)
    else:
        #ACCESSO NON CONSENTITO; ritorno home con errore
        return render_template('home.html', errore="Nome non valido. Seleziona un nome dalla lista.", anno_corrente=anno_corrente)
    
@app.route('/home2')
def verify_user2():
    name = session.get('name')
    return render_template('index.html', name=name, libri=libri, anno_corrente=anno_corrente)

@app.route('/infodati', methods=['POST'])
def dati():
    e = None
    name = request.form['name']
    email = request.form['email']

    if name in NOMI_VALIDI:
        informazioni = "Simone Carassale, 3E, altre informazioni"
        oggetto = "PickONE Library PRIVACY"
        format_email = f"Ciao {name},\ncome richiesto, ecco tutte le informazioni che PickONE Library ha su di te.\n\n-------------\nINFORMAZIONI: {informazioni}\n-------------\n\nCordiali Saluti,\n© PickONE Library"
        e = manda_mail(email, oggetto, format_email)
        if e:
            return render_template('info.html', errore="Non è stato possibile inviare l'e-mail. Riprova più tardi.", anno_corrente=anno_corrente)
        else:
            return render_template('info.html', errore="E-mail inviata correttamente! Controlla la casella di posta.", anno_corrente=anno_corrente)
    else:
        return render_template('info.html', errore="Nome non valido. Seleziona un nome dalla lista.", anno_corrente=anno_corrente)

@app.route('/info')
def info_oneai():
    name = session.get('name')
    return render_template('info.html', anno_corrente=anno_corrente, name=name)

app.run(debug=True)