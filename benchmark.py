from benchmark_helper import *
from crypto_helper import *
from matplotlib_helper import plot_raw_benchmark

# Benchmark in AES 3 categories:
# Full software AES-CTR using PyCryptodome
# AES-NI mode CTR using PyCryptodome (hardware accelerated + Python cross-platform) (remove)
# AES-CTR using OpenSSL backend (hardware accelerated + platform optimized)

# TODO: plot results

# benchmark
benchmark_list = [
    CipherBenchmarkCategory("AES encryption", initialize_data)
        .add_test(CipherBenchmark("Software AES-CTR-128 encryption", get_pycrypto_aes_cipher(KEY_128, False).encrypt))
        .add_test(CipherBenchmark("Software AES-CTR-256 encryption", get_pycrypto_aes_cipher(KEY_256, False).encrypt))
        .add_test(CipherBenchmark("OpenSSL (hwaccel) AES-CTR-128 encryption", get_openssl_aes_encryptor(KEY_128)))
        .add_test(CipherBenchmark("OpenSSL (hwaccel) AES-CTR-256 encryption", get_openssl_aes_encryptor(KEY_256))),
    #------------------------------------------------
    CipherBenchmarkCategory("AES decryption key 128", lambda: initialize_encrypted_data(get_openssl_aes_encryptor(KEY_128)))
        .add_test(CipherBenchmark("Software AES-CTR-128 decryption", get_pycrypto_aes_cipher(KEY_128, False).decrypt))
        .add_test(CipherBenchmark("OpenSSL (hwaccel) AES-CTR-128 decryption", get_openssl_aes_decryptor(KEY_128))),
    #------------------------------------------------
    CipherBenchmarkCategory("AES decryption key 256", lambda: initialize_encrypted_data(get_openssl_aes_encryptor(KEY_256)))
        .add_test(CipherBenchmark("Software AES-CTR-256 decryption", get_pycrypto_aes_cipher(KEY_256, False).decrypt))
        .add_test(CipherBenchmark("OpenSSL (hwaccel) AES-CTR-256 decryption", get_openssl_aes_decryptor(KEY_256))),
    #------------------------------------------------
    CipherBenchmarkCategory("ChaCha20 encryption", initialize_data)
        .add_test(CipherBenchmark("OpenSSL ChaCha20 encryption", get_openssl_chacha20_encryptor())),
    #------------------------------------------------
    CipherBenchmarkCategory("ChaCha20 decryption", lambda: initialize_encrypted_data(get_openssl_chacha20_encryptor()))
        .add_test(CipherBenchmark("OpenSSL ChaCha20 decryption", get_openssl_chacha20_decryptor())),
    #------------------------------------------------
    CipherBenchmarkCategory("Blowfish encryption", initialize_data)
        .add_test(CipherBenchmark("OpenSSL Blowfish-CBC encryption", get_openssl_blowfish_encryptor_and_padder()[0])),
    #------------------------------------------------
    CipherBenchmarkCategory("Blowfish decryption", lambda: initialize_encrypted_data_hazmat_cbc(get_openssl_blowfish_encryptor_and_padder()))
        .add_test(CipherBenchmark("OpenSSL Blowfish-CBC decryption", get_openssl_blowfish_decryptor_and_unpadder()[0])),
    #------------------------------------------------
    CipherBenchmarkCategory("3DES encryption", initialize_data)
        .add_test(CipherBenchmark("OpenSSL 3DES-CBC encryption", get_openssl_3des_encryptor_and_padder()[0])),
    #------------------------------------------------
    CipherBenchmarkCategory("3DES decryption", lambda: initialize_encrypted_data_hazmat_cbc(get_openssl_3des_encryptor_and_padder()))
        .add_test(CipherBenchmark("OpenSSL 3DES-CBC decryption", get_openssl_3des_decryptor_and_unpadder()[0])),
    #------------------------------------------------
    CipherBenchmarkCategory("DES encryption", initialize_data)
        .add_test(CipherBenchmark("PyCryptodome DES-CBC encryption", get_pycrypto_des_cipher().encrypt)),
    #------------------------------------------------
    CipherBenchmarkCategory("DES decryption", lambda: initialize_encrypted_data_pycrypto_cbc(get_pycrypto_des_cipher()))
        .add_test(CipherBenchmark("PyCryptodome DES-CBC decryption", get_pycrypto_des_cipher().decrypt)),

]

for category in benchmark_list:
    print(f"Benchmarking category: {category.name}")
    category_results = category.test()
    print("-" * 80)
    print("\nPreview results:")
    for label, data_size, result in category_results:
        rounded_result = [round(r, 2) for r in result]
        rounded_result_throughput = [round(r, 2) for r in to_MBPS(result)]
        print(f"{label} ({data_size / 1024 / 1024} MiB) execution time (seconds): {rounded_result}")
        print(f"{label} ({data_size / 1024 / 1024} MiB) throughput (MiB/s): {rounded_result_throughput}")
    print("\n")
    print("-" * 80)

    # plot_raw_benchmark(category_results)
