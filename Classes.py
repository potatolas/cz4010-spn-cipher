from random import shuffle
from os import urandom
from utils import *

integers = [i for i in range(16)]

# Substitution Box Class
class SubBox:
    def __init__(self, type) -> None:
        shuffled = [0, 14, 7, 5, 13, 10, 11, 6, 2, 8, 12, 1, 15, 4, 3, 9]
        if(type == 1):
            shuffled = [0, 14, 7, 5, 13, 10, 11, 6, 2, 8, 12, 1, 15, 4, 3, 9]
        elif(type == 2):
            shuffled = [4, 13, 8, 0, 11, 10, 3, 15, 7, 14, 9, 1, 6, 5, 2, 12]
        elif(type == 3):
            shuffled = [5, 14, 10, 9, 15, 8, 3, 1, 2, 11, 0, 13, 7, 12, 6, 4]
        elif(type == 4):
            shuffled = [10, 8, 0, 5, 12, 4, 11, 3, 6, 1, 7, 13, 14, 9, 2, 15]
        else:
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

# Permutation Box Class
class PermBox:
    def __init__(self) -> None:
        # new position of bit no.
        # eg. [2, 3, 1] means [bit 2, bit 3, bit 1]
        self.position = [2, 15, 8, 13, 3, 12, 0, 9, 5, 4, 11, 7, 10, 14, 6, 1]

    # 16-bit length integer input
    def perm(self, bit_input) -> int:
        # input as list of 16 bits
        bit_array = [bit for bit in format(bit_input, '016b')]
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

class SPN:
    # minimum num_layers = 2
    def __init__(self, num_layers=4) -> None:
        self.num_layers = num_layers
        self.layers = {}

        # each layer has a substitution layer and a permutation layer
        for layer in range(1, num_layers):
            self.layers[f'layer {layer}'] = {}

            self.layers[f'layer {layer}']['sbox 1'] = SubBox(1)
            self.layers[f'layer {layer}']['sbox 2'] = SubBox(2)
            self.layers[f'layer {layer}']['sbox 3'] = SubBox(3)
            self.layers[f'layer {layer}']['sbox 4'] = SubBox(4)

            self.layers[f'layer {layer}']['pbox'] = PermBox()

        # final layer is a substitution layer
        self.layers[f'layer {num_layers}'] = {}

        self.layers[f'layer {num_layers}']['sbox 1'] = SubBox(1)
        self.layers[f'layer {num_layers}']['sbox 2'] = SubBox(2)
        self.layers[f'layer {num_layers}']['sbox 3'] = SubBox(3)
        self.layers[f'layer {num_layers}']['sbox 4'] = SubBox(4)

    # assume input_key is 16-bit, same key used for all rounds (layers)
    # inputs are bytes type?
    def encrypt(self, plaintext, input_key) -> bytes:
        keys = self.gen_keys(input_key)

        round_key = keys.pop(0)
        round_key_binary_array = convert_int_to_binary_array(round_key)
        plaintext_binary_array = convert_int_to_binary_array(plaintext)
        xor_result = convert_binary_array_to_int(xor_binary_arrays(round_key_binary_array, plaintext_binary_array))
        print(xor_result)

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
        return [input_key for round in range(self.num_layers)]


# key = urandom(2)
# # print(key)
# # print(key.hex())
# # print(int(key.hex(), 16))

# plaintext = urandom(2)
# print('plaintext (bytes):')
# print(plaintext)
# print('plaintext (hex):')
# print(plaintext.hex())
# print('plaintext (int):')
# print(int(plaintext.hex(), 16))

# # print(plaintext^key)
# print('='*25)
# print()

# asspeeann = SPN()
# ctext = asspeeann.encrypt(plaintext=plaintext, input_key=key)
# print(f'ciphertext:\t\t{ctext.hex()}')
# # print(ctext.hex())
# print(f'ciphertext int:\t\t{int(ctext.hex(), 16)}')
# # print(int(ctext.hex(), 16))
# print()
# ptext = asspeeann.decrypt(ciphertext=ctext, input_key=key)
# print(f'plaintext:\t\t{ptext.hex()}')
# # print(ptext.hex())
# print(f'plaintext int:\t\t{int(ptext.hex(), 16)}')
# print(int(ptext.hex(), 16))