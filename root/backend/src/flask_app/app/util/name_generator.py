import random

def generate_username():
    steine = ["fels", "stein", "kies", "kiesel", "geoden", "mineralien", ""]
    nomen = ["liebhaber", "fan", "sucher", "finder", "freund", "künstler", "conoisseur", "kenner", "krieger"]

    return random.choice(steine) + random.choice(nomen)+ random.choice(["", "in"]) + str(random.randint(10, 99))