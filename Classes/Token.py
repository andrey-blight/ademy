from os import environ

import requests
from cryptography.fernet import Fernet

from Classes.ServerBuilder import ServerBuilder


class Token:
    TIME_EXPIRATION: int = 0  # Never expires

    def __init__(self):
        self._secret_key: str = environ.get("SECRET_KEY")
        self._encryption = Fernet(b'CtJTNc5Ei-DPioGiaNYDJFsrpuaD8hfWOZrUG9pWhcA=')
        self._server_host = ServerBuilder().get_server()

    def is_token_valid(self, encrypted_token: str) -> bool:
        # Decrypting encrypted token
        decrypted_token = self._encryption.decrypt(bytes(encrypted_token.encode("utf-8")))
        data = decrypted_token.decode("utf-8").split('.')
        # Request to API
        request = requests.get(f'{self._server_host}/api/v1/user/{data[1]}')
        if request.status_code != 200:
            return False
        # Checking valid secret key, valid user id and expiration time
        if data[0] == str(self._secret_key) and int(data[2]) == self.TIME_EXPIRATION:
            return True
        else:
            return False

    def get_token(self, user_id: int) -> str:
        data: dict = {
            "key": f"{self._secret_key}",
            "id": f"{user_id}",
            "expiration": f"{self.TIME_EXPIRATION}"
        }
        token: str = f"{data['key']}.{data['id']}.{data['expiration']}"
        encrypted_token = self._encryption.encrypt(bytes(token.encode("utf-8"))).decode("utf-8")
        return encrypted_token
