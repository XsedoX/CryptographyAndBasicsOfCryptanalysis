import random
import time
import base64
from Crypto.Cipher import AES

def main():
    P = int(input("Provide first public number P = "))
    G = int(input("Provide second public number G = "))
    a = random.randint(1, 100)
    alices_public_key = G**a % P
    fancy_print(f"Alice chooses random integer:\na = {a}")
    input()
    fancy_print(f"She also calculates her public key:\nA = G^a mod P = {G}^{a} mod {P} = {alices_public_key}")
    input()
    b = random.randint(1, 100)
    bobs_public_key = G**b % P
    fancy_print(f"Bob chooses random integer:\nb = {b}")
    input()
    fancy_print(f"He also calculates his public key:\nB = G^b mod P = {G}^{b} mod {P} = {bobs_public_key}")
    input()
    fancy_print("A and B are Alice's and Bob's public keys respectively. They can share them through public channel.")
    input()
    alices_secret = bobs_public_key**a % P
    bobs_secret = alices_public_key**b % P
    fancy_print(f"To calculate shared secret number Alice needs to calculate:\ns = B ^ a mod P = {bobs_public_key}^{a} mod {P} = {alices_secret}")
    input()
    fancy_print(f"Similarly Bob calculates the number:\ns = A ^ b mod P = {alices_public_key}^{b} mod {P} = {bobs_secret}")
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
    fancy_print(f"But he needs to prepare for it. He chooses 2 random numbers: \nc = {c}\nd = {d}\nfor Alice and Bob "
                f"respectively.\n")
    fancy_print(f"Mallet also knows:\nP = {P},\nG = {G},\nA = {alices_public_key},\nB = {bobs_public_key}\n"
                f"because these are public numbers.")
    input()
    bobs_public_key_from_mallet = G**c % P
    alices_public_key_from_mallet = G**d % P
    fancy_print(f"Alice should get Bob's public key B = {bobs_public_key} but instead she got key that Mallet calculated:\n"
                f"MB = G ^ c mod P = {G}^{c} mod {P} = {bobs_public_key_from_mallet}")
    input()
    fancy_print(f"He does the same thing to Bob:\nMA = G ^ d mod P = {G}^{d} mod {P} = {alices_public_key_from_mallet}")
    input()
    fancy_print(f"Alice got Mallet's MB while being convinced that she has got Bob's public key B.\n")
    fancy_print("Bob got Mallet's MA while also being convinced that he has got Alice's public key A.")
    input()
    alice_secret_from_mallet = bobs_public_key_from_mallet**a % P
    bob_secret_from_mallet = alices_public_key_from_mallet**b % P
    fancy_print(f"Now Alice calculates secret number \ns = MB ^ a mod P = {bobs_public_key_from_mallet}^{a} mod {P} = {alice_secret_from_mallet}\n")
    fancy_print(f"Bob also calculates secret number \ns = MA ^ b mod P = {alices_public_key_from_mallet}^{b} mod {P} = {bob_secret_from_mallet}")
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
    input()
    
    time.sleep(3)
    print("Alice, provide a message that you want to send to Bob, please: ")
    msg_to_bob = input()
    msg_sent_to_bob = aes_encryption(msg_to_bob, alices_secret)
    print("\nYour message is encrypted now and it's ready to be sent:\n", msg_sent_to_bob)
    decrypted_msg_for_bob = aes_decryption(msg_sent_to_bob, bobs_secret)
    print("\nBob, you received a message. Try to decrypt it with your private key:\n", decrypted_msg_for_bob)
    print("\n\nBob, try to respond to Alice now:", )
    msg_to_alice = input()
    msg_sent_to_alice = aes_encryption(msg_to_alice, bobs_secret)
    print("\nYour message is encrypted now and it's ready to be sent:\n", msg_sent_to_alice)
    decrypted_msg_for_alice = aes_decryption(msg_sent_to_alice, alices_secret)
    print("\nAlice, you received a message. Try to decrypt it with your private key:\n", decrypted_msg_for_alice)

    print("\nWhat if mallet intercepted any encrypted message?")
    print("\nProvide a message for Alice that she wants to send to Bob")
    alices_msg = input()
    msg_to_bob_swapped_key = aes_encryption(alices_msg, alice_secret_from_mallet)
    print("Message to Bob, encrypted with swapped key:\n", msg_to_bob_swapped_key)
    intercepted_alices_msg = aes_decryption(msg_to_bob_swapped_key, alice_secret_mallet_has)
    print("\nMallet intercepted a message from Alice and suddenly decrypted it:\n", intercepted_alices_msg)
    
    print("\nWe can do the same with Bob")
    print("\nProvide a message for Bob that she wants to send to Alice")
    bobs_msg = input()
    msg_to_alice_swapped_key = aes_encryption(bobs_msg, bob_secret_from_mallet)
    print("Message to Alice, encrypted with swapped key:\n", msg_to_alice_swapped_key)
    intercepted_bobs_msg = aes_decryption(msg_to_alice_swapped_key, bob_secret_mallet_has)
    print("\nMallet intercepted a message from Bob and suddenly decrypted it:\n", intercepted_bobs_msg)

def aes_encryption(plaintext, key):
    key = str(key)
    key_up_to_32_bytes = str.encode(key.zfill(32))
    text_up_to_256_bytes = str.encode(plaintext.zfill(256))
    cipher = AES.new(key_up_to_32_bytes, AES.MODE_ECB)
    ciphertext = cipher.encrypt(text_up_to_256_bytes)
    ciphertext_base64 = base64.b64encode(ciphertext).decode('utf-8')
    return ciphertext_base64

def aes_decryption(ciphertext, key):
    key = str(key)
    key_up_to_32_bytes = str.encode(key.zfill(32))
    ciphertext_base64_decoded = base64.b64decode(ciphertext)
    cipher = AES.new(key_up_to_32_bytes, AES.MODE_ECB)
    plaintext_byte_string = (cipher.decrypt(ciphertext_base64_decoded)).decode()
    plaintext = remove_zeros_from_zfill(plaintext_byte_string)
    return plaintext

def remove_zeros_from_zfill(text):
    list = [i.lstrip('0') for i in text]
    return "".join(list)

def fancy_print(text: str):
    for letter in text:
        print(letter, end="", sep="")
        time.sleep(0.03)

if __name__ == "__main__":
    main()