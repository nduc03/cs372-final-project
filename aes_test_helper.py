from Crypto.Cipher import AES
from Crypto.Util import Counter
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def get_pycrypto_cipher(key, iv, use_aesni):
    nonce = iv[:8]             # first 8 bytes
    counter_bytes = iv[8:]     # last 8 bytes

    # Convert counter_bytes to integer for initial counter value
    initial_counter = int.from_bytes(counter_bytes, byteorder='big')

    ctr = Counter.new(64, prefix=nonce, initial_value=initial_counter)
    return AES.new(key, AES.MODE_CTR, counter=ctr, use_aesni=use_aesni)


def get_openssl_encryptor(key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CTR(iv))
    return cipher.encryptor().update


def get_openssl_decryptor(key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CTR(iv))
    return cipher.decryptor().update