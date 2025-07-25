import gmpy2
from gmpy2 import mpz, powmod, next_prime, mpz_random, random_state
import json
import os
import random
def prover(username, password, serial,p):
    rand = random_state(hash(os.urandom(32)))
    u = mpz(username) 
    k = mpz(password)
    c = mpz(serial)

    l = mpz_random(rand, p - 1) + 1

    c1 = powmod(c, l, p)
    c2 = powmod(u, l, p)
    c3 = powmod(k, l, p)
    
    return c1, c2, c3

def verifier(c1, c2, c3, s, p): 
    
    r = powmod(c2*c3, s, p)
 
    return r == c1

def load_database(un_path,pw_path,se_path):
    with open(un_path, "r") as f:
        usernames = json.load(f)
    with open(pw_path, "r") as f:
        passwords = json.load(f)
    with open(se_path, "r") as f:
        serials = json.load(f)
    return usernames, passwords, serials    
def main():
    with open("params.json", "r") as f:
        params = json.load(f)
    p = mpz(params['p'])
    s = mpz(params['s'])

    usernames, passwords, serials = load_database("usernames_database.json", "passwords_database.json", "serials_database.json") 

    tot_num = 0
    verified = 0
    for i in range(len(usernames)):
        tot_num+=1
        username = int(usernames[i])
        password = int(passwords[i])

        serial = int(serials[i])
        c1, c2, c3 = prover(username,password,serial,p)
        verification = verifier(c1,c2,c3,s,p)
        if(verification):
            print('user '+str(i+1)+' is verified successfully!')
            verified+=1
        else:
            print('Verification failed!')
    print('%'+str(100*verified/tot_num)+' was verified successfully!')
if __name__=='__main__':
     main()