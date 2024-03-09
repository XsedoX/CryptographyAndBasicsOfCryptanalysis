from math import sqrt
from itertools import combinations


def geometric_series_sum(n, a, r):
    return a * ((1 - (r ** n)) / (1 - r))


def factorial(n):
    if n == 0:
        return 1
    result = n
    for i in range(1, n):
        result *= i
    return result


def binomial_coefficient(n, k):
    return factorial(n) / (factorial(k) * factorial(n - k))


def pascals_triangle(rows_amount):
    triangle = []
    for rowNum in range(rows_amount):
        row = [1]
        for column in range(rowNum):
            row.append(1)
        triangle.append(row)

    for rowNum in range(1, len(triangle) - 1):
        for columnNum in range(len(triangle[rowNum]) - 1):
            row_sum = triangle[rowNum][columnNum] + triangle[rowNum][columnNum + 1]
            triangle[rowNum + 1][columnNum + 1] = row_sum

    return triangle


def prime_num_finder(n):
    primes = [True for _ in range(n + 1)]
    for i in range(2, int(sqrt(n))):
        if primes[i]:
            for j in range(i * i, n+1, i):
                primes[j] = False

    result = []
    for index in range(2, n+1):
        if primes[index]:
            result.append(index)

    return result


def goldbach_conjecture(n):
    primes = prime_num_finder(n)
    for numberToCheck in range(4, 100, 2):
        available_primes = [prime for prime in primes if prime <= numberToCheck]
        available_combinations = list(combinations(available_primes, 2))
        is_prime_sum = False
        for available_combination in available_combinations:
            if sum(available_combination) == numberToCheck:
                is_prime_sum = True
                break
            if numberToCheck % available_combination[0] == 0:
                is_prime_sum = True
                break
            if numberToCheck % available_combination[1] == 0:
                is_prime_sum = True
                break
                
        if not is_prime_sum:
            return False
    return True


print("Goldbach's Conjecture verification for n=10000 is", goldbach_conjecture(10000))
print("Prime numbers to 10000 =", prime_num_finder(10000))
print("Pascal's triangle for 8 rows =", pascals_triangle(8))
print("Binomial coefficient n=22, k=3 =", binomial_coefficient(22, 3))
print("10! =", factorial(10))
print("Geometric series sum =", geometric_series_sum(4, 10, 3))
