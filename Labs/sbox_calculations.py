import itertools
import random
from sympy.logic.boolalg import ANFform
from sympy import symbols


def read_sbox(path):
    f = open(path, mode='rb')
    s_box = f.read()
    f.close()
    return s_box


def average(list_to_calculate):
    return sum(list_to_calculate) / len(list_to_calculate)


def extract_function_from_row_notation(in_row_notation_dict, column, amount_of_arguments):
    result = []
    for rowNumber in range(2 ** amount_of_arguments):
        result.append(in_row_notation_dict[rowNumber][column])
    return result


def get_nth_bit(int_num, n):
    return (int_num >> n) & 1


def extract_functions_from_sbox(sbox, amount_of_arguments):
    result = []
    for i in range(amount_of_arguments):
        result.append([])

    skip = False
    for number in sbox:
        if not skip:
            for nthBit in range(amount_of_arguments):
                result[nthBit].append(get_nth_bit(number, nthBit))
        skip = not skip

    return result


def combinations_generator(num_list):
    result = []
    for number in num_list:
        result += list(itertools.combinations(num_list, number + 1))

    return result


def linear_functions_generator(amount_of_arguments):
    result = {}
    num_list = []
    for i in range(amount_of_arguments):
        num_list.append(i)

    combinations = combinations_generator(num_list)

    for rowNum in range(2 ** amount_of_arguments):
        row = []
        inversed_row = []
        for combination in combinations:
            sum_from_combinations = 0
            for num in combination:
                sum_from_combinations ^= get_nth_bit(rowNum, num)

            inversed_sum_from_combinations = sum_from_combinations ^ 1
            row.append(sum_from_combinations)
            inversed_row.append(inversed_sum_from_combinations)
        row.append(0)
        inversed_row.append(1)
        result[rowNum] = tuple(row + inversed_row)

    return result


def hamming_distance(function1, function2):
    distance = 0
    for index, _ in enumerate(function1):
        xored_value = function2[index] ^ function1[index]
        if xored_value == 1:
            distance += 1

    return distance


def calculate_function_linearity(sbox_function, linear_functions_dict_row_notation: dict, amount_of_arguments):
    min_distance = None
    columns = len(linear_functions_dict_row_notation[0])
    for column in range(columns):
        distance = hamming_distance(
            extract_function_from_row_notation(linear_functions_dict_row_notation, column, amount_of_arguments),
            sbox_function)
        if min_distance is None:
            min_distance = distance
        else:
            min_distance = min(min_distance, distance)

    return min_distance


def calculate_function_SAC(sbox_function, amount_of_arguments):
    amount_of_sbox_function_values = len(sbox_function)
    SAC_values = []
    for changed_bit in range(amount_of_arguments):
        alpha = changed_bit * 2
        if alpha == 0:
            alpha = 1
        SAC_value_for_changed_bit = 0
        for index, sbox_function_value in enumerate(sbox_function):
            function_value_with_changed_bit = sbox_function[(alpha + index) % amount_of_sbox_function_values]
            SAC_value_for_changed_bit += function_value_with_changed_bit ^ sbox_function_value

        SAC_values.append(SAC_value_for_changed_bit / amount_of_sbox_function_values)

    return average(SAC_values)


def calculate_all_functions_SAC(sbox, amount_of_arguments):
    sbox_functions = extract_functions_from_sbox(sbox, amount_of_arguments)
    all_functions_SAC = []
    for sbox_function in sbox_functions:
        all_functions_SAC.append(calculate_function_SAC(sbox_function, amount_of_arguments))

    return all_functions_SAC


def calculate_all_functions_linearity(sbox, amount_of_arguments):
    sbox_functions = extract_functions_from_sbox(sbox, amount_of_arguments)
    linear_functions = linear_functions_generator(amount_of_arguments)
    all_functions_linearity = []
    for sbox_function in sbox_functions:
        function_linearity = calculate_function_linearity(sbox_function, linear_functions, amount_of_arguments)
        all_functions_linearity.append(function_linearity)

    return all_functions_linearity


