import matplotlib.pyplot as plt

def to_MBPS(data_size: int, seconds: float | list[float]) -> float | list[float]:
    data_size_MB = data_size / (1024 * 1024)
    if isinstance(seconds, list):
        return [data_size_MB / sec for sec in seconds]
    return data_size_MB / seconds

def plot_raw_benchmark(category_results: list[tuple[str, int, list[float]]]):
    for label, data_size, result in category_results:
        iteration = range(len(result))
        plt.bar(iteration, result, label=label)

        plt.xlabel("Iteration")
        plt.ylabel("Time (seconds)")
        plt.title(f"Benchmark: {label} (Data size: {data_size} bytes)")
        plt.legend()
        plt.show()

        plt.bar(iteration, to_MBPS(data_size, result), label=label)

        plt.xlabel("Iteration")
        plt.ylabel("Throughput (MB/s)")
        plt.title(f"Benchmark: {label} (Data size: {data_size} bytes)")
        plt.legend()
        plt.show()
