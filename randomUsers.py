from util.user import User
import names
import random as r

def populate():
    for x in range(50):
        gen = r.choice(["Male", "Female"])
        format = lambda input : input if len(f"{input}") > 1 else f"0{input}"
        date = f"{r.randint(2000, 2019)}-{format(r.randint(1, 12))}-{format(r.randint(10, 28))}"
        #username = ""
        #for i in range(10):
        #    username += r.choice(string.ascii_lowercase)
        User.new_user(x, "", names.get_full_name(gender=gen.lower()), gen, r.choice(["Both", "Males", "Females"]), date, "dummy email", "dummy phone number", "lorem ipsum shut up", f"{r.uniform(35, 45)},{r.uniform(-80, 70)}")
