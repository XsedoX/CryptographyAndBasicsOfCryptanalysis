import itertools


def file_reader(path):
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
    for byte in sbox:
        if not skip:
            for nthBit in range(amount_of_arguments):
                result[nthBit].append(get_nth_bit(byte, nthBit))
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


def calculate_all_functions_SAC(amount_of_arguments):
    sbox = file_reader("sbox.SBX")
    sbox_functions = extract_functions_from_sbox(sbox, amount_of_arguments)
    all_functions_SAC = []
    for sbox_function in sbox_functions:
        all_functions_SAC.append(calculate_function_SAC(sbox_function, amount_of_arguments))

    print("SAC:", all_functions_SAC)
    print("SAC average:", average(all_functions_SAC))


def calculate_all_functions_linearity(amount_of_arguments):
    sbox = file_reader("sbox.SBX")
    sbox_functions = extract_functions_from_sbox(sbox, amount_of_arguments)
    linear_functions = linear_functions_generator(amount_of_arguments)
    all_functions_linearity = []
    for sbox_function in sbox_functions:
        function_linearity = calculate_function_linearity(sbox_function, linear_functions, amount_of_arguments)
        all_functions_linearity.append(function_linearity)

    print("Linearity:", all_functions_linearity)
    print("Linearity average:", average(all_functions_linearity))


calculate_all_functions_linearity(8)
calculate_all_functions_SAC(8)
