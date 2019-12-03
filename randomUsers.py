from util.user import User
import names
import random as r

for x in range(50):
    date = str(r.randint(2000, 2019)) + "-" + str(r.randint(10, 12)) + "-" + str(r.randint(10, 28))
    User.new_user(x , "", names.get_full_name(), "Male", "Both", date, "dummy email", "dummy phone number", "lorem ipsum shut up", str(r.random()) + "," + str(r.random()))
