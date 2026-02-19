from hashall import *
from hashbig import *

# return password, where toy_hash(password) = <HASH_OUTPUT_BY_GRADESCOPE>
import hashlib

def problem_2a():
    target = "a33a874eb313"
    dict_path = "/usr/share/dict/words"

    try:
        with open(dict_path, "r") as f:
            for line in f:
                word = line.strip().lower()

                if not word.isalpha():
                    continue

                attempt = word.encode()

                result_hash = hashlib.sha256(attempt).hexdigest()[:12]

                if result_hash == target:
                    print(f"--- SUCCESS ---")
                    print(f"Target:   {target}")
                    print(f"Found:    {result_hash}")
                    print(f"PASSWORD: {word}")
                    return word

        print("Password not found in the dictionary.")
    except FileNotFoundError:
        print(f"Error: Dictionary not found at {dict_path}. If you're on Windows, you may need to download a wordlist.")

# return password, where toy_hash(password) is in hashes.txt
def problem_2c():
    print("Loading 16 million hashes... (this might take 10-20 seconds)")
    targets = set()

    # We use a set for O(1) lookups.
    # This will use about 1-2 GB of RAM.
    try:
        with open("hashes.txt", "r") as f:
            for line in f:
                targets.add(line.strip())
    except FileNotFoundError:
        print("Error: hashes.txt not found.")
        return

    print(f"Loaded {len(targets)} hashes. Starting Brute Force...")

    # Brute Force Strategy
    # The file has exactly 2^24 lines.
    # It's extremely likely the inputs are just integers 0, 1, 2...
    # Even if they aren't, checking 16 million random numbers
    # is statistically guaranteed to find a collision.
    for i in range(20000000):  # Loop up to 20 million
        s = str(i)

        data = s.encode('ascii')

        h = hashlib.sha256(data).digest()[0:6].hex()

        if h in targets:
            print(f"\n🔥🔥🔥 FOUND A PREIMAGE! 🔥🔥🔥")
            print(f"Input: {s}")
            print(f"Hash:  {h}")
            return s

        if i % 500000 == 0:
            print(f"Checked {i} inputs...", end="\r")

# return probability of being in bin k
def problem_3a(B, N):
    prob = 1/N
    return prob

# return probability of both balls being in bin k
def problem_3b(B,N):
    prob = 1 / (N**2)
    return prob

# return number of ball pairs
def problem_3c(B):
    prob = (B * (B - 1)) // 2
    return prob

# return reasonable upper bound
def problem_3d(B,N):
    prob = (B * (B - 1)) / (2 * N)
    return prob
    
# return reasonable upper bound
def problem_3e(L,N):
    prob = (L * (L - 1)) / (2 * (2**N))
    return prob

# return h1,h2 where H(h1) == H(h2)
def problem_4b():
    x0 = b"start_value"

    h1 = H(x0)  # 1 step
    h2 = H(H(x0))  # 2 steps

    steps = 1
    while h1 != h2:
        h1 = H(h1)
        h2 = H(H(h2))
        steps += 1
        if steps % 1000000 == 0:
            print(f"Computed {steps // 1000000} million steps...", end="\r")
    print("Phase 1 complete: Cycle detected!")

    h1 = x0
    while H(h1) != H(h2):
        h1 = H(h1)
        h2 = H(h2)
    print("Phase 2 complete: Collision found! 💥")

    return h1, h2
