import requests


class Resources:
    def __init__(self, key):
        self.api_key = key

    def __make_request(self, url: str):
        """
        Private method used for making GET requests.
        DO NOT use this method.
        """
        try:
            r = requests.get(url).json()
            return r
        except requests.RequestException as e:
            raise e

    def achievements(self) -> dict:
        """
        Gets a list of all Hypixel's achievements
        """
        return self.__make_request('https://api.hypixel.net/resources/achievements')

    def challenges(self) -> dict:
        """
        Gets a list of all Hypixel's challenges
        """
        return self.__make_request('https://api.hypixel.net/resources/challenges')

    def quests(self) -> dict:
        """
        Gets a list of all Hypixel's quest
        """
        return self.__make_request('https://api.hypixel.net/resources/quests')
    
    def guild_achievements(self) -> dict:
        """
        Gets a list of all Hypixel's guild achievements
        """
        return self.__make_request('https://api.hypixel.net/resources/guilds/achievements')

    def guild_permissions(self) -> dict:
        """
        Gets a list of all Hypixel's guild permissions
        """
        return self.__make_request('https://api.hypixel.net/resources/guilds/permissions')
