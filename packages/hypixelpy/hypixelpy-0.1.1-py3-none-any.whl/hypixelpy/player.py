import requests
from hypixelpy.exceptions import *


class Player:
    def __init__(self, key):
        self.api_key = key

    def __make_request(self, url, uuid):
        """
        Private method used for making GET requests.
        DO NOT use this method.
        """
        try:
            r = requests.get(f'{url}?key={self.api_key}&uuid={uuid}').json()

            if not r['success']:
                if r['cause'] == 'Invalid API key':
                    raise InvalidApiKeyException(f'Cause: {r["cause"]}')
                elif r['cause'] == 'Malformed UUID':
                    raise MalformedUUIDException(f'Cause: {r["cause"]}')
            else:
                return r
        except requests.RequestException as e:
            raise e

    def uuid(self, username: str) -> str:
        """
        Converts username to UUID.
        """
        r = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{username}').status_code

        # if the username is invalid, the HTTP code will be 204
        if r == 204:
            raise NoContentException(f'The request made has no content.')
        else:
            return requests.get(f'https://api.mojang.com/users/profiles/minecraft/{username}').json()['id']

    def data(self, uuid: str) -> dict:
        """
        Gets all the data available from the player
        """
        return self.__make_request('https://api.hypixel.net/player', uuid)

    def friends(self, uuid) -> dict:
        """
        Gets a list of friends from a the given player.
        If the player has no friends, the 'record' element will be empty
        """
        return self.__make_request('https://api.hypixel.net/friends', uuid)

    def recent_games(self, uuid) -> dict:
        """
        Gets all recently played games from the given player
        """
        return self.__make_request('https://api.hypixel.net/recentgames', uuid)

    def status(self, uuid) -> dict:
        """
        Gets the status of a given player.
        """
        return self.__make_request('https://api.hypixel.net/status', uuid)

    def guild(self, uuid):
        """
        Work in progress
        """
        pass
