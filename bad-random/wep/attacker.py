import zlib

class Attacker:
    def __init__(self, v):
        self.victim = v

    def attack_one(self, plaintext, ciphertext, attack_msg):
        # You may NOT use self.victim, since this is
        # a passive attack.
        iv, encrypted_payload = self._split_packet(ciphertext)

        original_payload = self._append_checksum(plaintext)
        keystream = self._xor_bytes(encrypted_payload, original_payload)

        malicious_payload = self._append_checksum(attack_msg)
        forged_encrypted_payload = self._xor_bytes(malicious_payload, keystream)

        return iv + forged_encrypted_payload

    def attack_two(self, ciphertext, attack_msg):
        # You may NOT use self.victim, since this is
        # a passive attack.

        iv, encrypted_payload = self._split_packet(ciphertext)

        crc_mask = self._calculate_crc_mask(attack_msg)
        full_modification_mask = attack_msg + crc_mask
        forged_payload = self._xor_bytes(encrypted_payload, full_modification_mask)

        return iv + forged_payload

    def attack_three(self, target):
        # You may NOT call self.victim.send_packet() 
        # or self.victim.receive_packet() here.
        #
        # You may call self.victim.check_packet(),
        # defined in grader.py.
        
        ### Your cleverness here
        return guess_of_secret_msg

    def _split_packet(self, ciphertext):
        """Separates the 3-byte unencrypted IV from the encrypted payload."""
        return ciphertext[:3], ciphertext[3:]

    def _append_checksum(self, message_bytes):
        """Calculates the CRC32 checksum and attaches it to the end of the message."""
        checksum = zlib.crc32(message_bytes).to_bytes(4, 'little')
        return message_bytes + checksum

    def _xor_bytes(self, bytes1, bytes2):
        """Applies a bitwise XOR to two byte strings. Used for both encrypting and decrypting."""
        return bytes(b1 ^ b2 for b1, b2 in zip(bytes1, bytes2))

    def _calculate_crc_mask(self, delta_message):
        """
        Calculates the exact CRC32 bit-flips needed by canceling out
        the standard padding (affine constants) using an all-zero string.
        """
        zero_string = bytes(len(delta_message))
        pure_difference = zlib.crc32(delta_message) ^ zlib.crc32(zero_string)

        return pure_difference.to_bytes(4, 'little')
