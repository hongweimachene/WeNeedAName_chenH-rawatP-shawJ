from util.user import User
import names
import random as r

'''Creates a bunch of dummy accounts to store in database'''
for x in range(50):
    date = str(r.randint(2000, 2019)) + "-" + str(r.randint(1, 12)) + "-" + str(r.randint(1, 28))
    User.new_user(x , "", names.get_full_name(), "Male", "Both", date, "dummy email", "dummy phone number", "lorem ipsum shut up", "yeet street")
