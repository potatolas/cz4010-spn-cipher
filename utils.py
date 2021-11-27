import pandas as pd

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
    # if(length == 16):
    #     target_string = format(target, '016b')
    # if(length == 4):
    #     target_string = format(target, '04b')
    target_string = format(target, f'0{length}b')

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

def split_bits_to_4_bit_int(target, length=16):
    target_string = format(target, f'0{length}b')
    # result_string_array = [target_string[0:4], target_string[4:8], target_string[8:12], target_string[12:16]]
    result_string_array = [target_string[i*4:i*4+4] for i in range(length//4)]
    result_array = []
    for string in result_string_array:
        result_array.append(int(string, base=2))
    return result_array

def visualise_linear_approx_table(linear_approx_table):
    columns = []
    table = {}

    for i in range(16):
        columns.append([])

    for key, value in linear_approx_table.items():
        columns[key[1]].append(value)

    for i in range(16):
        table[i] = columns[i]

    linear_approx_table_df = pd.DataFrame(table)
    return linear_approx_table_df

def visualise_top_25_subkeys(linear_attack_bias_df):
    return linear_attack_bias_df.style.hide_index()