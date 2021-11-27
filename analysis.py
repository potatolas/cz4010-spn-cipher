from classes import *
from utils import *
from data import known_ciphertext, known_plaintext

def test_partial_key_eqn(u_array, p_array):
    keyspace = {}
    sbox = SubBox()
    for i in range(256):
        keyspace[i] = 0

    for key in keyspace.keys():
        for index, ciphertext in enumerate(known_ciphertext):
            key_binary_array = convert_int_to_binary_array(key, 8)
            # pad key to 16 bits
            key_binary_array.extend([0 for i in range(16 - len(key_binary_array))])
            ciphertext_binary_array = convert_int_to_binary_array(ciphertext)

            # reverse xor
            reverse_xor_result = convert_binary_array_to_int(xor_binary_arrays(key_binary_array, ciphertext_binary_array))

            partial_ciphertext_array = split_bits_to_4_bit_int(reverse_xor_result)[:2]

            # reverse sub
            reverse_sub_result = [sbox.unsub(partial_ciphertext_array[0]), sbox.unsub(partial_ciphertext_array[1])]

            reverse_sub_array = convert_int_to_binary_array(reverse_sub_result[0], 4)
            reverse_sub_array.extend(convert_int_to_binary_array(reverse_sub_result[1], 4))
            
            # xor result
            # result = reverse_sub_array[1]
            # result = result ^ reverse_sub_array[4]
            # result = result ^ reverse_sub_array[5]
            # result = result ^ reverse_sub_array[6]
            
            result = 0

            for i in u_array:
                result = result ^ reverse_sub_array[i]

            plaintext_binary_array = convert_int_to_binary_array(known_plaintext[index])

            # result = result ^ plaintext_binary_array[1]
            # result = result ^ plaintext_binary_array[2]
            # result = result ^ plaintext_binary_array[3]

            for i in p_array:
                result = result ^ plaintext_binary_array[i]

            if result == 0:
                keyspace[key] += 1
    
    return keyspace

def generate_linear_approx_table(linear_approx_table, sbox):
    # initialise all to -8
    for input_mask in range(16):
        for output_mask in range(16):
            linear_approx_table[(input_mask, output_mask)] = -8

    # generate combinations of input bits and output bits
    for input_mask in range(16):
        for output_mask in range(16):
            input_mask_array = convert_int_to_binary_array(input_mask, 4)
            output_mask_array = convert_int_to_binary_array(output_mask, 4)

            for sbox_input in range(16):
                input_array = convert_int_to_binary_array(sbox_input, 4)
                sbox_output = sbox.sub(sbox_input)
                output_array = convert_int_to_binary_array(sbox_output, 4)

                LHS_array = []
                RHS_array = []

                for i in range(4):
                    if input_mask_array[i] == 1:
                        LHS_array.append(input_array[i])
                    if output_mask_array[i] == 1:
                        RHS_array.append(output_array[i])

                LHS_result = 0
                RHS_result = 0
                
                for bit in LHS_array:
                    LHS_result = LHS_result ^ bit

                for bit in RHS_array:
                    RHS_result = RHS_result ^ bit
                
                if LHS_result == RHS_result:
                    linear_approx_table[(input_mask, output_mask)] += 1
    
    return linear_approx_table