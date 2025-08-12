from Crypto.Cipher import AES as _AES, DES as _DES
from Crypto.Util import Counter as _Counter
from Crypto.Cipher._mode_cbc import CbcMode as _CbcMode
from Crypto.Cipher._mode_ctr import CtrMode as _CtrMode
from cryptography.hazmat.primitives.ciphers import Cipher as _Cipher, algorithms as _algorithms, modes as _modes
from cryptography.hazmat.decrepit.ciphers.algorithms import TripleDES as _3DES, Blowfish as _Blowfish


# Private consts
_TRIPLE_DES_KEY = b'\x00' * 8 + b'\x11' * 8 + b'\x22' * 8
_DES_KEY = b'\x00' * 8
_IV = b"\x00" * 16

# Public consts
KEY_128 = b"\x00" * 16
KEY_256 = b"\x00" * 32

def _zero_bytes(num_bytes: int):
    return num_bytes * b"\x00"


def get_pycrypto_aes_cipher(key, aesni) -> _CtrMode:
    nonce = _IV[:8]             # first 8 bytes
    counter_bytes = _IV[8:]     # last 8 bytes

    # Convert counter_bytes to integer for initial counter value
    initial_counter = int.from_bytes(counter_bytes, byteorder='big')

    ctr = _Counter.new(64, prefix=nonce, initial_value=initial_counter)
    return _AES.new(key, _AES.MODE_CTR, counter=ctr, use_aesni=aesni)


def get_openssl_aes_encryptor(key):
    cipher = _Cipher(_algorithms.AES(key), _modes.CTR(_IV))
    return cipher.encryptor().update


def get_openssl_aes_decryptor(key):
    cipher = _Cipher(_algorithms.AES(key), _modes.CTR(_IV))
    return cipher.decryptor().update


def get_openssl_chacha20_encryptor():
    return _Cipher(_algorithms.ChaCha20(KEY_256, nonce=_zero_bytes(16)), mode=None).encryptor().update


def get_openssl_chacha20_decryptor():
    return _Cipher(_algorithms.ChaCha20(KEY_256, nonce=_zero_bytes(16)), mode=None).decryptor().update


def get_openssl_3des_encryptor_and_padder():
    encryptor = _Cipher(_3DES(_TRIPLE_DES_KEY), mode=_modes.CBC(_zero_bytes(8))).encryptor()
    return encryptor.update, encryptor.finalize


def get_openssl_3des_decryptor_and_unpadder():
    decryptor = _Cipher(_3DES(_TRIPLE_DES_KEY), mode=_modes.CBC(_zero_bytes(8))).decryptor()
    return decryptor.update, decryptor.finalize


def get_openssl_blowfish_encryptor_and_padder():
    encryptor = _Cipher(_Blowfish(KEY_256), mode=_modes.CBC(_zero_bytes(8))).encryptor()
    return encryptor.update, encryptor.finalize


def get_openssl_blowfish_decryptor_and_unpadder():
    decryptor = _Cipher(_Blowfish(KEY_256), mode=_modes.CBC(_zero_bytes(8))).decryptor()
    return decryptor.update, decryptor.finalize

def get_pycrypto_des_cipher() -> _CbcMode:
    return _DES.new(key=_DES_KEY, mode=_DES.MODE_CBC, iv=_zero_bytes(8))
