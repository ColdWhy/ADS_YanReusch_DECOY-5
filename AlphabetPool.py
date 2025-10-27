alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ,.? ')
key_pool = alphabet + list('1234567890abcdefghijklmnopqrstuvwxyz!@#$%&*-=_+;:<>')
# MAKE SURE THE KEY_POOL CONTAINS ALL ALPHABET CHARACTERS!!!

def set_alphabet(new_alphabet: str):
    # Update the global alphabet and key_pool.
    global alphabet, key_pool
    if new_alphabet == alphabet:
        print("[AlphabetPool] New alphabet is identical to previous!")
    else:
        alphabet = list(new_alphabet)
        key_pool = alphabet + list('1234567890abcdefghijklmnopqrstuvwxyz!@#$%&*-=_+;:<>')

    print("[AlphabetPool] Alphabet and key_pool updated!")