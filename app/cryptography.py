from cryptography.fernet import Fernet

from app.settings import settings

fernet = Fernet(settings.cryptography_key)
