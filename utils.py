correct_list = ["Hasta la vista, baby", "Elementary, my dear Watson", "Life will find a way",
                "We came. We saw. We kicked its ass.", "Kumbayaa Kumbayaa!"]
wrong_list = ["I pity the fool", "Keep watching the skies!", "Let's go home, Debbie", "Houson, we have a problem",
              "One, two, Freddy's coming for you ...", "Mama says 'stupid is as stupid does",
              "Sometimes, you gotta say 'what the beep", "Oh, Moses, Moses, you stubborn, splendid, adorable fool."]
worst_list = ["You're tearing me apart!", "Open the pod bay doors, HAL.",
              "Naughty Naughty!"]

teams = [
    787177630889017374,
    787178184105263124,
    787178432055738378,
    787178495251316756,
    787178633130934282,
    787178688567050260,
    787178736658153502,
    787178848386154596,
    787178919299907614,
    787178979718201364,
    787179031338549318,
    787179081103310878,
]

team_name = [
    'january',
    'february',
    'march',
    'april',
    'may',
    'june',
    'july',
    'august',
    'september',
    'october',
    'november',
    'december'
]

super_users = [755703395989585942, 743472398896070657]


def get_teams():
    names = {}
    for i in range(len(teams)):
        names[team_name[i]] = teams[i]
    return names


def make_scoreboard():
    ss = {}
    for i in team_name:
        ss[i] = {"points": 0}
    return ss
