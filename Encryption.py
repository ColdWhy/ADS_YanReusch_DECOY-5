import secrets
import os
from tqdm import tqdm
from Transposition import transpose
from KeyHandling import split_key, generate_stream
from Masking import mask
from AlphabetPool import alphabet, key_pool

# ===================================================================================================
#  LETTER BLOCKS
# ===================================================================================================

letter_blocks = []

print("Generating alphabet table...")
for char1 in tqdm(alphabet, desc="Progress", ncols=70):
    for char2 in alphabet:
        for char3 in alphabet:
            for char4 in alphabet:
                for char5 in alphabet:
                    letter_blocks.append(char1 + char2 + char3 + char4 + char5)

# ===================================================================================================
#  KEY AND TABLE
# ===================================================================================================

def generate_key():
    return ''.join(secrets.choice(key_pool) for _ in range(20))

def generate_key_r(length):
    return ''.join(secrets.choice(alphabet) for _ in range(length))

class FenwickTree:
    def __init__(self, size):
        self.size = size
        self.tree = [0] * (size + 1)

    def update(self, index, delta):
        index += 1
        while index <= self.size:
            self.tree[index] += delta
            index += index & -index

    def query(self, index):
        # sum of [0, index]
        index += 1
        result = 0
        while index > 0:
            result += self.tree[index]
            index -= index & -index
        return result

    def find_kth(self, k):
        # find smallest index with prefix sum >= k+1
        index = 0
        bit_mask = 1 << (self.size.bit_length())
        while bit_mask > 0:
            t = index + bit_mask
            if t <= self.size and self.tree[t] <= k:
                k -= self.tree[t]
                index = t
            bit_mask //= 2
        return index

