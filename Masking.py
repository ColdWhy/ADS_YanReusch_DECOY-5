"""
DECOY-5 encrypts blocks of 5 characters, so all ciphertexts
end up being divisible by 5.
In order to hide that, this masking function adds up to
10 random characters at the end. It looks at the 5 first
characters of a ciphertext and if its index is even, it
adds a random character at the end.

This is not meant to increase the cipher's strength. It's merely
to prevent an attacker unfamiliar with DECOY-5 from immediately identifying
its nature.
"""

import secrets
from AlphabetPool import alphabet

def mask(text):
    output_text = text[:]
    for c in text[:10]:
        if alphabet.index(c) % 2 == 0:
            output_text += secrets.choice(alphabet)
    return output_text

def unmask(text):
    output_text = text[:]
    for c in text[:10]:
        if alphabet.index(c) % 2 == 0:
            output_text = output_text[:-1]
    return output_text
