from random import shuffle
from os import urandom

integers = [i for i in range(16)]

# print bits as string/list with formatting, integer input
def print_bits(bits, length=4) -> str:
    return format(bits, f'0{length}b')

def print_bits_list(bits_list, length=4) -> str:
    result = ""
    for bits in bits_list:
        result += ' ' + format(bits, f'0{length}b')
    return result.strip()

def print_bit(bits, length=4) -> None:
    if type(bits) != int:
        print(print_bits_list(list(bits), length))
    else:
        print(print_bits(bits, length))

# print_bit(15)
# print_bit([0, 1, 7, 13])


# Substitution Box Class
class SubBox:
    def __init__(self) -> None:
        shuffled = [integer for integer in integers]
        shuffle(shuffled)

        # mapping contains original:substitute (int:int)
        self.mapping = {integers[i]:shuffled[i] for i in range(len(integers))}

    # integer input
    def sub(self, input_block) -> int:
        return self.mapping[input_block]

    # integer input
    def unsub(self, input_block) -> int:
        return list(self.mapping.keys())[list(self.mapping.values()).index(input_block)]

# sbox = SubBox()

# print_bit(sbox.mapping.values())
# print(sbox.mapping.values())

# var = 0b0
# result = sbox.sub(var)
# print_bit(result)
# print_bit(sbox.unsub(result))
# print()
# print_bit(sbox.mapping.keys())
# print_bit(sbox.mapping.values())

class PermBox:
    def __init__(self) -> None:
        # new position of bit no.
        # eg. [2, 3, 1] means [bit 2, bit 3, bit 1]
        self.position = [i for i in range(16)]
        shuffle(self.position)

    # 16-bit length integer input
    def perm(self, bit_input) -> int:
        # input as list of 16 bits
        bit_array = [bit for bit in format(bit_input, '016b')]
        # print(bit_input) # debug
        # print(len(bit_array)) # debug
        # print(len(self.position)) # debug
        # swap positions of bits
        result = [bit_array[self.position[i]] for i in range(len(bit_array))]
            
        # output as str of 16 bits
        bit_output = ""
        for bit in result:
            bit_output += bit

        return int(bit_output, 2)

    # 16-bit length integer input
    def unperm(self, bit_input) -> int:
        # input as list of 16 bits
        bit_array = [bit for bit in format(bit_input, '016b')]

        # reverse position swapping
        indexes = [self.position.index(bit_index) for bit_index in range(len(bit_array))]
        result = [bit_array[index] for index in indexes]

        # output as str of 16 bits
        bit_output = ""
        for bit in result:
            bit_output += bit

        return int(bit_output, 2)

# pbox = PermBox()

# print(f'positions: {pbox.position}\n')

# intput = 0b1001101011010111 # 39639
# print(f'{intput}')
# print_bit(intput, 16)
# print()

# permuted = pbox.perm(intput)
# print(f'{permuted}')
# print_bit(permuted, 16)
# print()

# unpermuted = pbox.unperm(permuted) # 39639
# print(f'{unpermuted}')
# print_bit(unpermuted, 16)

