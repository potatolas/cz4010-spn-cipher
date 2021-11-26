import math

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

def convert_int_to_binary_array(target, length=16):
    if(length == 16):
        target_string = format(target, '016b')
    if(length == 4):
        target_string = format(target, '04b')

    target_string_list = list(target_string)
    target_int_list = []
    for char in target_string_list:
        target_int_list.append(int(char))

    return target_int_list

def xor_binary_arrays(array1, array2):
    result_array = []
    for i in range(len(array1)):
        result_array.append(array1[i] ^ array2[i])
    return result_array

def convert_binary_array_to_int(target):
    target_string = ""
    for digit in target:
        target_string += str(digit)
    
    target_int = int(target_string, base=2)
    return target_int

def split_16_bits_to_4_bit_int(target):
    target_string = format(target, '016b')
    result_string_array = [target_string[0:4], target_string[4:8], target_string[8:12], target_string[12:16]]
    result_array = []
    for string in result_string_array:
        result_array.append(int(string, base=2))
    return result_array

# def split_plaintext_into_array(plaintext):
#     ascii_plaintext = "" 
#     for char in list(plaintext):
#         ascii_plaintext += bin(ord(char))[2:]

#     string_array = []
#     print(ascii_plaintext)

#     num_of_zeros = 16 - (len(ascii_plaintext) % 16)

#     ascii_plaintext = num_of_zeros*'0' + ascii_plaintext

#     print(ascii_plaintext)

#     slices = math.ceil(len(ascii_plaintext)/16)
#     start_index = 0
#     end_index = 16
#     while(slices > 0):
#         string_array.append(ascii_plaintext[start_index:end_index])
#         start_index += 16
#         end_index += 16
#         if(end_index > len(ascii_plaintext) - 1):
#             end_index = len(ascii_plaintext)
#         slices -= 1

#     print(string_array)

#     int_array = []
#     for string in string_array:
#         int_array.append(int(string, base=2))

#     return int_array

# print_bit(15)
# print_bit([0, 1, 7, 13])