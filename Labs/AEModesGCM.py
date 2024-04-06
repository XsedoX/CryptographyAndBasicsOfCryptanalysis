import random
import math

P = "To jest tekst to zaszyfrowania."
A = "Header przykladowy."


def text_to_binary(text: str) -> str:
    return "".join(format(ord(x), 'b') for x in text)


def integer_to_string(x: int, s: int) -> str:
    binary_string = bin(x)[2:]
    padded_string = binary_string.zfill(s)
    return padded_string


def to_blocks(message: str) -> list[str]:
    result = [message[i:i + 128] for i in range(0, len(message), 128)]
    last_block_len = len(result[-1])
    missing_amount_of_bits = 128 - last_block_len
    missing_amount_of_bytes = int(missing_amount_of_bits / 8)
    for i in range(missing_amount_of_bytes):
        result[-1] += integer_to_string(missing_amount_of_bytes, 8)

    if len(result[-1]) != 128:
        raise ValueError("Last block wrong length")
    return result


def string_to_integer(X: str) -> int:
    return int(X, 2)


def inc(X: str, s: int) -> str:
    if len(X) < s:
        raise ValueError("s is higher than len(X) in increment")
    lsb = LSB(X, s)
    return MSB(X, len(X) - s) + integer_to_string((string_to_integer(lsb) + 1) % 2 ** s, s)


def generate_s_bits(s: int, bit: int) -> str:
    result = ""
    if bit not in [0, 1]:
        raise ValueError("Bit has to be 0 or 1.")
    for i in range(s):
        result += str(bit)

    return result


def LSB(X: str, s: int) -> str:
    if len(X) < s:
        raise ValueError("X is less than s in LSB")
    return X[len(X) - s: len(X)]


def MSB(X: str, s: int) -> str:
    if len(X) < s:
        raise ValueError("X is less than s in MSB")
    return X[0: s]


def right_shift(X: str) -> str:
    return "0" + X[:-1]


def xor(number1: str, number2: str) -> str:
    if len(number1) != len(number2):
        raise ValueError("xor numbers are not the same length")
    result = ""
    for index in range(len(number2)):
        result += str(int(number2[index]) ^ int(number1[index]))

    return result


def toInt(X: str) -> int:
    result = 0
    for index in range(len(X)):
        result += int(X[len(X) - index - 1]) * 2 ** index

    return result


def checkVariablesRequirements(p: str, a: str, iv: str) -> None:
    if len(p) > 2 ** 39 - 256:
        raise ValueError("Message to long")
    if len(a) > 2 ** 64 - 1:
        raise ValueError("Additional authenticated data too long")
    if (len(iv) < 1) or (len(iv) > 2 ** 64 - 1):
        raise ValueError("IV does not meet requirements")


def blocks_multiplication(X: str, Y: str) -> str:
    Z = [generate_s_bits(128, 0)]
    V = [Y]
    R = "11100001" + generate_s_bits(120, 0)
    if len(X) != 128:
        raise ValueError("X does not have 128 bits")
    if len(Y) != 128:
        raise ValueError("Y does not have 128 bits")
    for i in range(128):
        if X[i] == "0":
            Z.append(Z[i])
        elif X[i] == "1":
            Z.append(xor(Z[i], V[i]))

        if LSB(V[i], 1) == "0":
            V.append(right_shift(V[i]))
        elif LSB(V[i], 1) == "1":
            V.append(xor(right_shift(V[i]), R))

    return Z[128]


def CIPH(K: str, cypher_block: str) -> str:
    return ""


def GHASH(H: str, X: str) -> str:
    X = to_blocks(X)
    m = len(X)
    Y = [generate_s_bits(128, 0)]
    for i in range(1, m + 1):
        Y.append(blocks_multiplication(xor(Y[i - 1], X[i - 1]), H))
    return Y[m]


def GCTR(K: str, ICB: str, X: str) -> str:
    if len(X) == 0:
        return ""
    n = math.ceil(len(X) / 128)
    X = to_blocks(X)
    CB = ["", ICB]
    Y = []
    result = ""
    for i in range(2, n + 1):
        CB.append(inc(CB[i - 1], 32))

    for i in range(1, n):
        Y.append(xor(X[i], CIPH(K, CB[i])))

    Y.append(xor(X[n], MSB(CIPH(K, CB[n]), len(X[n]))))
    for y in Y:
        result += y

    return result


def GCM_AE(K: str, IV: str, P: str, A: str) -> tuple[str, str]:
    H = CIPH(K, generate_s_bits(128, 0))
    if len(IV) == 96:
        J = [IV + generate_s_bits(31, 0) + "1"]
    else:
        s = (128 * math.ceil(len(IV) / 128)) - len(IV)
        J = [GHASH(H, IV + generate_s_bits(s + 64, 0) + integer_to_string(len(IV), 64))]

    C = GCTR(K, inc(J[0], 32), P)
    u = (128 * math.ceil(len(C) / 128)) - len(C)
    v = (128 * math.ceil(len(A) / 128)) - len(A)
    S = GHASH(H, A + generate_s_bits(v, 0) + C + generate_s_bits(u, 0) + integer_to_string(len(A), 64)
              + integer_to_string(len(C), 64))
    T = MSB(GCTR(K, J[0], S), 128)
    return C, T


def GCM_AD(K: str, IV: str, C: str, A: str, T: str) -> str:
    H = CIPH(K, generate_s_bits(128, 0))
    if len(IV) == 96:
        J = [IV + generate_s_bits(31, 0) + "1"]
    else:
        s = (128 * math.ceil(len(IV) / 128)) - len(IV)
        J = [GHASH(H, IV + generate_s_bits(s + 64, 0) + integer_to_string(len(IV), 64))]
    P = GCTR(K, inc(J[0], 32), C)
    u = (128 * math.ceil(len(C) / 128)) - len(C)
    v = (128 * math.ceil(len(A) / 128)) - len(A)
    S = GHASH(H, A + generate_s_bits(v, 0) + C + generate_s_bits(u, 0) + integer_to_string(len(A), 64)
              + integer_to_string(len(C), 64))
    T_prim = MSB(GCTR(K, J[0], S), 128)
    if T == T_prim:
        return P
    else:
        return "Fail"



P_binary = text_to_binary(P)
A_binary = text_to_binary(A)

IV = str(random.getrandbits(128))
K = str(random.getrandbits(128))
IV_binary = text_to_binary(IV)
K_binary = text_to_binary(K)

checkVariablesRequirements(P_binary, A_binary, IV_binary)
