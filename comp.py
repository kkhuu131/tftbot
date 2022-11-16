# COMP VARIABLES

COMP = {
    "Gangplank": {
        "position": (0, 3),
        "items": [],
        "star": 3,
    },
    "Fiora": {
        "position": (3, 3),
        "items": ["GuinsoosRageblade", "HandOfJustice", "GiantSlayer"],
        "star": 3,
    },
    "LeeSin": {
        "position": (0, 6),
        "items": [],
        "star": 3,
    },
    "Malphite": {
        "position": (0, 4),
        "items": [],
        "star": 3,
    },
    "Yasuo": {
        "position": (1, 5),
        "items": ["GuinsoosRageblade", "HandOfJustice", "GiantSlayer"],
        "star": 3,
    },
    "Alistar": {
        "position": (0, 1),
        "items": [],
        "star": 2,
    },
    "Zoe": {
        "position": (3, 6),
        "items": [],
        "star": 2,
    },
    "Zed": {
        "position": (1, 1),
        "items": [],
        "star": 2,
    },
}

# set ideal augments (order matters) and unplayable augments
TARGET_AUGMENTS: set[str] = [
]

AVOID_AUGMENTS: set[str] = [
]