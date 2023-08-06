from hypixelpy.api import Api
from hypixelpy.player import Player
from hypixelpy.resources import Resources
from hypixelpy.skyblock import Skyblock
from hypixelpy.other import Other
from hypixelpy.gametypes import GameTypes

class Hypixel:
    def __init__(self, key):
        self.api_key = key
#       self.header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'}

        self.api = Api(self.api_key)
        self.player = Player(self.api_key)
        self.resources = Resources(self.api_key)
        self.skyblock = Skyblock(self.api_key)
        self.other = Other(self.api_key)
        self.gametypes = GameTypes()
