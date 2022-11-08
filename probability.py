from scipy.stats import hypergeom

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


def prob_find_n_units_base(level, tier, rolls, desired):
    """
    Returns probability to find at least n number of units in a given number of rolls.
    """

    # Math from https://tft.teamward.xyz/

    # first Hypergeometric distribution
    # M: total balls, n: number of success balls, k: amount to get less than or equal to, N: total draws
    M = get_unit_numbers(tier)*get_unique_units(tier) / get_tier_probability(level, tier)
    n = get_unit_numbers(tier)
    k = desired-1
    N = 5*rolls
    # probability to get < desired amount of units
    cdf1 = hypergeom.cdf(k, M, n, N)

    # second Hypergeometric distribution
    # M: total balls, n: number of success balls, k: amount to get less than or equal to, N: total draws
    M = 5*rolls + get_unit_numbers(tier) * get_unique_units(tier) / get_tier_probability(level, tier)
    n = get_unit_numbers(tier)
    k = desired - 1
    N = 5 * rolls
    # probability to get < desired amount of units
    cdf2 = hypergeom.cdf(k, M, n, N)

    # take average of both distributions
    cdf = (cdf1+cdf2)/2

    # probability to get at least desired amount of units
    prob = 1-cdf
    return prob


def prob_find_n_units(level, tier, rolls, desired, desired_taken, same_tier_taken):
    """
    Returns probability to find at least n number of units in a given number of rolls.
    """

    # Math from https://tft.teamward.xyz/

    # first Hypergeometric distribution
    # M: total balls, n: number of success balls, k: amount to get less than or equal to, N: total draws
    M = get_unit_numbers(tier)*get_unique_units(tier) - same_tier_taken / get_tier_probability(level, tier)
    n = get_unit_numbers(tier)-desired_taken
    k = desired-1
    N = 5*rolls
    # probability to get < desired amount of units
    cdf1 = hypergeom.cdf(k, M, n, N)

    # second Hypergeometric distribution
    # M: total balls, n: number of success balls, k: amount to get less than or equal to, N: total draws
    M = 5*rolls + get_unit_numbers(tier) * get_unique_units(tier) - same_tier_taken / get_tier_probability(level, tier)
    n = get_unit_numbers(tier)-desired_taken
    k = desired - 1
    N = 5 * rolls
    # probability to get < desired amount of units
    cdf2 = hypergeom.cdf(k, M, n, N)

    # take average of both distributions
    cdf = (cdf1+cdf2)/2

    # probability to get at least desired amount of units
    prob = 1-cdf
    return prob

