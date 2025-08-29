from AlphabetPool import key_pool

def transpose(plaintext, trans_key):
    trans_key = list(trans_key)

    key_num = []
    for c in trans_key:  # coverts characters in the key to numbers according to the key pool
        key_num.append(key_pool.index(c) + 1)  # +1 so there's no zeros

    # cycles through the indexes of 3 elements from the key in a "clock" fashion
    index = 0

    coordinates = []
    for _ in plaintext:

        i1 = index % len(key_num)
        i2 = (index // len(key_num)) % len(key_num)
        i3 = (index // (len(key_num) ** 2)) % len(key_num)

        increase = 0
        while True:
            coord = (key_num[i1] * key_num[i2] * key_num[i3]) + increase
            if coord in coordinates:
                increase += 1 # all numbers must be different, so it keeps adding 1 until it lands on a unique one
            else:
                break

        coordinates.append(coord)
        index += 1  # moves the index clock

    # Map coordinates to characters
    paired = list(zip(coordinates, plaintext))

    # Sort by coordinate
    paired.sort(key=lambda x: x[0])

    # Extract characters in sorted order
    ciphertext = ''.join(char for _, char in paired)

    # print(paired)

    # print("Ciphertext:", ciphertext)

    return ciphertext


def unscramble(ciphertext, trans_key):
    trans_key = list(trans_key)

    key_num = []
    for c in trans_key:
        key_num.append(key_pool.index(c) + 1)

    index = 0
    coordinates = []
    for _ in range(len(ciphertext)):
        i1 = index % len(key_num)
        i2 = (index // len(key_num)) % len(key_num)
        i3 = (index // (len(key_num) ** 2)) % len(key_num)

        increase = 0
        while True:
            coord = (key_num[i1] * key_num[i2] * key_num[i3]) + increase
            if coord in coordinates:
                increase += 1
            else:
                break

        coordinates.append(coord)
        index += 1

    # Sorted version of coordinates tells us how the characters were shuffled
    sorted_coords = sorted(coordinates)

    # Map sorted_coords[i] -> original_coords[i] (inverse map)
    plaintext = [''] * len(ciphertext)
    for i, coord in enumerate(coordinates):
        sorted_index = sorted_coords.index(coord)
        plaintext[i] = ciphertext[sorted_index]

    return ''.join(plaintext)

# ===========================