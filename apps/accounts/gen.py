import string
from random import choice, randint
min_char = 8
max_char = 12
# allchar = string.ascii_letters + string.punctuation + string.digits
allchar = string.ascii_letters + string.digits
password = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
print("This is your password : ", password)
