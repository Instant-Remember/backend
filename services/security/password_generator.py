import secrets
import string

alphabet = string.ascii_letters + string.digits

def generate():
    password = ''.join(secrets.choice(alphabet) for i in range(20))

    return password
