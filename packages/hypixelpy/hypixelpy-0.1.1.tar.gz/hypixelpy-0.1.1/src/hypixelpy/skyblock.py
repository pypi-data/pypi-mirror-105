import requests
from hypixelpy.exceptions import InvalidApiKeyException


class Skyblock:
    def __init__(self, key):
        self.api_key = key

    def collections(self) -> dict:
        """
        Gets all the collections available in Skyblock
        :return: dict
        """
        try:
            r = requests.get(f'https://api.hypixel.net/resources/skyblock/collections').json()
            return r
        except requests.RequestException as e:
            raise e

    def skills(self) -> dict:
        """
        Gets all the skills available in Skyblock
        :return: dict
        """
        try:
            r = requests.get(f'https://api.hypixel.net/resources/skyblock/skills').json()
            return r
        except requests.RequestException as e:
            raise e

    def news(self) -> dict:
        """
        Gets Skyblock's news
        :return: dict
        """
        try:
            r = requests.get(f'https://api.hypixel.net/skyblock/news?key={self.api_key}').json()

            if not r['success']:
                if r['cause'] == 'Invalid API key':
                    raise InvalidApiKeyException(f'Cause: {r["cause"]}')
            else:
                return r
        except requests.RequestException as e:
            raise e

    def auctions(self, uuid: str, player: str, profile: str) -> dict:
        """
        Gets auctions by uuid, player and profile
        :param uuid: player's UUID
        :param player: UUID
        :param profile: profile's name
        :return: dict
        """
        try:
            r = requests.get(f'https://api.hypixel.net/skyblock/auction?key={self.api_key}'
                             f'&uuid={uuid}&player={player}&profile={profile}').json()

            if not r['success']:
                if r['cause'] == 'Invalid API key':
                    raise InvalidApiKeyException(f'Cause: {r["cause"]}')
            else:
                return r
        except requests.RequestException as e:
            raise e

    def active_auctions(self, page: int = 0) -> dict:
        """
        Gets the data from an active auction by page
        :param page: page number
        :return: dict
        """
        try:
            r = requests.get(f'https://api.hypixel.net/skyblock/auctions?page={page}').json()
            return r
        except requests.RequestException as e:
            raise e

    def ended_auctions(self) -> dict:
        """
        Gets all ended auctions in the last 60 seconds
        :return: dict
        """
        try:
            r = requests.get(f'https://api.hypixel.net/skyblock/auctions_ended').json()
            return r
        except requests.RequestException as e:
            raise e

    def bazaar(self) -> dict:
        """
        Gets all the data from bazaar
        :return: dict
        """
        try:
            r = requests.get(f'https://api.hypixel.net/skyblock/bazaar').json()
            return r
        except requests.RequestException as e:
            raise e

    def bazaar_products_id(self) -> list:
        """
        Gets all the bazaar's item ids
        :return: list
        """
        data = self.bazaar()
        items = []
        for p in data['products']:
            items.append(data['products'][p]['product_id'])

        return items

    def profile(self, uuid: str) -> dict:
        """
        Gets information about a given player
        :param uuid: player's uuid
        :return: dict
        """
        try:
            r = requests.get(f'https://api.hypixel.net/skyblock/profile?key={self.api_key}&profile={uuid}').json()

            if not r['success']:
                if r['cause'] == 'Invalid API key':
                    raise InvalidApiKeyException(f'Cause: {r["cause"]}')
            else:
                return r
        except requests.RequestException as e:
            raise e

    def player_profiles(self, uuid: str) -> dict:
        """
        Gets player's profiles
        :param uuid: player's uuid
        :return: dict
        """
        try:
            r = requests.get(f'https://api.hypixel.net/skyblock/profiles?key={self.api_key}&uuid={uuid}').json()

            if not r['success']:
                if r['cause'] == 'Invalid API key':
                    raise InvalidApiKeyException(f'Cause: {r["cause"]}')
            else:
                return r
        except requests.RequestException as e:
            raise e
