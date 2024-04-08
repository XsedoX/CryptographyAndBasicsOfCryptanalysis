# Based on https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-38d.pdf#%5B%7B%22num%22%3A31%2C%22gen%22%3A0%7D%2C%7B%22name%22%3A%22XYZ%22%7D%2C93%2C721%2Cnull%5D
import random
import math
from Crypto.Cipher import AES


def text_to_binary(text: str) -> str:
    byte_data = bytes(text, encoding="utf-8")
    bits = ""
    for byte in byte_data:
        bits += bin(byte)[2:].zfill(8)

    return bits


def bytes_to_binary(byte_data: bytes) -> str:
    bits = ""
    for byte in byte_data:
        bits += bin(byte)[2:].zfill(8)

    return bits


def binary_to_bytes(bits_string: str) -> bytearray:
    result = bytearray()
    for i in range(0, len(bits_string), 8):
        byte_value = int(bits_string[i:i+8], 2)
        result.append(byte_value)
    return result


def binary_to_text(bits: str) -> str:
    if len(bits) % 8 != 0:
        raise ValueError("Binary string length must be a multiple of 8")
    byte_data = bytearray()
    for i in range(0, len(bits), 8):
        byte_value = int(bits[i:i+8], 2)
        byte_data.append(byte_value)

    return byte_data.decode("utf-8")


def integer_to_binary(x: int, s: int) -> str:
    binary_string = bin(x)[2:]
    padded_string = binary_string.zfill(s)
    return padded_string


def to_blocks(message: str) -> list[str]:
    result = [message[i:i + 128] for i in range(0, len(message), 128)]
    # A good practise is to use padding as PKCS#7 is suggesting.

    # last_block_len = len(result[-1])
    # missing_amount_of_bits = 128 - last_block_len
    # missing_amount_of_bytes = missing_amount_of_bits // 8
    # for i in range(missing_amount_of_bytes):
    #     result[-1] += integer_to_string(missing_amount_of_bytes, 8)
    #
    # if len(result[-1]) != 128:
    #     raise ValueError("Last block wrong length")
    return result


def binary_to_integer(X: str) -> int:
    return int(X, 2)


def inc(X: str, s: int) -> str:
    if len(X) < s:
        raise ValueError("s is higher than len(X) in increment")
    lsb = LSB(X, s)
    return MSB(X, len(X) - s) + integer_to_binary((binary_to_integer(lsb) + 1) % (2 ** s), s)


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
    len1 = len(number1)
    len2 = len(number2)
    if len1 > len2:
        number2 = generate_s_bits(len1-len2, 0) + number2
    elif len2 > len1:
        number1 = generate_s_bits(len2-len1, 0) + number1

    result = ""
    for index in range(len2):
        result += str(int(number2[index]) ^ int(number1[index]))

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
            if len(Z[-1]) != 128:
                raise ValueError("Z does not have 128 bits")
        elif X[i] == "1":
            Z.append(xor(Z[i], V[i]))
            if len(Z[-1]) != 128:
                raise ValueError("Z does not have 128 bits")
        if LSB(V[i], 1) == "0":
            V.append(right_shift(V[i]))
            if len(V[-1]) != 128:
                raise ValueError("V does not have 128 bits")
        elif LSB(V[i], 1) == "1":
            V.append(xor(right_shift(V[i]), R))
            if len(V[-1]) != 128:
                raise ValueError("V does not have 128 bits")

    return Z[128]


def CIPH(K: str, data_to_encode: str, iv: str) -> str:
    cipher = AES.new(binary_to_bytes(K), AES.MODE_GCM, nonce=binary_to_bytes(iv))
    ct_bytes = cipher.encrypt(binary_to_bytes(data_to_encode))
    return bytes_to_binary(ct_bytes)


def GHASH(H: str, X: str) -> str:
    X = to_blocks(X)
    m = len(X)
    Y = [generate_s_bits(128, 0)]
    for i in range(1, m + 1):
        Y.append(blocks_multiplication(xor(Y[i - 1], X[i - 1]), H))
    return Y[m]


def GCTR(K: str, ICB: str, X: str, IV: str) -> str:
    if len(X) == 0:
        return ""
    n = math.ceil(len(X) / 128)
    X = [""] + to_blocks(X)
    CB = ["", ICB]
    Y = [""]
    result = ""
    for i in range(2, n + 1):
        CB.append(inc(CB[i - 1], 32))

    for i in range(1, n):
        Y.append(xor(X[i], CIPH(K, CB[i], IV)))

    Y.append(xor(X[n], MSB(CIPH(K, CB[n], IV), len(X[n]))))
    for y in Y:
        result += y

    return result


def GCM_AE(K: str, IV: str, P: str, A: str) -> tuple[str, str]:
    H = CIPH(K, generate_s_bits(128, 0), IV)
    if len(IV) == 96:
        J = [IV + generate_s_bits(31, 0) + "1"]
    else:
        s = (128 * math.ceil(len(IV) / 128)) - len(IV)
        J = [GHASH(H, IV + generate_s_bits(s + 64, 0) + integer_to_binary(len(IV), 64))]

    C = GCTR(K, inc(J[0], 32), P, IV)
    u = (128 * math.ceil(len(C) / 128)) - len(C)
    v = (128 * math.ceil(len(A) / 128)) - len(A)
    S = GHASH(H, A + generate_s_bits(v, 0) + C + generate_s_bits(u, 0) + integer_to_binary(len(A), 64)
              + integer_to_binary(len(C), 64))
    T = MSB(GCTR(K, J[0], S, IV), 128)
    return C, T


def GCM_AD(K: str, IV: str, C: str, A: str, T: str) -> str:
    H = CIPH(K, generate_s_bits(128, 0), IV)
    if len(IV) == 96:
        J = [IV + generate_s_bits(31, 0) + "1"]
    else:
        s = (128 * math.ceil(len(IV) / 128)) - len(IV)
        J = [GHASH(H, IV + generate_s_bits(s + 64, 0) + integer_to_binary(len(IV), 64))]
    P = GCTR(K, inc(J[0], 32), C, IV)
    u = (128 * math.ceil(len(C) / 128)) - len(C)
    v = (128 * math.ceil(len(A) / 128)) - len(A)
    S = GHASH(H, A + generate_s_bits(v, 0) + C + generate_s_bits(u, 0) + integer_to_binary(len(A), 64)
              + integer_to_binary(len(C), 64))
    T_prim = MSB(GCTR(K, J[0], S, IV), 128)
    if T == T_prim:
        return binary_to_text(P)
    else:
        return "Fail"


def main() -> None:
    P = "To jest tekst do zaszyfrowania."
    A = "Header przykladowy."
    P_binary = text_to_binary(P)
    A_binary = text_to_binary(A)

    IV = random.getrandbits(128)
    K = random.getrandbits(128)
    IV_binary = integer_to_binary(IV, 128)
    K_binary = integer_to_binary(K, 128)

    checkVariablesRequirements(P_binary, A_binary, IV_binary)

    print("P =", P)
    print("A =", A)
    print("IV =", IV)
    print("K =", K)
    cyphertext, authentication_tag = GCM_AE(K_binary, IV_binary, P_binary, A_binary)
    print("Cyphertext =", cyphertext)
    print("Authentication tag =", authentication_tag)
    decryption_result = GCM_AD(K_binary, IV_binary, cyphertext, A_binary, authentication_tag)
    print("Decryption result =", decryption_result)


if __name__ == "__main__":
    main()


