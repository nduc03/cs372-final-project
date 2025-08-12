import logging as _logging
import timeit as _timeit
from typing import Callable as _Callable, _NamedTuple
from Crypto.Util.Padding import pad as _pad
from Crypto.Cipher._mode_cbc import CbcMode as _CbcMode
import log_helper as _log_helper

_logger = _log_helper.get_logger(_logging.INFO)

_TEST_SIZE_MIB = 512
_BYTES_PER_MIB = 1024 * 1024

TimeType = float
class CipherBenchmarkResult(_NamedTuple):
    label: str
    data_size: int
    exec_times: list[TimeType]
    # mem_usages: list[int]

def to_MiBPS(seconds: TimeType | list[TimeType]) -> TimeType | list[TimeType]:
    if isinstance(seconds, list):
        return [_TEST_SIZE_MIB / sec for sec in seconds]
    return _TEST_SIZE_MIB / seconds


class CipherBenchmark:
    def __init__(self, label: str, cipher_method: callable):
        self.label = label
        self.cipher_method = cipher_method

    def benchmark(self, benchmark_data: bytes, repeat: int = 5) -> list[TimeType]:
        _logger.info('Benchmarking "%s"...', self.label)
        _logger.info("Data size: %d bytes", len(benchmark_data))
        bench_result = _timeit.repeat(lambda: self.cipher_method(
            benchmark_data), repeat=repeat, number=1)
        _logger.info('Done benchmarking "%s".', self.label)
        return bench_result


class CipherBenchmarkCategory:
    def __init__(self, name: str, data_initializer: callable):
        self.name = name
        self.data_initializer = data_initializer
        self.test_cases = []

    def add_test(self, test: CipherBenchmark):
        self.test_cases.append(test)
        return self

    def test(self) -> list[CipherBenchmarkResult]:
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
    return b"\xff" * int(_TEST_SIZE_MIB * _BYTES_PER_MIB)


def init_encrypted_data(encryptor: _Callable[[bytes], bytes]):
    return encryptor(b"\xff" * int(_TEST_SIZE_MIB * _BYTES_PER_MIB))


def init_encrypted_data_hazmat_cbc(encryptor_getter: tuple[_Callable[[bytes], bytes], _Callable[[], bytes]]):
    update, finalize = encryptor_getter
    return update(b"\xff" * int(_TEST_SIZE_MIB * _BYTES_PER_MIB)) + finalize()

def init_encrypted_data_pycrypto_cbc(pycrypto_cbc_cipher: _CbcMode):
    return pycrypto_cbc_cipher.encrypt(_pad(b"\xff" * int(_TEST_SIZE_MIB * _BYTES_PER_MIB), pycrypto_cbc_cipher.block_size))