import random
import time


def main():
    P = int(input("Provide first public number P = "))
    G = int(input("Provide second public number G = "))
    a = random.randint(1, 100)
    alices_public_key = G**a % P
    fancy_print(f"Alice chooses random integer:\n"
                f"a = {a}")
    input()
    fancy_print(f"She also calculates her public key:\n"
                f"A = G^a mod P = {G}^{a} mod {P} = {alices_public_key}")
    input()
    b = random.randint(1, 100)
    bobs_public_key = G**b % P
    fancy_print(f"Bob chooses random integer:\n"
                f"b = {b}")
    input()
    fancy_print(f"He also calculates his public key:\n"
                f"B = G^b mod P = {G}^{b} mod {P} = {bobs_public_key}")
    input()
    fancy_print("A and B are Alice's and Bob's public keys respectively. They can share them through public channel.")
    input()
    alices_secret = bobs_public_key**a % P
    bobs_secret = alices_public_key**b % P
    fancy_print(f"To calculate shared secret number Alice needs to calculate:\n"
                f"s = B ^ a mod P = {bobs_public_key}^{a} mod {P} = {alices_secret}")
    input()
    fancy_print(f"Similarly Bob calculates the number:\n"
                f"s = A ^ b mod P = {alices_public_key}^{b} mod {P} = {bobs_secret}")
    input()
    fancy_print("Now what if someone interrupts the exchange?\n")
    fancy_print("What if someone catches the numbers A and B?")
    input()
    fancy_print("Let's introduce Mallet. He is a really smart guy.")
    input()
    fancy_print("Mallet intercepted exchange of public keys between Alice and Bob.")
    input()
    c = random.randint(0, 100)
    d = random.randint(0, 100)
    fancy_print("He additionally swapped values of A and B with his owns, in a way that both Alice and Bob had no "
                "idea about it.")
    input()
    fancy_print(f"But he needs to prepare for it. He chooses 2 random numbers: \n"
                f"c = {c}\n"
                f"d = {d}\n"
                f"for Alice and Bob "
                f"respectively.\n")
    fancy_print(f"Mallet also knows:\n"
                f"P = {P},\n"
                f"G = {G},\n"
                f"A = {alices_public_key},\n"
                f"B = {bobs_public_key}\n"
                f"because these are public numbers.")
    input()
    bobs_public_key_from_mallet = G**c % P
    alices_public_key_from_mallet = G**d % P
    fancy_print(f"Alice should get Bob's public key B = {bobs_public_key} but instead she got key that Mallet calculated:\n"
                f"MB = G ^ c mod P = {G}^{c} mod {P} = {bobs_public_key_from_mallet}")
    input()
    fancy_print(f"He does the same thing to Bob:\n"
                f"MA = G ^ d mod P = {G}^{d} mod {P} = {alices_public_key_from_mallet}")
    input()
    fancy_print(f"Alice got Mallet's MB while being convinced that she has got Bob's public key B.\n")
    fancy_print("Bob got Mallet's MA while also being convinced that he has got Alice's public key A.")
    input()
    alice_secret_from_mallet = bobs_public_key_from_mallet**a % P
    bob_secret_from_mallet = alices_public_key_from_mallet**b % P
    fancy_print(f"Now Alice calculates secret number \n"
                f"s = MB ^ a mod P = {bobs_public_key_from_mallet}^{a} mod {P} = {alice_secret_from_mallet}\n")
    fancy_print(f"Bob also calculates secret number \n"
                f"s = MA ^ b mod P = {alices_public_key_from_mallet}^{b} mod {P} = {bob_secret_from_mallet}")
    input()
    alice_secret_mallet_has = alices_public_key**c % P
    bob_secret_mallet_has = bobs_public_key**d % P
    fancy_print(f"Now Bob has got {bob_secret_from_mallet}, Alice has got {alice_secret_from_mallet} and Mallet can calculate these numbers by using:\n"
                f"c = {c}\n"
                f"d = {d}.\n")
    fancy_print("Alice's secret number that Mallet can calculate using Alice's public key A (that Bob has never got):\n"
                f"s = A ^ c mod P = {alices_public_key} ^ {c} mod {P} = {alice_secret_mallet_has}\n")
    fancy_print("Bob's secret that Mallet also has using Bob's public key (that Alice has never got):\n"
                f"s = B ^ d mod P = {bobs_public_key} ^ {d} mod {P} = {bob_secret_mallet_has}\n")
    fancy_print("Malice can decrypt, edit and then encrypt the communication between Alice and Bob without them noticing it.")


def fancy_print(text: str):
    for letter in text:
        print(letter, end="", sep="")
        time.sleep(0.03)


if __name__ == "__main__":
    main()