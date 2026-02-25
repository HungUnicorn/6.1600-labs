import time
import hashlib
from ecdsa import SigningKey, NIST256p

import hashlib
from datetime import datetime
from multiprocessing import Pool, cpu_count
from ecdsa import SigningKey, NIST256p

def problem_1a(date_string, vk):
    """
    Brute-forces the ECDSA secret key based on a known generation date.
    """
    dt = datetime.strptime(date_string, "%Y-%m-%d")

    start_ts = int(dt.timestamp())
    # A full 24-hour day
    end_ts = start_ts + 86400

    # Convert the target verifying key to raw bytes once to save time in the loop
    target_vk_bytes = vk.to_string()
    search_space = [(ts, target_vk_bytes) for ts in range(start_ts, end_ts)]

    with Pool(processes=cpu_count()) as pool:
        # imap_unordered is the fastest way to return the first successful match
        for result in pool.imap_unordered(check_timestamp, search_space, chunksize=500):
            if result is not None:
                pool.terminate()  # Kill all other processes immediately once found
                return SigningKey.from_secret_exponent(result, curve=NIST256p)

    raise ValueError("Secret key not found in the given date range.")

def problem_2b(sig1, sig2, Hm1, Hm2):
    recoverer = ECDSAKeyRecoverer(sig1, sig2, Hm1, Hm2)

    recovered_nonce = recoverer.recover_nonce()
    private_key = recoverer.recover_private_key(recovered_nonce)

    return private_key

# The mathematical boundary for the P-256 curve is a global constant
CURVE_ORDER = 6277101735386680763835789423176059013767194773182842284081

class ECDSAKeyRecoverer:
    """Encapsulates the data and logic needed to break an ECDSA key with a reused nonce."""

    def __init__(self, sig1, sig2, message1_hash, message2_hash):
        self.shared_nonce_point, self.signature1_proof = sig1
        _, self.signature2_proof = sig2

        self.message1_hash = message1_hash
        self.message2_hash = message2_hash

    def _modular_divide(self, numerator, denominator):
        inverse_denominator = pow(denominator, -1, CURVE_ORDER)
        return (numerator * inverse_denominator) % CURVE_ORDER

    def recover_nonce(self):
        """Step 1: Uses the instance state to isolate the secret nonce."""
        hash_difference = (self.message1_hash - self.message2_hash) % CURVE_ORDER
        proof_difference = (self.signature1_proof - self.signature2_proof) % CURVE_ORDER

        return self._modular_divide(hash_difference, proof_difference)

    def recover_private_key(self, recovered_nonce):
        """Step 2: Plugs the recovered nonce back in to find the private key."""
        key_numerator = (self.signature1_proof * recovered_nonce - self.message1_hash) % CURVE_ORDER

        return self._modular_divide(key_numerator, self.shared_nonce_point)

def check_timestamp(args):
    """
    Worker function to test a single timestamp.
    Runs on separate CPU cores to speed up the brute force.
    """
    ts, target_vk_bytes = args

    # Recreate the exact vulnerability from keygen.py
    b = b'%d' % ts
    h = hashlib.sha256(b).digest()
    secexp = int.from_bytes(h, "big")

    sk = SigningKey.from_secret_exponent(secexp, curve=NIST256p)

    # Compare raw bytes (much faster than converting to PEM every time)
    if sk.verifying_key.to_string() == target_vk_bytes:
        return secexp

    return None
