import smtplib
import os
from email.message import EmailMessage

destinatario = "sbubolo"
oggetto = "Prova e-mail con Python"
testo = "Ciao questa è una prova"


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
        print("Errore: " + str(e))

manda_mail(destinatario, oggetto, testo)