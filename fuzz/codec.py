import string

printable = string.printable[:94].encode('ascii')
alphanumeric = (string.ascii_letters + string.digits).encode('ascii')

# Requirements:
#
# - Your codec must encode bytes into bytes, and decode back into bytes.
# - Your codec must encode arbitrary bytes.  It must be possible to
#   encode any byte sequence, and decode it correctly.
# - The encoding must be printable (every encoding byte must be in the
#   `printable` bytes object.  Your encodings cannot contain non-printable
#   bytes.
# - Alphanumeric inputs (where every character is in string.ascii_letters
#   or string.digits) must be encoded one-to-one: the encoding must be the
#   same as the input.
# - The encoding should be at most 3x the size of the input, in the worst case.
# - The encoding must be recoverable.  This means that, if you take an encoding
#   and chop off some parts of it (at the beginning or at the end), then decoding
#   that chopped part should produce the corresponding part of the original string,
#   modulo things that might have gotten cut off at each end.

import string

ALPHANUMERIC = frozenset((string.ascii_letters + string.digits).encode('ascii'))
ESCAPE_CHAR = ord('=')
PUNCT_ALPHABET = b"!#$%&()*+,-./:;?"


def encode(input_bytes: bytes) -> bytes:
    out = bytearray()
    for byte in input_bytes:
        if _is_alphanumeric(byte):
            out.append(byte)
        else:
            out.extend(_encode_escaped_byte(byte))
    return bytes(out)


def decode(encoded_bytes: bytes) -> bytes:
    out = bytearray()
    i = 0
    length = len(encoded_bytes)

    while i < length:
        current_byte = encoded_bytes[i]

        if current_byte == ESCAPE_CHAR and _has_valid_escape_sequence(encoded_bytes, i):
            out.append(_decode_escaped_byte(encoded_bytes[i + 1], encoded_bytes[i + 2]))
            i += 3
        elif _is_alphanumeric(current_byte):
            out.append(current_byte)
            i += 1
        else:
            # Safely skip chopped escape characters or orphaned punctuation
            i += 1

    return bytes(out)

def encode_and_decode(i):
    enc = encode(i)
    dec = decode(enc)
    print(i, "->", enc, "->", dec)

def _has_valid_escape_sequence(buf: bytes, index: int) -> bool:
    if index + 2 >= len(buf):
        return False
    return buf[index + 1] in PUNCT_ALPHABET and buf[index + 2] in PUNCT_ALPHABET


def _is_alphanumeric(byte: int) -> bool:
    return byte in ALPHANUMERIC


def _encode_escaped_byte(byte: int) -> bytes:
    high_nibble = byte // 16
    low_nibble = byte % 16
    return bytes([ESCAPE_CHAR, PUNCT_ALPHABET[high_nibble], PUNCT_ALPHABET[low_nibble]])


def _decode_escaped_byte(char1: int, char2: int) -> int:
    high_val = PUNCT_ALPHABET.index(char1)
    low_val = PUNCT_ALPHABET.index(char2)
    return (high_val * 16) + low_val

encode_and_decode(b"hello world")
encode_and_decode(b"\x00\x01\x02\x03")
