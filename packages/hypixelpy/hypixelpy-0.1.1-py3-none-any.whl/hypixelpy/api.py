import requests
from hypixelpy.exceptions import InvalidApiKeyException


class Api:
    def __init__(self, key):
        self.api_key = key

    def key_information(self) -> dict:
        """
        Gets all the information about the API's key
        :return: dict
        """
        try:
            r = requests.get(f'https://api.hypixel.net/key?key={self.api_key}').json()
            if not r['success']:
                raise InvalidApiKeyException(r['cause'])
            else:
                return r
        except requests.RequestException as e:
            raise e
