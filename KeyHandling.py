import math
from Transposition import transpose
from AlphabetPool import key_pool

def mangle_key(key):
    original_key = key[:]

    increase = 1
    key = ""
    for c in original_key:
        new_c_index = (key_pool.index(c) + increase) % len(key_pool)
        key += key_pool[new_c_index]
        increase += increase

    key = transpose(key, original_key[::-1]) # uses the key in reverse to transpose
    # this process is done to prevent any linguist patterns in the key from influencing the ciphertext
    # additionally, if an attacker somehow manages to figure out the sub_key and trans_key, it'll be harder to guess the table_key

    return key

def generate_stream(key):
    key = list(key)
    stream_key = []

    # Precompute key_pool index lookups
    key_pool_map = {char: idx for idx, char in enumerate(key_pool)}
    num_key = [key_pool_map[char] ** 2 for char in key]

    alt_num_key = []
    seen_counts = {}

    for n in num_key:
        count = seen_counts.get(n, 0)
        if count < 1:  # allow up to 2 repeats, adjust as needed
            alt_num_key.append(n)
            seen_counts[n] = count + 1
        else:
            # find next available unique number
            while n in seen_counts:
                n += 1
            alt_num_key.append(n)
            seen_counts[n] = 1

    print(alt_num_key)
    num_key = alt_num_key[:]

    index = 0
    position = 0
    increase = 1

    for num in num_key:
        position += num

    keyspace = len(num_key) * len(num_key) * len(num_key)
    for _ in range(keyspace):
        i1 = index % len(num_key)
        i2 = (index // len(num_key)) % len(num_key)
        i3 = (index // (len(num_key) ** 2)) % len(num_key)

        new_i = (num_key[i1] + num_key[i2] + num_key[i3] + position + increase) % len(key_pool)
        stream_key.append(key_pool[new_i])

        index += 1
        if (new_i % 2) + increase == 0:
            increase += 1
        else:
            increase += 101

    stream_key = ''.join(stream_key)
    stream_key = transpose(stream_key, stream_key[::-1])
    return stream_key

def split_key(master_key):
    master_key = mangle_key(master_key)
    master_key = generate_stream(master_key)

    table_key = ""
    subtrans_key = ""
    sub_key = ""
    trans_key = ""

    pendulum = True

    for c in master_key:
        if pendulum == True:
            table_key += c
        else:
            subtrans_key += c

        pendulum = not pendulum

    pendulum = True

    for c in subtrans_key:
        if pendulum == True:
            sub_key += c
        else:
            trans_key += c

        pendulum = not pendulum


    '''
    old splitting logic
    
    cutoff = (len(master_key) + 1) // 2  # ensures first half is bigger if odd
    table_key, subtrans_keys = master_key[:cutoff], master_key[cutoff:]

    cutoff = (len(subtrans_keys) + 1) // 2
    sub_key, trans_key = subtrans_keys[:cutoff], subtrans_keys[cutoff:]
    '''

    return sub_key, table_key, trans_key
