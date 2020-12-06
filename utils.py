correct_list = ["Hasta la vista, baby", "Elementary, my dear Watson", "Life will find a way",
                "We came. We saw. We kicked its ass.", "Kumbayaa Kumbayaa!"]
wrong_list = ["I pity the fool", "Keep watching the skies!", "Let's go home, Debbie", "Houson, we have a problem",
              "One, two, Freddy's coming for you ...", "Mama says 'stupid is as stupid does",
              "Sometimes, you gotta say 'what the beep", "Oh, Moses, Moses, you stubborn, splendid, adorable fool."]
worst_list = ["You're tearing me apart!", "Open the pod bay doors, HAL.",
              "Naughty Naughty!"]

teams = [
    "arnold",
    "bergman",
    "brad",
    "cameron",
    "chadwick",
    "connery",
    "leonardo",
    "nolan",
    "spielberg",
    "stan",
    "sylvestor",
    "tarantino",
]

super_users = [755703395989585942, 743472398896070657]


def make_tries():
    tr = {}
    for i in teams:
        tr[i] = {'tries': {}}
    return tr


def make_scoreboard():
    ss = {}
    for i in teams:
        ss[i] = {"points": 0, "attended": []}
    return ss
