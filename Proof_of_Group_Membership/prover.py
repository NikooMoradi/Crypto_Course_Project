# prover.py
from py_ecc.bn128 import add, multiply, neg
from utils import (
    get_random_scalar, hash_to_int, serialize_point, p
)

class Prover:
    """
    The Prover, who wants to prove membership of a secret 'k' in a public set.
    """
    def __init__(self, secret_k, signature_A_k, params):
        self.k = secret_k
        self.A_k = signature_A_k # The BB-signature for k: g^(1/(y+k)) 
        self.params = params

    def generate_proof(self):
        """
        Generates the full non-interactive proof Π, following the protocol in Figure 4.
        This is a Fiat-Shamir transformation of the described Sigma protocol.
        """
        # Unpack params for easier access
        g, g1, h_T = self.params['g'], self.params['g1'], self.params['h_T']

        # === Prover's Pre-computations ===
        # Choose ν and compute commitment Com
        nu = get_random_scalar()
        Com = add(multiply(g1, self.k), multiply(h_T, nu)) # Com = g1^k * h_T^ν

        # Choose l, randomize signature A_k into B, and compute D
        l = get_random_scalar()
        B = multiply(self.A_k, l) # B = A_k^l
        B1 = neg(B) # B1 = B^(-1)
        D = add(multiply(B1, self.k), multiply(g, l)) # D = B1^k * g^l

        # === Real-time computations (for ZKPK) ===
        # 1. Commit to witnesses (k, ν, l)
        k1, r1, l1 = get_random_scalar(), get_random_scalar(), get_random_scalar()
        Com1 = add(multiply(g1, k1), multiply(h_T, r1)) # Com1 = g1^k1 * h_T^r1 
        D1 = add(multiply(B1, k1), multiply(g, l1)) # D1 = B1^k1 * g^l1 

        # 2. Compute challenge c using Fiat-Shamir heuristic 
        hash_input = (
            serialize_point(Com) + serialize_point(B) + serialize_point(D) +
            serialize_point(Com1) + serialize_point(D1)
        )
        c = hash_to_int(hash_input)
        
        # 3. Compute responses s1, s2, s3 
        s1 = (k1 + c * self.k) % p
        s2 = (r1 + c * nu) % p
        s3 = (l1 + c * l) % p

        # The final proof Π contains the main values, challenge and responses
        proof = {
            "Com": Com, "B": B, "D": D, "c": c,
            "s1": s1, "s2": s2, "s3": s3
        }
        return proof