def generate_cipher_table(table_key):
    table_key = list(table_key)
    num_key = [((key_pool.index(char) + 1) * 7) ** 3 for char in table_key]

    n = len(num_key)
    total = len(letter_blocks)
    ft = FenwickTree(total)
    for i in range(total):
        ft.update(i, 1)  # mark all elements as present

    cipher_table = []
    position = sum(num_key) % total

    print("Generating cipher table...")

    for index in tqdm(range(total), desc="Progress", ncols=70):
        i1 = index % n
        i2 = (index // n) % n
        i3 = (index // (n ** 2)) % n

        mirror_index = (position + num_key[i1] + num_key[i2] + num_key[i3]) % (total - index)
        actual_index = ft.find_kth(mirror_index)
        cipher_table.append(letter_blocks[actual_index])

        ft.update(actual_index, -1)  # remove this element
        position = mirror_index

    return cipher_table, dict(zip(letter_blocks, cipher_table))
# ===================================================================================================
#  PLAINTEXT PROCESSING
# ===================================================================================================

def arrange_plaintext(plaintext):
    plaintext = plaintext.upper()
    plaintext_list = []
    counter = 0
    for char in plaintext:
        if char in alphabet:
            plaintext_list.append(char)
            if counter == 3:
                plaintext_list.append(secrets.choice(alphabet))  # adds a decoy every 4 letters to form a tetragraph
                counter = 0
            else:
                counter += 1

    while len(plaintext_list) % 5 != 0:
        plaintext_list.append(secrets.choice(alphabet))

    arranged_plaintext = []
    block = []
    for char in plaintext_list:
        block.append(char)
        if len(block) == 5:
            arranged_plaintext.append(''.join(block))
            block = []
    return arranged_plaintext

def separate_plaintext(plaintext_list):
    while len(plaintext_list) % 5 != 0:
        plaintext_list.append(secrets.choice(alphabet))

    arranged_plaintext = []
    block = []
    for char in plaintext_list:
        block.append(char)
        if len(block) == 5:
            arranged_plaintext.append(''.join(block))
            block = []
    return arranged_plaintext

# ===================================================================================================
#  SUBSTITUTION
# ===================================================================================================

# generates random key, encrypts the text and inserts the key into the text.
# it's done to create more diffusion.
# and if the same key is used multiple times, it prevents patterns from emerging across different ciphertexts
def encrypt_r(master_key, cipher_table, arranged_plaintext):
    length = len(master_key) # random key is the same length as the master key
    sub_key_r = generate_key_r(length)
    sub_stream_r = generate_stream(sub_key_r)

    ciphertext_blocks = []

    # Precompute key_pool index lookups
    key_pool_map = {char: idx for idx, char in enumerate(key_pool)}
    num_key = [((key_pool_map[char] + 1) * 7) ** 3 for char in sub_stream_r]

    # Precompute cipher_table index lookups
    cipher_table_map = {val: idx for idx, val in enumerate(cipher_table)}

    # Summing num_key elements produces a key-dependent starting offset
    position = sum(num_key)

    index = 0
    len_key = len(num_key)
    len_table = len(cipher_table)

    for block in arranged_plaintext:
        i1 = index % len_key
        i2 = (index // len_key) % len_key
        i3 = (index // (len_key * len_key)) % len_key

        # O(1) lookup instead of O(n)
        block_num = cipher_table_map[block]

        new_block_num = (position + block_num + num_key[i1] + num_key[i2] + num_key[i3]) % len_table
        ciphertext_blocks.append(cipher_table[new_block_num])

        position = new_block_num
        index += 1

    # ================
    # inserting random key into ciphertext

    ciphertext_blocks = ''.join(ciphertext_blocks)

    ciphertext_blocks = sub_key_r + ciphertext_blocks

    ciphertext_blocks = separate_plaintext(list(ciphertext_blocks))
    return ciphertext_blocks

def encrypt(sub_key, cipher_table, arranged_plaintext):
    ciphertext_blocks = []

    # Precompute key_pool index lookups
    key_pool_map = {char: idx for idx, char in enumerate(key_pool)}
    num_key = [((key_pool_map[char] + 1) * 7) ** 3 for char in sub_key]

    # Precompute cipher_table index lookups
    cipher_table_map = {val: idx for idx, val in enumerate(cipher_table)}

    # Summing num_key elements produces a key-dependent starting offset
    position = sum(num_key)

    index = 0
    len_key = len(num_key)
    len_table = len(cipher_table)

    for block in arranged_plaintext:
        i1 = index % len_key
        i2 = (index // len_key) % len_key
        i3 = (index // (len_key * len_key)) % len_key

        # O(1) lookup instead of O(n)
        block_num = cipher_table_map[block]

        new_block_num = (position + block_num + num_key[i1] + num_key[i2] + num_key[i3]) % len_table
        ciphertext_blocks.append(cipher_table[new_block_num])

        position = new_block_num
        index += 1

    return ''.join(ciphertext_blocks)


# ===================================================================================================
#  RUNNING
# ===================================================================================================

# in case a random key is to be generated
flag_generate_key = True
# in case a cipher table is to be generated
flag_generate_table = True
cipher_table = None

if os.stat("storage.txt").st_size != 0:  # if storage is NOT empty
    print("Would you like to use the last cipher table stored? (Y/N)")
    ask = input("If so, make sure that you use the same key as the one used to create the table.\n").upper()

    if ask == "Y":
        flag_generate_key = False
        flag_generate_table = False
        with open("storage.txt", "r") as storage:
            cipher_table = storage.read().splitlines()

    else:
        ask = input("Would you like to generate a random key? (Y/N): ").upper()
        if ask == "Y":
            flag_generate_key = True
        else:
            flag_generate_key = False

else: # if storage IS empty
    ask = input("Would you like to generate a random key? (Y/N): ").upper()
    if ask == "Y":
        flag_generate_key = True
    else:
        flag_generate_key = False

if flag_generate_key == False:
    while True:
        master_key = input(f"Input key: ")
        if any(c not in key_pool for c in master_key):
            print(f"Key has invalid characters. Characters allowed: [0–9], [A–Z], [a–z], [!@#$%&*-=_+?,.;:<>]")
        else:
            break
else:
    master_key = generate_key()

sub_key, table_key, trans_key = split_key(master_key)

if flag_generate_table == True:
    cipher_table, cipher_dict = generate_cipher_table(table_key) # cipher_dict currently unused
    ask = input("Save new cipher table? Overwrites previous table. (Y/N): ").upper()
    if ask == "Y":
        with open("storage.txt", "w") as file:
            file.writelines(item + "\n" for item in cipher_table)

if not cipher_table:
    raise ValueError("No cipher table available. Either load one from storage or generate a new one.")

plaintext = "Beyond the northern mountains lies the timeless city"
arranged_plaintext = arrange_plaintext(plaintext)
ciphertext_r = encrypt_r(master_key, cipher_table, arranged_plaintext)
ciphertext = encrypt(sub_key, cipher_table, ciphertext_r)
ciphertext = transpose(ciphertext, trans_key)
ciphertext = mask(ciphertext)

print(f"\nKeys:\nMaster key: ({master_key})\n\nSubstitution key: {sub_key}\n\nTable key: {table_key}\n\nTransposition key: {trans_key}")
print(f"\nPlaintext: {plaintext}")
print(f"\nCiphertext: ({ciphertext})")

