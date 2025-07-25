# cryptosystem.py
from py_ecc.bn128 import G1, G2, multiply
from utils import get_random_scalar, p

class SystemSetup:
    """
    Handles the generation of public parameters and authority keys
    """
    def __init__(self):
        # 1. Define generators for G1 and G2
        self.g = G1
        self.g1 = multiply(G1, get_random_scalar())
        self.h_T = multiply(G1, get_random_scalar())
        self.g3 = G2
        
        # 2. Designated authority generates its key pair
        self.y = get_random_scalar() # Private key
        self.Y = multiply(self.g3, self.y) # Public key

        self.params = {
            'g': self.g,
            'g1': self.g1,
            'h_T': self.h_T,
            'g3': self.g3,
            'Y': self.Y,
            'p': p
        }
    
    def generate_signatures_for_set(self, public_set):
        """
        The designated authority issues BB-signatures for each element
        [cite_start]of the public set Φ[cite: 379, 380].
        """
        signatures = {}
        for k in public_set:
            # Ak = g^(1/(y+k))
            if (self.y + k) % p == 0:
                continue # Avoid division by zero
            inv = pow(self.y + k, -1, p)
            A_k = multiply(self.g, inv)
            signatures[k] = A_k
        return signatures