from smtplib import SMTP
from email.message import EmailMessage
from django.conf import settings
import random
import string

def sendMail(email, otp):
    try:
        msg = EmailMessage()
        msg.set_content(f"Your otp for the verification is: {otp}")
        msg['Subject'] = "Pizza Delivery Email verification"
        msg['From'] = settings.FROM_EMAIL
        msg['To'] = email

        server = SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(settings.FROM_EMAIL, settings.FROM_EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except:
        print("an error occured at time of sending email")
        return False

def generate_otp(length=6):
    characters = string.digits
    otp = ''.join(random.choice(characters) for _ in range(length))
    return otp