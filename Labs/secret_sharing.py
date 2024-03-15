from Crypto.Util import number
import random

p = number.getPrime(1024)
a0 = 954
n = 4
t = 3


def generate_t_minus_1_random_numbers():
    result = []
    for i in range(1, t):
        result.append(random.randint(1, p))
    return result


a = [a0] + generate_t_minus_1_random_numbers()


def calculate_shares():
    result = []
    for i in range(1, n + 1):
        summ = 0
        for j in range(t):
            summ += a[j] * i ** j
        summ = summ % p
        result.append((i, summ))

    return result


s = calculate_shares()
print("Calculated shares:", s)

secrets_to_recover_from = [s[1], s[2], s[3]]
print("Shares chosen to recover from:", [row[0] for row in secrets_to_recover_from])


def lagrange():
    recovered_secret, x = 0, 0
    for i in range(t):
        multi = 1
        for j in range(t):
            if j == i:
                continue
            multi *= (x - secrets_to_recover_from[j][0]) * pow(secrets_to_recover_from[i][0] - secrets_to_recover_from[j][0], -1, p)

        multi = multi % p
        recovered_secret += secrets_to_recover_from[i][1] * multi
    recovered_secret = recovered_secret % p
    return recovered_secret


calculated_secret = lagrange()
print("Data at the start:\n"
      "secret = {}\n"
      "p = {}\n"
      "n = {}\n"
      "t = {}".format(a0, p, n, t, a))
print("Recovered secret:", calculated_secret)
