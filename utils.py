# utils.py
import os
import hashlib
from py_ecc.bn128 import curve_order, FQ

# Use the curve order as the prime field modulus
p = curve_order

def int_to_bytes(n):
    """Converts an integer to a 32-byte array."""
    return n.to_bytes(32, 'big')

def sha256(data):
    """Computes SHA256 hash of the given data."""
    return hashlib.sha256(data).digest()

def hash_to_int(data):
    """Hashes data and returns it as an integer modulo the curve order."""
    return int.from_bytes(sha256(data), 'big') % p

def serialize_point(point):
    """Serializes an elliptic curve point to bytes for hashing."""
    if point is None: # For the identity element
        return b'\x00' * 64
    return int_to_bytes(point[0].n) + int_to_bytes(point[1].n)
    
def get_random_scalar():
    """Generates a random scalar in Z_p^*."""
    # Ensure it's not zero
    while True:
        s = int.from_bytes(os.urandom(32), 'big') % p
        if s != 0:
            return s