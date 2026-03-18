import sys
import atheris
import msgpack
import msgpacker

class CorruptionError(RuntimeError):
    """Raised when the encoder produces invalid data without crashing."""
    pass

class LogicBugError(RuntimeError):
    """Raised when the decoder returns the wrong data type or value."""
    pass

class CompatibilityBugError(RuntimeError):
    """Raised when the decoder rejects perfectly valid standard bytes."""
    pass


def generate_fuzzed_object(fdp, max_depth=5):
    """Generates complex, nested Python objects using FDP."""
    if max_depth <= 0:
        return fdp.ConsumeInt(2)

    choice = fdp.ConsumeIntInRange(0, 5)

    match choice:
        case 0:
            return fdp.ConsumeInt(fdp.ConsumeIntInRange(1, 8))
        case 1:
            return fdp.ConsumeUnicodeNoSurrogates(fdp.ConsumeIntInRange(0, 256))
        case 2:
            return fdp.ConsumeBytes(fdp.ConsumeIntInRange(0, 256))
        case 3:
            return fdp.ConsumeBool() if fdp.ConsumeBool() else None
        case 4:
            return [generate_fuzzed_object(fdp, max_depth - 1) for _ in range(fdp.ConsumeIntInRange(0, 10))]
        case 5:
            return {
                fdp.ConsumeUnicodeNoSurrogates(10): generate_fuzzed_object(fdp, max_depth - 1)
                for _ in range(fdp.ConsumeIntInRange(0, 10))
            }
        case _:
            return None



def assert_decoder_resilience_to_garbage(data):
    """Phase 1: Asserts the decoder fails gracefully on invalid bytes."""
    try:
        dec = msgpacker.decoder(data)
        dec.decode()
    except (msgpacker.BadEncodingException, msgpacker.UnsupportedValueException):
        pass  # Expected graceful failure
    except Exception as e:
        raise RuntimeError(f"DECODER CRASH: {type(e).__name__} on bytes {data.hex()}: {e}") from e


def assert_encoder_output_is_spec_compliant(fdp):
    """Phase 2: Asserts your encoder produces standard MessagePack bytes."""
    val = generate_fuzzed_object(fdp)

    try:
        enc = msgpacker.encoder()
        enc.encode(val)
        test_bytes = enc.get_buf()

        ref_decoded = msgpack.unpackb(test_bytes, strict_map_key=False)
        if val != ref_decoded:
            raise CorruptionError(f"CORRUPTION: Encoded {repr(val)} but standard library read {repr(ref_decoded)}")

    except CorruptionError:
        raise
    except Exception as e:
        raise RuntimeError(f"ENCODER CRASH: {type(e).__name__} on {repr(val)}: {e}") from e


def assert_decoder_can_read_standard_bytes(fdp):
    """Phase 3: Asserts your decoder accurately reads standard MessagePack bytes."""
    val = generate_fuzzed_object(fdp)

    valid_bytes = msgpack.packb(val, use_bin_type=True)

    try:
        dec = msgpacker.decoder(valid_bytes)
        test_decoded = dec.decode()
        if val != test_decoded:
            raise LogicBugError(f"LOGIC BUG: Expected {repr(val)}, decoder returned {repr(test_decoded)}")

    except (msgpacker.BadEncodingException, msgpacker.UnsupportedValueException) as e:
        raise CompatibilityBugError(f"COMPATIBILITY BUG: Rejected valid bytes {valid_bytes.hex()} (value: {repr(val)}): {e}") from e
    except LogicBugError:
        raise
    except Exception as e:
        raise RuntimeError(f"DECODER CRASH ON VALID DATA: {type(e).__name__} on {repr(val)}: {e}") from e


def TestOneInput(data):
    """Routes the fuzzer into one of the three testing phases."""
    if not data:
        return

    fdp = atheris.FuzzedDataProvider(data)
    routing_byte = fdp.ConsumeIntInRange(0, 2)

    match routing_byte:
        case 0:
            assert_decoder_resilience_to_garbage(fdp.ConsumeBytes(sys.maxsize))
        case 1:
            assert_encoder_output_is_spec_compliant(fdp)
        case 2:
            assert_decoder_can_read_standard_bytes(fdp)


if __name__ == "__main__":
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()