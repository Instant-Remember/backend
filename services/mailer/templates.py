from email.message import EmailMessage


class BaseEmailMessage:
    _message = EmailMessage


def ResetPasswordMessage(token):
    subject = "Reset passord"
    message = "Your new password:"
