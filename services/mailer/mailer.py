from config.settings import SMTP

import smtplib


from email.message import EmailMessage


class Mailer:
    __host = SMTP["HOST"]
    __port = SMTP["PORT"]
    __user = SMTP["USER"]
    __password = SMTP["PASS"]

    @staticmethod
    def send_email(email, m):
        message = EmailMessage()

        message.set_content(m)
        message["Subject"] = "Test"
        message["From"] = "instantremember@yandex.ru"
        message["To"] = email

        mailer = smtplib.SMTP_SSL(Mailer.__host, Mailer.__port)
        mailer.login(Mailer.__user, Mailer.__password)

        mailer.send_message(message)
        mailer.quit()
