STAGES: set[str] = {"1-1", "1-2", "1-3", "1-4",
          "2-1", "2-2", "2-3", "2-4", "2-5", "2-6", "2-7",
          "3-1", "3-2", "3-3", "3-4", "3-5", "3-6", "3-7",
          "4-1", "4-2", "4-3", "4-4", "4-5", "4-6", "4-7",
          "5-1", "5-2", "5-3", "5-4", "5-5", "5-6", "5-7",
          "6-1", "6-2", "6-3", "6-4", "6-5", "6-6", "6-7",
          "7-1", "7-2", "7-3", "7-4", "7-5", "7-6", "7-7"}


COMPONENTS: set[str] = {
    "NeedlesslyLargeRod",
    "TearoftheGoddess",
    "SparringGloves",
    "Spatula",
    "NegatronCloak",
    "ChainVest",
    "RecurveBow",
    "BFSword",
    "GiantsBelt"
}

NORMAL_ITEMS: set[str] = {
                  "ArchangelsStaff", "ADMINEmblem", "Guardbreaker", "Bloodthirster",
                  "BlueBuff", "BrambleVest", "AnimaSquadEmblem", "ChaliceofPower",
                  "Deathblade", "DuelistEmblem", "DragonsClaw", "EdgeofNight",
                  "ProtectorsVow", "GargoyleStoneplate", "GiantSlayer", "HandofJustice",
                  "HextechGunblade", "InfinityEdge", "IonicSpark", "JewledGauntlet",
                  "LastWhisper", "LocketoftheIronSolari", "HeartEmblem", "LaserCorpsEmblem",
                  "Morellonomicon", "Quicksilver", "RabadonsDeathcap", "MascotEmblem",
                  "RapidFirecannon", "Redemption", "RunaansHurricane", "OxForceEmblem",
                  "ShroudofStillness", "SpearofShojin", "StatikkShiv", "SunfireCape",
                  "TacticiansCrown", "ThiefsGloves", "TitansResolve", "WarmogsArmor",
                  "ZekesHerald", "Zephyr", "ZZRotPortal", "RecurveBow",
                  "RenegadeEmblem", "GuinsoosRageblade"}

ELUSIVE_ITEMS: set[str] = {
                  "AstralEmblem", "BruiserEmblem", "Cannoneer Emblem",
                  "DragonmancersBlessing", "EvokerEmblem", "GuildEmblem",
                  "JadeEmblem", "LegendEmblem", "MysticEmblem",
                  "RevelEmblem", "ScalescornEmblem", "SwiftshotEmblem",
                  "TempestEmblem", "WarriorEmblem", "WhispersEmblem"}

ORNN_ITEMS: set[str] = {
                  "AnimaVisage", "DeathsDefiance", "EternalWinter",
                  "GoldCollector", "InfinityForce",
                  "Manazane", "ObsidianCleaver", "RaduinsSanctum",
                  "RocketPropelledFist", "ZhonyasParadox"}

RADIANT_ITEMS: set[str] = {
                 "Absolution", "BansheesSilence", "BlessedBloodthirster",
                 "BlueBlessing", "BrinkofDawn", "ChaliceofCharity",
                 "CovalentSpark", "DemonSlayer", "DragonsWill",
                 "DvarapalaStoneplate", "EternalWhisper", "FistofFairness",
                 "BulwarksOath", "GlamorousGauntlet", "GuinsoosReckoning",
                 "HextechLifeblade", "LocketofTargonPrime", "LuminousDeathblade",
                 "Mistral", "MoreMoreellonomicon", "Quickestsilver",
                 "RabadonsAscendedDeathcap", "RadiantRedemption", "RapidLightcannon",
                 "RascalsGloves", "RosethornVest", "RunaansTempest",
                 "ShroudofReverance", "SpearofHirana", "StatikkFavor",
                 "SunlightCape", "TitansVow", "UrfAngelsStaff",
                 "WarmogsPride", "ZekesHarmony", "ZenithEdge",
                 "ZzRotsInvitation"}


ITEMS: set[str] = COMPONENTS.union(NORMAL_ITEMS).union(ELUSIVE_ITEMS).union(ORNN_ITEMS).union(RADIANT_ITEMS)


