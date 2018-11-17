from json import loads
from random import choice

# Constant
K_FACTORS = 10
STARTING = 1000

# Variables
males_list = []
females_list = []

# Functions
def compare(name1, name2, is_female, score):
    """
    Compare two names
    :param name1: What is the first name?
    :param name2: Second name?
    :param is_female: Are both names female?
    :param score: 0 for First name losing, 1 for first name winning
    :return: None. Scores are updated
    """
    global males, females, K_FACTORS
    if is_female:
        old1, old2 = females[name1], females[name2]
        females[name1] = old1 + K_FACTORS * ((1-score) - expected(old1, old2))
        females[name2] = old2 + K_FACTORS * (score - expected(old2, old1))
        return females[name1], females[name2]
    else:
        old1, old2 = males[name1], males[name2]
        males[name1] = old1 + K_FACTORS * ((1-score) - expected(old1, old2))
        males[name2] = old2 + K_FACTORS * (score - expected(old2, old1))
        return males[name1], males[name2]


def expected(A, B):
    """
    Calculate expected score of A in a match against B
    :param A: Elo rating for player A
    :param B: Elo rating for player B
    """
    return 1 / (1 + 10 ** ((B - A) / 400))


def choose(is_female):
    # Pick two random, different names
    global females, males
    names = [choice(list(females.keys())), choice(list(females.keys()))] if is_female else [choice(list(males.keys())), choice(list(males.keys()))]
    while names[0] is names[1]: names = [choice(list(females.keys())), choice(list(females.keys()))] if is_female else [choice(list(males.keys())), choice(list(males.keys()))]
    return names

# Process names into ELO dictionary
names = loads(open('processed_names.json').read())
males, females = dict.fromkeys(names['male'], STARTING), dict.fromkeys(names['female'], STARTING)

choice1, choice2, = None, None

if __name__ == '__main__':
    while True:
        # Males
        choice1, choice2 = choice(list(males.keys())), choice(list(males.keys()))
        while choice1 is choice2:
            choice1, choice2 = choice(list(males.keys())), choice(list(males.keys()))
        my_choice = 1 if input(choice1 + " is cooler than " + choice2 + "\nanswer with y or n") == 'y' else 0
        print(compare(choice1, choice2, False, my_choice))
        # print(sorted(males, key=males.get))  # Create list of names from the sorted pile

        # Females
        choice1, choice2 = choice(list(females.keys())), choice(list(females.keys()))
        while choice1 is choice2:
            choice1, choice2 = choice(list(females.keys())), choice(list(females.keys()))
        my_choice = 1 if input(choice1 + " is cooler than " + choice2 + "\nanswer with y or n") == 'y' else 0
        print(compare(choice1, choice2, True, my_choice))
        # print(sorted(females, key=females.get))  # Create list of names from the sorted pile
