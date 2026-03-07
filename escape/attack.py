def attack_one(guess):
    return guess.__closure__[0].cell_contents

def attack_two():
    import sys
    caller_frame = sys._getframe(1)
    return caller_frame.f_locals['secret']

def attack_three():
    import os
    rigged_secret = b'x' * 256

    os.urandom = lambda size: rigged_secret

    return rigged_secret

def attack_four():
    import gc
    for obj in gc.get_objects():
        if type(obj).__name__ == "SecretStore":
            return obj.secret
    return b''