ITEM_TO_COMPONENTS = {"ArchangelsStaff": ("NeedlesslyLargeRod", "TearoftheGoddess"),
              "RenegadeEmblem": ("SparringGloves", "Spatula"),
              "Guardbreaker": ("GiantsBelt", "SparringGloves"),
              "Bloodthirster": ("BFSword", "NegatronCloak"),
              "BlueBuff": ("TearoftheGoddess", "TearoftheGoddess"),
              "BrambleVest": ("ChainVest", "ChainVest"),
              "OxForceEmblem": ("ChainVest", "Spatula"),
              "ChaliceofPower": ("NegatronCloak", "TearoftheGoddess"),
              "Deathblade": ("BFSword", "BFSword"),
              "AnimaSquadEmblem": ("NeedlesslyLargeRod", "Spatula"),
              "DragonsClaw": ("NegatronCloak", "NegatronCloak"),
              "EdgeofNight": ("BFSword", "ChainVest"),
              "ProtectorsVow": ("ChainVest", "TearoftheGoddess"),
              "GargoyleStoneplate": ("ChainVest", "NegatronCloak"),
              "GiantSlayer": ("BFSword", "RecurveBow"),
              "MascotEmblem": ("GiantsBelt", "Spatula"),
              "GuinsoosRageblade": ("NeedlesslyLargeRod", "RecurveBow"),
              "HandofJustice": ("SparringGloves", "TearoftheGoddess"),
              "HextechGunblade": ("BFSword", "NeedlesslyLargeRod"),
              "InfinityEdge": ("BFSword", "SparringGloves"),
              "IonicSpark": ("NeedlesslyLargeRod", "NegatronCloak"),
              "JeweledGauntlet": ("NeedlesslyLargeRod", "SparringGloves"),
              "LastWhisper": ("RecurveBow", "SparringGloves"),
              "LocketoftheIronSolari": ("ChainVest", "NeedlesslyLargeRod"),
              "HeartEmblem": ("TearoftheGoddess", "Spatula"),
              "ADMINEmblem": ("NegatronCloak", "Spatula"),
              "Morellonomicon": ("GiantsBelt", "NeedlesslyLargeRod"),
              "Quicksilver": ("NegatronCloak", "SparringGloves"),
              "RabadonsDeathcap": ("NeedlesslyLargeRod", "NeedlesslyLargeRod"),
              "DuelistEmblem": ("RecurveBow", "Spatula"),
              "RapidFirecannon": ("RecurveBow", "RecurveBow"),
              "Redemption": ("GiantsBelt", "TearoftheGoddess"),
              "RunaansHurricane": ("NegatronCloak", "RecurveBow"),
              "LaserCorpsEmblem": ("BFSword", "Spatula"),
              "ShroudofStillness": ("ChainVest", "SparringGloves"),
              "SpearofShojin": ("BFSword", "TearoftheGoddess"),
              "StatikkShiv": ("RecurveBow", "TearoftheGoddess"),
              "SunfireCape": ("ChainVest", "GiantsBelt"),
              "TacticiansCrown": ("Spatula", "Spatula"),
              "ThiefsGloves": ("SparringGloves", "SparringGloves"),
              "TitansResolve": ("ChainVest", "RecurveBow"),
              "WarmogsArmor": ("GiantsBelt", "GiantsBelt"),
              "ZekesHerald": ("BFSword", "GiantsBelt"),
              "Zephyr": ("GiantsBelt", "NegatronCloak"),
              "ZzRotPortal": ("GiantsBelt", "RecurveBow")
}

COMPONENTS_TO_ITEM = {v: k for k, v in ITEM_TO_COMPONENTS.items()}


CHAMPIONS: dict[str, dict[str, int]] = {
    "Nasus": {"Gold": 1},
    "Galio": {"Gold": 1},
    "Poppy": {"Gold": 1},
    "Wukong": {"Gold": 1},
    "Ashe": {"Gold": 1},
    "Lux": {"Gold": 1},
    "Sylas": {"Gold": 1},
    "Blitzcrank": {"Gold": 1},
    "Renekton": {"Gold": 1},
    "Kayle": {"Gold": 1},
    "GangPlank": {"Gold": 1},
    "Lulu": {"Gold": 1},
    "Talon": {"Gold": 1},
    "Malphite": {"Gold": 2},
    "Yuumi": {"Gold": 2},
    "Rell": {"Gold": 2},
    "Ezreal": {"Gold": 2},
    "Annie": {"Gold": 2},
    "Camille": {"Gold": 2},
    "LeeSin": {"Gold": 2},
    "Vi": {"Gold": 2},
    "Fiora": {"Gold": 2},
    "Yasuo": {"Gold": 2},
    "Jinx": {"Gold": 2},
    "Draven": {"Gold": 2},
    "Sivir": {"Gold": 2},
    "Velkoz": {"Gold": 3},
    "ChoGath": {"Gold": 3},
    "Rammus": {"Gold": 3},
    "Alistar": {"Gold": 3},
    "Riven": {"Gold": 3},
    "Vayne": {"Gold": 3},
    "Kaisa": {"Gold": 3},
    "Sona": {"Gold": 3},
    "LeBlanc": {"Gold": 3},
    "Zoe": {"Gold": 3},
    "Nilah": {"Gold": 3},
    "Senna": {"Gold": 3},
    "Jax": {"Gold": 3},
    "Zed": {"Gold": 4},
    "Taliyah": {"Gold": 4},
    "Viego": {"Gold": 4},
    "Sejuani": {"Gold": 4},
    "Soraka": {"Gold": 4},
    "Ekko": {"Gold": 4},
    "Samira": {"Gold": 4},
    "MissFortune": {"Gold": 4},
    "Sett": {"Gold": 4},
    "AurelionSol": {"Gold": 4},
    "Zac": {"Gold": 4},
    "BelVeth": {"Gold": 4},
    "Nunu": {"Gold": 5},
    "Syndra": {"Gold": 5},
    "Aphelios": {"Gold": 5},
    "Janna": {"Gold": 5},
    "Leona": {"Gold": 5},
    "Mordekaiser": {"Gold": 5},
    "Fiddlesticks": {"Gold": 5},
    "Urgot": {"Gold": 5},
}


def unit_gold(unit: str) -> int:
    """Returns cost of a unit."""
    return CHAMPIONS[unit]["Gold"]

