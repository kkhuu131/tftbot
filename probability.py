# probabilities of 1,2,3,4,5 costs at levels 1-10
level_chart = [
    [1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0],
    [.75, .25, 0, 0, 0],
    [.55, .3, .15, 0, 0],
    [.45, .33, .2, .02, 0],
    [.25, .4, .3, .05, 0],
    [.19, .3, .35, .15, .01],
    [.16, .2, .35, .25, .04],
    [.09, .15, .3, .3, .16],
    [.05, .1, .2, .4, .25]
]

# number of copies of a 1,2,3,4,5 tier unit
unit_numbers = [29, 22, 18, 12, 10]

# number of unique 1,2,3,4,5 tier units
unique_units = [13, 13, 13, 12, 8]


def get_tier_probability(level, tier):
    """
    Returns probability of units with a given tier at a given level.
    """
    return level_chart[level-1][tier-1]


def get_unit_numbers(tier):
    """
    Returns number of a unit with a given tier.
    """
    return unit_numbers[tier-1]


def get_unique_units(tier):
    """
    Returns number of unique units with a given tier.
    """
    return unique_units[tier-1]


def exp_unit_base(level, tier):
    """
    Returns number of expected units from one shop when none are out of pool
    """
    return 5*(get_tier_probability(level, tier)*(1.0/get_unique_units(tier)))


def n_exp_unit_base(level, tier, rolls):
    """
    Returns number of expected units from a given number of shops when none are out of pool
    """
    return rolls*5*(get_tier_probability(level, tier)*(1.0/get_unique_units(tier)))


def exp_unit(level, tier, taken):
    """
    Returns number of expected units from one shop
    """
    return 5*(get_tier_probability(level, tier)*(1.0/get_unique_units(tier)))*((get_unit_numbers(tier)-taken)/get_unit_numbers(tier))


def n_exp_unit(level, tier, taken, rolls):
    """
    Returns number of expected units from a given number of shops
    """
    return rolls*5*(get_tier_probability(level, tier)*(1.0/get_unique_units(tier)))*((get_unit_numbers(tier)-taken)/get_unit_numbers(tier))


def prob_find_n_units(level, tier, rolls, n):
    """
    Returns probability to find exactly n number of units in a given number of rolls.
    """
    desired_unit_total = get_unit_numbers(tier)
    desired_units_left = get_unit_numbers(tier)
    number_of_slots = rolls*5

    number_of_tier_units = number_of_slots*(get_tier_probability(level, tier))

    total_probability = 1

    return 1
