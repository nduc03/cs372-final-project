import timeit
import log_helper
from typing import Callable
from Crypto.Util.Padding import pad
from Crypto.Cipher._mode_cbc import CbcMode
import logging

logger = log_helper.get_logger(logging.INFO)

TEST_SIZE_MB = 256

def to_MBPS(seconds: float | list[float]) -> float | list[float]:
    if isinstance(seconds, list):
        return [TEST_SIZE_MB / sec for sec in seconds]
    return TEST_SIZE_MB / seconds


class CipherBenchmark:
    def __init__(self, label: str, cipher_method: callable):
        self.label = label
        self.cipher_method = cipher_method

    def benchmark(self, benchmark_data: bytes, repeat: int = 5) -> list[float]:
        logger.info('Benchmarking "%s"...', self.label)
        logger.info("Data size: %d bytes", len(benchmark_data))
        bench_result = timeit.repeat(lambda: self.cipher_method(
            benchmark_data), repeat=repeat, number=1)
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
        """Run all tests in this category.

        Returns: list of test results, each containing (label, data size, list of execution times).
        """
        test_data = self.data_initializer()
        result = []
        for test_case in self.test_cases:
            result.append((test_case.label, len(test_data),
                          test_case.benchmark(test_data)))
        return result


def initialize_data():
    return b"\xff" * int(TEST_SIZE_MB * 1024 * 1024)


def initialize_encrypted_data(encryptor: Callable[[bytes], bytes]):
    return encryptor(b"\xff" * int(TEST_SIZE_MB * 1024 * 1024))


def initialize_encrypted_data_hazmat_cbc(encryptor_getter: tuple[Callable[[bytes], bytes], Callable[[], bytes]]):
    update, finalize = encryptor_getter
    return update(b"\xff" * int(TEST_SIZE_MB * 1024 * 1024)) + finalize()

def initialize_encrypted_data_pycrypto_cbc(pycrypto_cbc_cipher: CbcMode):
    return pycrypto_cbc_cipher.encrypt(pad(b"\xff" * int(TEST_SIZE_MB * 1024 * 1024), pycrypto_cbc_cipher.block_size))