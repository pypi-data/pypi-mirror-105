import requests
from hypixelpy.exceptions import InvalidApiKeyException


class Other:
    def __init__(self, key):
        self.api_key = key

    def __make_request(self, url):
        """
        Private method used for making GET requests.
        DO NOT use this method.
        """
        try:
            r = requests.get(f'{url}?key={self.api_key}').json()

            if not r['success']:
                if r['cause'] == 'Invalid API key':
                    raise InvalidApiKeyException(f'Cause: {r["cause"]}')
            else:
                return r
        except requests.RequestException as e:
            raise e

    def active_network_boosters(self) -> dict:
        """
        Gets all the active network boosters
        """
        return self.__make_request('https://api.hypixel.net/boosters')

    def players_count(self) -> dict:
        """
        Gets all online players count
        """
        return self.__make_request('https://api.hypixel.net/counts')

    def current_leaderboard(self) -> dict:
        """
        Gets the current leaderboard from all mini games
        """
        return self.__make_request('https://api.hypixel.net/leaderboards')

    def punishment_statistics(self) -> dict:
        """
        Gets the punishment statistics
        """
        return self.__make_request('https://api.hypixel.net/punishmentstats')
