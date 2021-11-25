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

def convert_int_to_binary_array(target):
    target_string = bin(target)[2:]
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

# print_bit(15)
# print_bit([0, 1, 7, 13])