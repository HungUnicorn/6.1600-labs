import bad_server
import api
import secrets
from typing import Optional
import time

class Client:
    HEX_CHARS = "0123456789abcdef"
    SAMPLES = 30
    PADDING_CHAR = "0"
    TRIM_PERCENT = 0.1  # Trim the top % and bottom %

    def __init__(self, remote: bad_server.BadServer):
        self._remote = remote

    def steal_password(self, l: int) -> Optional[str]:
        password = ""
        total_chars = self._bytes_to_hex_length(l)

        for _ in range(total_chars):
            best_char = max(
                self.HEX_CHARS,
                key=lambda c: self._get_timing(password, c, total_chars)
            )
            password += best_char

        if self._remote.verify_password(api.VerifyRequest(password)).ret:
            return password
        return None

    def _bytes_to_hex_length(self, num_bytes: int) -> int:
        return num_bytes * 2

    def _get_timing(self, prefix: str, char: str, total_chars: int) -> float:
        """Measures the execution time for a specific character guess using a Trimmed Mean."""
        guess = (prefix + char).ljust(total_chars, self.PADDING_CHAR)
        req = api.VerifyRequest(guess)

        # Warm-up request to prime the caches
        self._remote.verify_password(req)

        times = []
        for _ in range(self.SAMPLES):
            start = time.perf_counter()
            self._remote.verify_password(req)
            times.append(time.perf_counter() - start)

        times.sort()
        k = int(len(times) * self.TRIM_PERCENT)
        reliable_samples = times[k: len(times) - k]

        return sum(reliable_samples) / len(reliable_samples)

if __name__ == "__main__":
    passwd = '37a4e5bf847630173da7e6d19991bb8d'
    nbytes = len(passwd) // 2
    server = bad_server.BadServer(passwd)
    alice = Client(server)
    print(alice.steal_password(nbytes))
