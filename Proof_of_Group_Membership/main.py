# main.py
import random
from cryptosystem import SystemSetup
from prover import Prover
from verifier import Verifier

def run_test_case(case_num, setup, public_set_phi, signatures_sigma):
    """Runs a single, complete test case for a random secret."""
    print(f"\n--- TEST CASE #{case_num} ---")
    
    # 1. Prover selects a random secret k from the set
    secret_k = random.choice(list(public_set_phi))
    signature_for_k = signatures_sigma[secret_k]
    
    print(f"Prover's secret k = {secret_k}. Generating proof...")
    prover = Prover(secret_k, signature_for_k, setup.params)
    proof = prover.generate_proof()
    print("✅ Proof generated.")
    
    # 2. Verifier checks the proof
    # Case 1: Verifier has the authority's private key 'y'
    print("\n[Verifier Mode: With Private Key (Case 1)]")
    verifier_with_key = Verifier(setup.params, authority_private_key_y=setup.y)
    is_valid_case1 = verifier_with_key.verify_proof(proof)
    print(f"Verification Result (Case 1): {'VALID' if is_valid_case1 else 'INVALID'}")
    assert is_valid_case1

    # Case 2: Verifier does NOT have the private key 'y'
    print("\n[Verifier Mode: Without Private Key (Case 2)]")
    verifier_without_key = Verifier(setup.params)
    is_valid_case2 = verifier_without_key.verify_proof(proof)
    print(f"Verification Result (Case 2): {'VALID' if is_valid_case2 else 'INVALID'}")
    assert is_valid_case2

    # 3. Test with a tampered proof to ensure it fails
    print("\n[Testing with a tampered proof]")
    tampered_proof = proof.copy()
    tampered_proof["s1"] = (tampered_proof["s1"] + 1) % setup.params['p']
    is_valid_tampered = verifier_without_key.verify_proof(tampered_proof)
    print(f"Verification Result (Tampered Proof): {'VALID' if is_valid_tampered else 'INVALID'}")
    assert not is_valid_tampered
    print(f"--- END OF TEST CASE #{case_num} ---")


if __name__ == "__main__":
    # System Setup
    print("Setting up cryptographic system...")
    setup = SystemSetup()
    
    # Define the public set Φ and generate signatures Σ for it
    public_set_phi = set(range(1, 21)) # A set of 20 valid tickets
    signatures_sigma = setup.generate_signatures_for_set(public_set_phi)
    print(f"System setup complete. Public set Φ has {len(signatures_sigma)} elements.")
    
    # Run 5 random test cases
    for i in range(1, 6):
        run_test_case(i, setup, public_set_phi, signatures_sigma)