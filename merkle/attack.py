from common import Proof, traversal_path, H_kv
import store
import client

class AttackOne:
    def __init__(self, s):
        self._store = s

    def attack_fake_key(self):
        return b"hell"

    def lookup(self, key):
        fake_value = b"oworld"
        fake_proof = Proof(key, fake_value, [])
        return fake_proof

class AttackTwo:
    def __init__(self, s):
        self._store = s

        self.fake_store = store.Store()
        self.fake_client = client.Client(self.fake_store)
        self.fake_keys = []

        left_key = None
        right_key = None

        for i in range(1000):
            k = f"key_{i}".encode('utf-8')
            v = f"val_{i}".encode('utf-8')

            self.fake_keys.append(k)
            self.fake_client.insert(k, v)

            if left_key is None and traversal_path(k)[0] == 0:
                left_key = k
            elif right_key is None and traversal_path(k)[0] == 1:
                right_key = k

        proof_left = self.fake_store.lookup(left_key)
        proof_right = self.fake_store.lookup(right_key)

        right_hash = proof_left.siblings[0]
        left_hash = proof_right.siblings[0]

        self.attack_k = left_hash
        self.attack_v = right_hash

    def attack_fake_keys(self):
        return self.fake_keys

    def attack_key_value(self):
        return self.attack_k, self.attack_v

    def lookup(self, key):
        return self.fake_store.lookup(key)

class AttackThree:
    def __init__(self, s):
        self._store = s

        # We need four specific keys based on their first two traversal steps
        k_00 = None  # Goes Left, then Left
        k_01 = None  # Goes Left, then Right
        k_10 = None  # Goes Right, then Left
        k_11 = None  # Goes Right, then Right

        for i in range(1000):
            k = f"k{i}".encode('utf-8')
            path = traversal_path(k)

            if k_00 is None and path[0] == 0 and path[1] == 0:
                k_00 = k
            elif k_01 is None and path[0] == 0 and path[1] == 1:
                k_01 = k
            elif k_10 is None and path[0] == 1 and path[1] == 0:
                k_10 = k
            elif k_11 is None and path[0] == 1 and path[1] == 1:
                k_11 = k

        p_00 = self._store.lookup(k_00)
        p_01 = self._store.lookup(k_01)
        p_10 = self._store.lookup(k_10)
        p_11 = self._store.lookup(k_11)

        self.R_hash = p_00.siblings[0]
        self.L_hash = p_10.siblings[0]

        # Extract the grandchildren quarter-tree hashes (Index 1)
        # A path going Left (0) means its sibling is on the Right (1).
        self.LR_hash = p_00.siblings[1]
        self.LL_hash = p_01.siblings[1]

        self.RR_hash = p_10.siblings[1]
        self.RL_hash = p_11.siblings[1]

    def lookup(self, key):
        path = traversal_path(key)

        if path[0] == 0:
            # Key goes Left.
            # Force node_hash to become L_hash. Sibling is R_hash.
            return Proof(self.LL_hash, self.LR_hash, [self.R_hash])
        else:
            # Key goes Right.
            # Force node_hash to become R_hash. Sibling is L_hash.
            return Proof(self.RL_hash, self.RR_hash, [self.L_hash])
class AttackFour:
    def __init__(self, s):
        self._store = s

    def insert(self, key, val):
        return self._store.insert(key, val)

    def attack_fake_key(self):
        return b''

    def lookup(self, key):
        return self._store.lookup(key)
