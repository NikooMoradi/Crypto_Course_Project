import gmpy2
from gmpy2 import mpz, powmod, next_prime, mpz_random, random_state
import json
import os
import random

def registration(username, password, p, s):
    c = powmod(username*password,s,p)
    return c

def generate_users(p, s, num):
    usernames = []
    passwords = []
    serials = []
    for i in range(num):
        rand = random_state(hash(os.urandom(32)))
        username = mpz_random(rand, p - 1) + 1
        password =  mpz_random(rand, p - 1) + 1
        user_record = registration(username, password, p, s)
        usernames.append(str(username))
        passwords.append(str(password))
        serials.append(str(user_record))
    return usernames, passwords, serials
 
def main():
    with open("params.json", "r") as f:
        params = json.load(f)
    p = int(params['p'])
    s = int(params['s'])

    num = 1000
    usernames, passwords, serials = generate_users(p, s, num)
    with open("usernames_database.json", "w") as f:
        json.dump(usernames, f)
    with open("passwords_database.json", "w") as f:
        json.dump(passwords, f)
    with open("serials_database.json", "w") as f:
        json.dump(serials, f)    
if __name__=='__main__':
     main()

