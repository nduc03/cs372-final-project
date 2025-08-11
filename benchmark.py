from benchmark_helper import *
from crypto_helper import *
from matplotlib_helper import plot_benchmark


# TODO: plot results

def start_benchmark(benchmark_categories_list):
    test_result = []
    for category in benchmark_categories_list:
        print(f"Benchmarking category: {category.name}")
        category_results = category.test()
        test_result.extend(category_results)
        print("-" * 80)
        print("\nPreview results:")
        for label, data_size, result in category_results:
            rounded_result = [round(r, 2) for r in result]
            rounded_result_throughput = [round(r, 2) for r in to_MBPS(result)]
            print(f"{label} ({data_size / 1024 / 1024} MiB) execution time (seconds): {rounded_result}")
            print(f"{label} ({data_size / 1024 / 1024} MiB) throughput (MiB/s): {rounded_result_throughput}")
        print("\n")
        print("-" * 80)

    return test_result

# benchmark
benchmark_encryption = [
    # Encrypt
    CipherBenchmarkCategory("Encryption", initialize_data)
        # AES-128
        .add_test(CipherBenchmark("PyCryptodome AES-CTR-128", get_pycrypto_aes_cipher(KEY_128, False).encrypt))
        .add_test(CipherBenchmark("OpenSSL (hwaccel) AES-CTR-128", get_openssl_aes_encryptor(KEY_128)))
        # AES-256
        .add_test(CipherBenchmark("PyCryptodome AES-CTR-256", get_pycrypto_aes_cipher(KEY_256, False).encrypt))
        .add_test(CipherBenchmark("OpenSSL (hwaccel) AES-CTR-256", get_openssl_aes_encryptor(KEY_256)))
        # ChaCha20
        .add_test(CipherBenchmark("OpenSSL ChaCha20", get_openssl_chacha20_encryptor()))
        # Blowfish
        .add_test(CipherBenchmark("OpenSSL Blowfish-CBC", get_openssl_blowfish_encryptor_and_padder()[0]))
        # 3DES
        .add_test(CipherBenchmark("OpenSSL 3DES-CBC", get_openssl_3des_encryptor_and_padder()[0]))
        # DES
        .add_test(CipherBenchmark("PyCryptodome DES-CBC", get_pycrypto_des_cipher().encrypt)),
]
benchmark_decryption = [
    # Decryption
    # AES-128
    CipherBenchmarkCategory("AES decryption key 128", lambda: initialize_encrypted_data(get_openssl_aes_encryptor(KEY_128)))
        .add_test(CipherBenchmark("PyCryptodome AES-CTR-128", get_pycrypto_aes_cipher(KEY_128, False).decrypt))
        .add_test(CipherBenchmark("OpenSSL (hwaccel) AES-CTR-128", get_openssl_aes_decryptor(KEY_128))),
    # AES-256
    CipherBenchmarkCategory("AES decryption key 256", lambda: initialize_encrypted_data(get_openssl_aes_encryptor(KEY_256)))
        .add_test(CipherBenchmark("PyCryptodome AES-CTR-256", get_pycrypto_aes_cipher(KEY_256, False).decrypt))
        .add_test(CipherBenchmark("OpenSSL (hwaccel) AES-CTR-256", get_openssl_aes_decryptor(KEY_256))),

    # ChaCha20
    CipherBenchmarkCategory("ChaCha20 decryption", lambda: initialize_encrypted_data(get_openssl_chacha20_encryptor()))
        .add_test(CipherBenchmark("OpenSSL ChaCha20", get_openssl_chacha20_decryptor())),

    # Blowfish
    CipherBenchmarkCategory("Blowfish decryption", lambda: initialize_encrypted_data_hazmat_cbc(get_openssl_blowfish_encryptor_and_padder()))
        .add_test(CipherBenchmark("OpenSSL Blowfish-CBC", get_openssl_blowfish_decryptor_and_unpadder()[0])),

    # 3DES
    CipherBenchmarkCategory("3DES decryption", lambda: initialize_encrypted_data_hazmat_cbc(get_openssl_3des_encryptor_and_padder()))
        .add_test(CipherBenchmark("OpenSSL 3DES-CBC", get_openssl_3des_decryptor_and_unpadder()[0])),

    # DES
    CipherBenchmarkCategory("DES decryption", lambda: initialize_encrypted_data_pycrypto_cbc(get_pycrypto_des_cipher()))
        .add_test(CipherBenchmark("PyCryptodome DES-CBC", get_pycrypto_des_cipher().decrypt)),
]

encryption_results = start_benchmark(benchmark_encryption)
decryption_results = start_benchmark(benchmark_decryption)

plot_benchmark(encryption_results, savefilename="encryption")
plot_benchmark(decryption_results, savefilename="decryption")