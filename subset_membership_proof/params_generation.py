import gmpy2
from gmpy2 import mpz, powmod, next_prime, mpz_random, random_state
import json
import os



def generate_public_params():
    rand = random_state(hash(os.urandom(32)))
    p = next_prime(mpz_random(rand, 2**2048))
    s = mpz_random(rand, p - 1) + 1
    return p, s

def main():
    p, s = generate_public_params()
    with open("params.json", "w") as f:
        json.dump({'p': str(p),'s': str(s)}, f)
    
if __name__=='__main__':
     main()