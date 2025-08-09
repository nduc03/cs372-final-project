import timeit
import logging
import log_helper
from aes_test_helper import get_pycrypto_cipher, get_openssl_encryptor, get_openssl_decryptor
from matplotlib_helper import plot_raw_benchmark

# Benchmark in AES 3 categories:
# Full software AES-CTR using PyCryptodome
# AES-NI mode CTR using PyCryptodome (hardware accelerated + Python cross-platform)
# AES-CTR using OpenSSL backend (hardware accelerated + platform optimized)

# TODO: 3DES, DES, ChaCha20, RC2
# TODO: plot results

logger = log_helper.get_logger(logging.INFO)

# define constants
KEY_128 = b"\x00" * 16
KEY_256 = b"\x00" * 32
IV = b"\x00" * 16

# helpers
def to_MBPS(seconds: float | list[float]) -> float | list[float]:
    if isinstance(seconds, list):
        return [1024 / sec for sec in seconds]
    return 1024 / seconds

class CipherBenchmark:
    def __init__(self, label: str, cipher_method: callable):
        self.label = label
        self.cipher_method = cipher_method

    def benchmark(self, benchmark_data: bytes, repeat: int = 5) -> list[float]:
        logger.info('Benchmarking "%s"...', self.label)
        logger.info("Data size: %d bytes", len(benchmark_data))
        bench_result = timeit.repeat(lambda: self.cipher_method(benchmark_data), repeat=repeat, number=1)
        logger.info('Done benchmarking "%s".', self.label)
        return bench_result

class CipherBenchmarkCategory:
    def __init__(self, name: str, data_initializer: callable):
        self.name = name
        self.data_initializer = data_initializer
        self.test_cases = []

    def add_test(self, test: CipherBenchmark):
        self.test_cases.append(test)
        return self

    def test(self) -> list[tuple[str, int, list[float]]]:
        test_data = self.data_initializer()
        result = []
        for test_case in self.test_cases:
            result.append((test_case.label, len(test_data), test_case.benchmark(test_data)))
        return result

def initialize_data():
    return b"\xff" * (1024 * 1024 * 1024)


def initialize_encrypted_data(encrypt_method):
    return encrypt_method(b"\xff" * (1024 * 1024 * 1024))

# benchmark
benchmark_list = [
    CipherBenchmarkCategory("AES encryption", initialize_data)
        # .add_test(CipherBenchmark("Software AES 128 encryption", get_pycrypto_cipher(KEY_128, IV, False).encrypt))
        # .add_test(CipherBenchmark("Software AES 256 encryption", get_pycrypto_cipher(KEY_256, IV, False).encrypt))
        # .add_test(CipherBenchmark("AES-NI 128 encryption", get_pycrypto_cipher(KEY_128, IV, True).encrypt))
        # .add_test(CipherBenchmark("AES-NI 256 encryption", get_pycrypto_cipher(KEY_256, IV, True).encrypt))
        .add_test(CipherBenchmark("OpenSSL AES 128 encryption", get_openssl_encryptor(KEY_128, IV)))
        .add_test(CipherBenchmark("OpenSSL AES 256 encryption", get_openssl_encryptor(KEY_256, IV))),
    # CipherBenchmarkCategory("AES decryption key 128", lambda: initialize_encrypted_data(get_openssl_encryptor(KEY_128, IV)))
    #     .add_test(CipherBenchmark("Software AES 128 decryption", get_pycrypto_cipher(KEY_128, IV, False).decrypt))
    #     .add_test(CipherBenchmark("AES-NI 128 decryption", get_pycrypto_cipher(KEY_128, IV, True).decrypt))
    #     .add_test(CipherBenchmark("OpenSSL AES 128 decryption", get_openssl_decryptor(KEY_128, IV))),
    # CipherBenchmarkCategory("AES decryption key 256", lambda: initialize_encrypted_data(get_openssl_encryptor(KEY_256, IV)))
    #     .add_test(CipherBenchmark("Software AES 256 decryption", get_pycrypto_cipher(KEY_256, IV, False).decrypt))
    #     .add_test(CipherBenchmark("AES-NI 256 decryption", get_pycrypto_cipher(KEY_256, IV, True).decrypt))
    #     .add_test(CipherBenchmark("OpenSSL AES 256 decryption", get_openssl_decryptor(KEY_256, IV))),
]

for category in benchmark_list:
    print(f"Benchmarking category: {category.name}")
    category_results = category.test()
    print("-" * 80)
    print("\nPreview results:")
    for label, data_size, result in category_results:
        rounded_result = [round(r, 2) for r in result]
        rounded_result_throughput = [round(r, 2) for r in to_MBPS(result)]
        print(f"{label} ({data_size / 1024 / 1024} MB) execution time (seconds): {rounded_result}")
        print(f"{label} ({data_size / 1024 / 1024} MB) throughput (MB/s): {rounded_result_throughput}")
    print("\n")
    print("-" * 80)

    plot_raw_benchmark(category_results)
