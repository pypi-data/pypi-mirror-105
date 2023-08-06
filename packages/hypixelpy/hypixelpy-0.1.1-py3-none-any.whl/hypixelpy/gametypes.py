import os
import json


class GameTypes:
    def __init__(self):
        self.data = '{"gametypes": {"quake": {"id": 2, "type_name": "QUAKECRAFT", "db_name": "Quake", "clean_name": "Quake"}, "walls": {"id": 3, "type_name": "WALLS", "db_name": "Walls", "clean_name": "Walls"}, "paintball": {"id": 4, "type_name": "PAINTBALL", "db_name": "Paintball", "clean_name": "Paintball"}, "blitz_survival_games": {"id": 5, "type_name": "SURVIVAL_GAMES", "db_name": "HungerGames", "clean_name": "Blitz Survival Games"}, "tnt_games": {"id": 6, "type_name": "TNTGAMES", "db_name": "TNTGames", "clean_name": "TNT Games"}, "vampirez": {"id": 7, "type_name": "VAMPIREZ", "db_name": "VampireZ", "clean_name": "VampireZ"}, "mega_walls": {"id": 13, "type_name": "WALLS3", "db_name": "Walls3", "clean_name": "Mega Walls"}, "arcade": {"id": 14, "type_name": "ARCADE", "db_name": "Arcade", "clean_name": "Arcade"}, "arena": {"id": 17, "type_name": "ARENA", "db_name": "Arena", "clean_name": "Arena"}, "uhc_champions": {"id": 20, "type_name": "UHC", "db_name": "UHC", "clean_name": "UHC Champions"}, "cops_and_crims": {"id": 21, "type_name": "MCGO", "db_name": "MCGO", "clean_name": "Cops and Crims"}, "warlords": {"id": 23, "type_name": "BATTLEGROUND", "db_name": "Battleground", "clean_name": "Warlords"}, "smash_heroes": {"id": 24, "type_name": "SUPER_SMASH", "db_name": "SuperSmash", "clean_name": "Smash Heroes"}, "turbo_kart_racers": {"id": 25, "type_name": "GINGERBREAD", "db_name": "GingerBread", "clean_name": "Turbo Kart Racers"}, "housing": {"id": 26, "type_name": "HOUSING", "db_name": "Housing", "clean_name": "Housing"}, "skywars": {"id": 51, "type_name": "SKYWARS", "db_name": "SkyWars", "clean_name": "SkyWars"}, "crazy_walls": {"id": 52, "type_name": "TRUE_COMBAT", "db_name": "TrueCombat", "clean_name": "Crazy Walls"}, "speed_uhc": {"id": 54, "type_name": "SPEED_UHC", "db_name": "SpeedUHC", "clean_name": "Speed UHC"}, "sky_clash": {"id": 55, "type_name": "SKYCLASH", "db_name": "SkyClash", "clean_name": "SkyClash"}, "classic_games": {"id": 56, "type_name": "LEGACY", "db_name": "Legacy", "clean_name": "Classic Games"}, "prototype": {"id": 57, "type_name": "PROTOTYPE", "db_name": "Prototype", "clean_name": "Prototype"}, "bed_wars": {"id": 58, "type_name": "BEDWARS", "db_name": "Bedwars", "clean_name": "Bed Wars"}, "murder_mystery": {"id": 59, "type_name": "MURDER_MYSTERY", "db_name": "MurderMystery", "clean_name": "Murder Mystery"}, "build_battle": {"id": 60, "type_name": "BUILD_BATTLE", "db_name": "BuildMystery", "clean_name": "Build Battle"}, "duels": {"id": 61, "type_name": "DUELS", "db_name": "Duels", "clean_name": "Duels"}, "skyblock": {"id": 63, "type_name": "SKYBLOCK", "db_name": "SkyBlock", "clean_name": "SkyBlock"}, "pit": {"id": 64, "type_name": "PIT", "db_name": "Pit", "clean_name": "Pit"}}}'
        self.game_types = json.loads(self.data)

    def get_all_ids(self) -> list:
        ids = []
        for i in self.game_types['gametypes']:
            ids.append(self.game_types['gametypes'][i]['id'])
        return ids

    def get_all_type_names(self) -> list:
        type_names = []
        for i in self.game_types['gametypes']:
            type_names.append(self.game_types['gametypes'][i]['type_name'])
        return type_names

    def get_all_db_names(self) -> list:
        db_names = []
        for i in self.game_types['gametypes']:
            db_names.append(self.game_types['gametypes'][i]['db_name'])
        return db_names

    def get_all_clean_names(self) -> list:
        clean_names = []
        for i in self.game_types['gametypes']:
            clean_names.append(self.game_types['gametypes'][i]['clean_name'])
        return clean_names