def extract_values_from_sbox(sbox):
    result = []
    skip = False
    for byte in sbox:
        if not skip:
            result.append(byte)
        skip = not skip

    return result


def calculate_cycles(checked_inputs, values_from_sbox, input_value):
    if len(checked_inputs) == 256:
        return True
    value_from_sbox = values_from_sbox[input_value]
    if value_from_sbox in checked_inputs:
        return False
    checked_inputs.add(value_from_sbox)
    return calculate_cycles(checked_inputs, values_from_sbox, value_from_sbox)


def calculate_xor(num1, num2, amount_of_arguments):
    result = 0
    for i in range(amount_of_arguments):
        xored_bit = get_nth_bit(num1, i) ^ get_nth_bit(num2, i)
        result += xored_bit * (2**i)
    
    return result


def calculate_xor_profile(amount_of_arguments, values_from_sbox):
    possible_outputs = [[0 for i in range(2**amount_of_arguments)] for j in range(2**amount_of_arguments)]
    possible_values = [i for i in range(2**amount_of_arguments)]
    combinations = list(itertools.combinations(possible_values, 2))
    for combination in combinations:
        x1 = combination[0]
        x2 = combination[1] 
        y1 = values_from_sbox[x1]
        y2 = values_from_sbox[x2]
        sum_x1_x2 = calculate_xor(x1, x2, amount_of_arguments)
        sum_y1_y2 = calculate_xor(y1, y2, amount_of_arguments)
        possible_outputs[sum_x1_x2][sum_y1_y2] += 2
    
    return max(map(max, possible_outputs))


def check_balanced(functions_from_sbox, amount_of_arguments):
    for function in functions_from_sbox:
        if sum(function) != 2**(amount_of_arguments-1):
            return False
    return True


def generate_sbox(amount_of_arguments):
    random_nums = []
    result = []
    while len(random_nums) != 2**amount_of_arguments:
        random_number = random.randint(0, (2**amount_of_arguments)-1)
        if random_number not in random_nums:
            random_nums.append(random_number)

    for num in random_nums:
        result.append(num)
        result.append(0)
    
    return result
    

def check_sbox(sbox, amount_of_arguments):
    functions_from_sbox = extract_functions_from_sbox(sbox, amount_of_arguments)
    values_from_sbox = extract_values_from_sbox(sbox)
    all_functions_linearity = calculate_all_functions_linearity(sbox, amount_of_arguments)
    all_functions_SAC = calculate_all_functions_SAC(sbox, amount_of_arguments)
    print("Balanced?: ", check_balanced(functions_from_sbox, amount_of_arguments))
    print("Linearity:", all_functions_linearity)
    print("SAC:", all_functions_SAC)
    print("SAC average:", average(all_functions_SAC))
    print("Cycles:", not calculate_cycles(set(), values_from_sbox, 0))
    print("XOR profile: ", calculate_xor_profile(amount_of_arguments, values_from_sbox))
    for index, anf_function in enumerate(calculate_rank(functions_from_sbox)):
        print("ANF form of function", index, "is:", anf_function)
    


def calculate_rank(functions_from_sbox:list):
    result = []

    for function in functions_from_sbox:
        x7, x6, x5, x4, x3, x2, x1, x0 = symbols('x7 x6 x5 x4 x3 x2 x1 x0')
        sbox_anf_form = ANFform([x7, x6, x5, x4, x3, x2, x1, x0], function)
        result.append([sbox_anf_form])
    
    return result



print("--------------------------------------------------------")
print("Given sbox:")
check_sbox(read_sbox("sbox.SBX"), 8)
print("--------------------------------------------------------")
print("Random sbox:")
check_sbox(generate_sbox(8), 8)
print("--------------------------------------------------------")