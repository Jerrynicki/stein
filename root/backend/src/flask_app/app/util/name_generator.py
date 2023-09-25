import random

def generate_username():
    # TODO emira

    steine = ["fels", "stein", "kies", "kiesel", "geoden"]
    nomen = ["liebhaber", "fan", "enjoyer"]

    return random.choice(steine) + random.choice(nomen) + str(random.randint(10, 99))