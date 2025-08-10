from Crypto.Cipher import AES, ChaCha20, DES
from Crypto.Util import Counter
from Crypto.Cipher._mode_cbc import CbcMode
from Crypto.Cipher._mode_ctr import CtrMode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.decrepit.ciphers.algorithms import TripleDES, Blowfish

KEY_128 = b"\x00" * 16
KEY_256 = b"\x00" * 32
TRIPLE_DES_KEY = b'\x00' * 8 + b'\x11' * 8 + b'\x22' * 8
DES_KEY = b'\x00' * 8
IV = b"\x00" * 16

def zero_bytes(num_bytes: int):
    return num_bytes * b"\x00"


def get_pycrypto_aes_cipher(key, use_aesni) -> CtrMode:
    nonce = IV[:8]             # first 8 bytes
    counter_bytes = IV[8:]     # last 8 bytes

    # Convert counter_bytes to integer for initial counter value
    initial_counter = int.from_bytes(counter_bytes, byteorder='big')

    ctr = Counter.new(64, prefix=nonce, initial_value=initial_counter)
    return AES.new(key, AES.MODE_CTR, counter=ctr, use_aesni=use_aesni)


def get_openssl_aes_encryptor(key):
    cipher = Cipher(algorithms.AES(key), modes.CTR(IV))
    return cipher.encryptor().update


def get_openssl_aes_decryptor(key):
    cipher = Cipher(algorithms.AES(key), modes.CTR(IV))
    return cipher.decryptor().update


def get_openssl_chacha20_encryptor():
    return Cipher(algorithms.ChaCha20(KEY_256, nonce=zero_bytes(16)), mode=None).encryptor().update


def get_openssl_chacha20_decryptor():
    return Cipher(algorithms.ChaCha20(KEY_256, nonce=zero_bytes(16)), mode=None).decryptor().update


def get_openssl_3des_encryptor_and_padder():
    encryptor = Cipher(TripleDES(TRIPLE_DES_KEY), mode=modes.CBC(zero_bytes(8))).encryptor()
    return encryptor.update, encryptor.finalize


def get_openssl_3des_decryptor_and_unpadder():
    decryptor = Cipher(TripleDES(TRIPLE_DES_KEY), mode=modes.CBC(zero_bytes(8))).decryptor()
    return decryptor.update, decryptor.finalize


def get_openssl_blowfish_encryptor_and_padder():
    encryptor = Cipher(Blowfish(KEY_256), mode=modes.CBC(zero_bytes(8))).encryptor()
    return encryptor.update, encryptor.finalize


def get_openssl_blowfish_decryptor_and_unpadder():
    decryptor = Cipher(Blowfish(KEY_256), mode=modes.CBC(zero_bytes(8))).decryptor()
    return decryptor.update, decryptor.finalize

def get_pycrypto_des_cipher() -> CbcMode:
    return DES.new(key=DES_KEY, mode=DES.MODE_CBC, iv=zero_bytes(8))