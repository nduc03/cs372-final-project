import matplotlib.pyplot as plt
from statistics import mean
import textwrap
import os

def to_MBps(data_size: int, seconds: float | list[float]) -> float | list[float]:
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

        plt.bar(iteration, to_MBps(data_size, result), label=label)

        plt.xlabel("Iteration")
        plt.ylabel("Throughput (MiB/s)")
        plt.title(f"Benchmark: {label} (Data size: {data_size} bytes)")
        plt.legend()
        plt.show()

def plot_benchmark(result: list[tuple[str, int, list[float]]], savefilename: str = None):
    mean_results = [(label, data_size, mean(exec_times)) for label, data_size, exec_times in result]
    mean_throughputs = [(label, data_size, mean(to_MBps(data_size, exec_times))) for label, data_size, exec_times in result]

    labels, _, exec_times = zip(*mean_results)
    _, _, throughput = zip(*mean_throughputs)

    wrapped_labels = ['\n'.join(textwrap.wrap(label, width=12)) for label in labels]

    os.makedirs("plots", exist_ok=True)

    def show_value_on_top_of_bar(bars):
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,  # x position: center of bar
                height,                            # y position: top of bar
                f'{height:.2f}',                      # text to display
                ha='center',                      # horizontal alignment
                va='bottom'                       # vertical alignment
            )

    plt.figure(figsize=(16,9))
    bars = plt.bar(wrapped_labels, exec_times, label="Execution Time (s)")
    show_value_on_top_of_bar(bars)
    plt.xlabel("Cipher Method")
    plt.ylabel("Time (seconds)")
    plt.title("Benchmark Results (Time)")
    plt.legend()
    plt.tight_layout()
    if savefilename:
        plt.savefig("plots/" + savefilename + "_exec_time.png")
    plt.show()

    plt.figure(figsize=(16,9))
    bars = plt.bar(wrapped_labels, throughput, label="Throughput (MiB/s)")
    show_value_on_top_of_bar(bars)
    plt.xlabel("Cipher Method")
    plt.ylabel("Throughput (MiB/s)")
    plt.title("Benchmark Results (Throughput)")
    plt.legend()
    plt.tight_layout()
    if savefilename:
        plt.savefig("plots/" + savefilename + "_throughput.png")
    plt.show()