# verifier.py
from py_ecc.bn128 import pairing, add, multiply, neg
from utils import hash_to_int, serialize_point

class Verifier:
    """
    The Verifier, who checks the Prover's proof of membership.
    """
    def __init__(self, params, authority_private_key_y=None):
        self.params = params
        self.y = authority_private_key_y # Optional: verifier might have the key 'y'

    def verify_proof(self, proof):
        """
        [cite_start]Verifies the proof Π. Handles both cases described in the paper[cite: 383].
        """
        # Unpack params
        g, g1, h_T, g3, Y, p = self.params.values()
        
        # Unpack proof
        Com, B, D, c, s1, s2, s3 = proof.values()
        
        # [cite_start]1. Check that B is not the identity element [cite: 397]
        if B is None:
            print("❌ Verification failed: B is the identity element.")
            return False

        # 2. Verify D's integrity
        if self.y is not None:
            # [cite_start]First Case: Verifier knows y and can compute D directly [cite: 398, 399]
            expected_D = multiply(B, self.y) # D = B^y
            if D != expected_D:
                print("❌ Verification failed: D does not match expected D=B^y.")
                return False
            print("✅ D verified using private key y.")
        else:
            # [cite_start]Second Case: Verifier uses pairing to check D [cite: 400]
            # Check e(D, g3) == e(B, Y)
            left_pairing = pairing(g3, D)
            right_pairing = pairing(Y, B)
            if left_pairing != right_pairing:
                print("❌ Verification failed: Pairing check e(D, g3) = e(B, Y) failed.")
                return False
            print("✅ D verified using pairing check.")

        # [cite_start]3. Verify the Zero-Knowledge Proof part (*) [cite: 401]
        B1 = neg(B)
        
        # Re-compute Com1 and D1 from the s-values
        Com_inv_c = neg(multiply(Com, c))
        Com1_recomputed = add(add(multiply(g1, s1), multiply(h_T, s2)), Com_inv_c)
        
        D_inv_c = neg(multiply(D, c))
        D1_recomputed = add(add(multiply(B1, s1), multiply(g, s3)), D_inv_c)

        # Re-compute c' and verify it matches the original c from the proof
        hash_input_recomputed = (
            serialize_point(Com) + serialize_point(B) + serialize_point(D) +
            serialize_point(Com1_recomputed) + serialize_point(D1_recomputed)
        )
        c_recomputed = hash_to_int(hash_input_recomputed)
        
        if c_recomputed != c:
            print("❌ Verification failed: ZKP challenge hash check failed.")
            return False

        print("✅ ZKP challenge hash verified.")
        return True