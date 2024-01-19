import smtplib
import os
from email.message import EmailMessage

send_email_declaration = {
    "name": "send_mail",
    "description": "Sends an email using SMTP with a specified subject, body, and recipient.",
    "parameters": {
        "type": "object",
        "properties": {
            "subject": {
                "type": "string",
                "description": "The subject of the email"
            },
            "body": {
                "type": "string",
                "description": "The body content of the email"
            },
            "to_email": {
                "type": "string",
                "description": "The recipient's email address"
            }
        },
        "required": ["subject", "body", "to_email"]
    },
}

def send_mail(subject, body, to_email):
    sender = "Private Person <from@example.com>"

    message = EmailMessage()
    message.set_content(body)
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = to_email

    smtp_password = os.environ.get('SMTP_PASSWORD')  

    with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
        server.login("78241a213408f2", smtp_password)
        server.send_message(message)
        return "Email has been sent"

# send_mail('Testmail', 'Dear Mr. X ...', 'bob@foe.de')