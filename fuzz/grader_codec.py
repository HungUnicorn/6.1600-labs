import sys
import atheris
import string
import codec

printable = string.printable[:94].encode('ascii')
alphanumeric = (string.ascii_letters + string.digits).encode('ascii')


class CodecBugError(Exception):
    pass


def assert_types_are_bytes(enc, dec):
    if not isinstance(enc, bytes) or not isinstance(dec, bytes):
        raise CodecBugError(f"TYPE BUG: Expected bytes, got enc:{type(enc)}, dec:{type(dec)}")


def assert_roundtrip_works(raw, dec):
    if raw != dec:
        raise CodecBugError(f"ROUNDTRIP BUG: Expected {repr(raw)}, decoded to {repr(dec)}")


def assert_output_is_printable(enc):
    for b in enc:
        if b not in printable:
            raise CodecBugError(f"PRINTABLE BUG: Encoded byte {hex(b)} is not in the printable set")


def assert_size_within_limits(raw, enc):
    if len(enc) > 3 * len(raw):
        raise CodecBugError(f"SIZE BUG: Encoded length {len(enc)} is > 3x original {len(raw)}")


def assert_alphanumeric_identity(alnum_bytes):
    enc = codec.encode(alnum_bytes)
    if enc != alnum_bytes:
        raise CodecBugError(f"ALPHANUMERIC BUG: {repr(alnum_bytes)} encoded to {repr(enc)}")


def assert_is_recoverable(raw, enc, fdp):
    if len(enc) < 2:
        return

    start = fdp.ConsumeIntInRange(0, len(enc) - 1)
    end = fdp.ConsumeIntInRange(start + 1, len(enc))

    chopped_enc = enc[start:end]
    chopped_dec = codec.decode(chopped_enc)

    if chopped_dec not in raw:
        raise CodecBugError(f"RECOVERABILITY BUG: Chopped dec {repr(chopped_dec)} not found in original {repr(raw)}")


def TestOneInput(data):
    fdp = atheris.FuzzedDataProvider(data)

    raw_bytes = fdp.ConsumeBytes(fdp.ConsumeIntInRange(1, 100))
    if not raw_bytes:
        return

    try:
        enc = codec.encode(raw_bytes)
        dec = codec.decode(enc)
    except Exception as e:
        raise CodecBugError(f"CRASH: {type(e).__name__} on input {repr(raw_bytes)}") from e

    assert_types_are_bytes(enc, dec)
    assert_roundtrip_works(raw_bytes, dec)
    assert_output_is_printable(enc)
    assert_size_within_limits(raw_bytes, enc)
    assert_is_recoverable(raw_bytes, enc, fdp)

    # Actively force an alphanumeric test
    alnum_str = fdp.ConsumeUnicodeNoSurrogates(20)
    alnum_bytes = "".join(c for c in alnum_str if c in string.ascii_letters + string.digits).encode('ascii')
    if alnum_bytes:
        assert_alphanumeric_identity(alnum_bytes)


if __name__ == "__main__":
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()