class SPN:
    # minimum num_layers = 2
    def __init__(self, num_layers=3) -> None:
        self.num_layers = num_layers
        self.layers = {}

        # each layer has a substitution layer and a permutation layer
        for layer in range(1, num_layers):
            self.layers[f'layer {layer}'] = {}

            self.layers[f'layer {layer}']['sbox 1'] = SubBox()
            self.layers[f'layer {layer}']['sbox 2'] = SubBox()
            self.layers[f'layer {layer}']['sbox 3'] = SubBox()
            self.layers[f'layer {layer}']['sbox 4'] = SubBox()

            self.layers[f'layer {layer}']['pbox'] = PermBox()

        # final layer is a substitution layer
        self.layers[f'layer {num_layers}'] = {}

        self.layers[f'layer {num_layers}']['sbox 1'] = SubBox()
        self.layers[f'layer {num_layers}']['sbox 2'] = SubBox()
        self.layers[f'layer {num_layers}']['sbox 3'] = SubBox()
        self.layers[f'layer {num_layers}']['sbox 4'] = SubBox()

    # assume input_key is 16-bit, same key used for all rounds (layers)
    # inputs are bytes type?
    def encrypt(self, plaintext, input_key) -> bytes:
        keys = self.gen_keys(input_key)

        round_key = keys.pop(0)
        xor_result = bytes(a ^ b for a, b in zip(round_key, plaintext))

        # num_layers - 1
        for round in range(1, self.num_layers):
            # print(format(int(xor_result.hex(), 16), '016b'))
            # substitution layer
            sbox_1_result = self.layers[f'layer {round}']['sbox 1'].sub(int(xor_result.hex()[0], 16))
            sbox_2_result = self.layers[f'layer {round}']['sbox 2'].sub(int(xor_result.hex()[1], 16))
            sbox_3_result = self.layers[f'layer {round}']['sbox 3'].sub(int(xor_result.hex()[2], 16))
            sbox_4_result = self.layers[f'layer {round}']['sbox 4'].sub(int(xor_result.hex()[3], 16))
            sbox_result = format(sbox_1_result, '04b') + format(sbox_2_result, '04b') + format(sbox_3_result, '04b') + format(sbox_4_result, '04b')
            # print(sbox_result)
            # print(int(sbox_result, 2))
            # permutation layer
            pbox_result = self.layers[f'layer {round}']['pbox'].perm(int(sbox_result, 2))

            # xor with round key
            round_key = keys.pop(0)
            xor_result = bytes(a ^ b for a, b in zip(round_key, pbox_result.to_bytes(2, 'big')))

        # final substitution layer
        sbox_1_result = self.layers[f'layer {self.num_layers}']['sbox 1'].sub(int(xor_result.hex()[0], 16))
        sbox_2_result = self.layers[f'layer {self.num_layers}']['sbox 2'].sub(int(xor_result.hex()[1], 16))
        sbox_3_result = self.layers[f'layer {self.num_layers}']['sbox 3'].sub(int(xor_result.hex()[2], 16))
        sbox_4_result = self.layers[f'layer {self.num_layers}']['sbox 4'].sub(int(xor_result.hex()[3], 16))
        sbox_result = format(sbox_1_result, '04b') + format(sbox_2_result, '04b') + format(sbox_3_result, '04b') + format(sbox_4_result, '04b')

        # final xor with round key
        round_key = keys.pop(0)
        ciphertext = bytes(a ^ b for a, b in zip(round_key, int(sbox_result, 2).to_bytes(2, 'big')))
        
        return ciphertext

    # inverse of encryption
    def decrypt(self, ciphertext, input_key) -> bytes:
        keys = self.gen_keys(input_key)

        # final xor with round key
        round_key = keys.pop()
        xor_result = bytes(a ^ b for a, b in zip(round_key, ciphertext))

        # final substitution layer
        sbox_1_result = self.layers[f'layer {self.num_layers}']['sbox 1'].unsub(int(xor_result.hex()[0], 16))
        sbox_2_result = self.layers[f'layer {self.num_layers}']['sbox 2'].unsub(int(xor_result.hex()[1], 16))
        sbox_3_result = self.layers[f'layer {self.num_layers}']['sbox 3'].unsub(int(xor_result.hex()[2], 16))
        sbox_4_result = self.layers[f'layer {self.num_layers}']['sbox 4'].unsub(int(xor_result.hex()[3], 16))
        sbox_result = format(sbox_1_result, '04b') + format(sbox_2_result, '04b') + format(sbox_3_result, '04b') + format(sbox_4_result, '04b')

        # num_layers - 1
        for round in range(self.num_layers - 1, 0, -1):
            # xor with round key
            round_key = keys.pop()
            xor_result = bytes(a ^ b for a, b in zip(round_key, int(sbox_result, 2).to_bytes(2, 'big')))

            # permutation layer
            pbox_result = self.layers[f'layer {round}']['pbox'].unperm(int(xor_result.hex(), 16))
            
            # substitution layer
            sbox_1_result = self.layers[f'layer {round}']['sbox 1'].unsub(int(format(pbox_result, '016b')[0:4], 2))
            sbox_2_result = self.layers[f'layer {round}']['sbox 2'].unsub(int(format(pbox_result, '016b')[4:8], 2))
            sbox_3_result = self.layers[f'layer {round}']['sbox 3'].unsub(int(format(pbox_result, '016b')[8:12], 2))
            sbox_4_result = self.layers[f'layer {round}']['sbox 4'].unsub(int(format(pbox_result, '016b')[12:], 2))
            sbox_result = format(sbox_1_result, '04b') + format(sbox_2_result, '04b') + format(sbox_3_result, '04b') + format(sbox_4_result, '04b')

        round_key = keys.pop()
        plaintext = bytes(a ^ b for a, b in zip(round_key, int(sbox_result, 2).to_bytes(2, 'big')))

        return plaintext

    # current implementation returns the same keys multiple times
    def gen_keys(self, input_key) -> list:
        return [input_key for round in range(self.num_layers + 1)]


key = urandom(2)
# print(key)
# print(key.hex())
# print(int(key.hex(), 16))

plaintext = urandom(2)
print('plaintext (bytes):')
print(plaintext)
print('plaintext (hex):')
print(plaintext.hex())
print('plaintext (int):')
print(int(plaintext.hex(), 16))

# print(plaintext^key)
print('='*25)
print()

asspeeann = SPN()
ctext = asspeeann.encrypt(plaintext=plaintext, input_key=key)
print(f'ciphertext:\t\t{ctext.hex()}')
# print(ctext.hex())
print(f'ciphertext int:\t\t{int(ctext.hex(), 16)}')
# print(int(ctext.hex(), 16))
print()
ptext = asspeeann.decrypt(ciphertext=ctext, input_key=key)
print(f'plaintext:\t\t{ptext.hex()}')
# print(ptext.hex())
print(f'plaintext int:\t\t{int(ptext.hex(), 16)}')
# print(int(ptext.hex(), 16))