import os
import textwrap
from statistics import mean
import matplotlib.pyplot as plt
from benchmark_helper import CipherBenchmarkResult, _TEST_SIZE_MIB

def _to_MiBps(data_size: int, seconds: float | list[float]) -> float | list[float]:
    data_size_MiB = data_size / (1024 * 1024)
    if isinstance(seconds, list):
        return [data_size_MiB / sec for sec in seconds]
    return data_size_MiB / seconds

def _show_value_on_top_of_bar(ax, bars):
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f'{height:.2f}',
            ha='center',
            va='bottom'
        )

def plot_raw_benchmark(results: list[CipherBenchmarkResult]):
    os.makedirs("raw-plots", exist_ok=True)

    for label, data_size, result in results:
        iteration = range(len(result))

        plt.figure(figsize=(8, 4))
        bars = plt.bar(iteration, result, label=label)

        plt.xlabel("Iteration")
        plt.ylabel("Time (seconds)")
        plt.title(f"Benchmark: {label} (Data size: {data_size} bytes)")
        _show_value_on_top_of_bar(plt, bars)
        plt.tight_layout()
        plt.savefig(f"raw-plots/{label.replace(' ', '_')}_raw_time.png")

def plot_benchmark(result: list[CipherBenchmarkResult], category: str):
    # Calculate the mean execution time for each CipherBenchmarkResult
    mean_results = [(label, data_size, mean(exec_times)) for label, data_size, exec_times in result]
    # Calculate the mean throughput (in MiB/s) for each CipherBenchmarkResult
    mean_throughputs = [(label, data_size, mean(_to_MiBps(data_size, exec_times))) for label, data_size, exec_times in result]

     # Sort results by execution time in ascending order (fastest first)
    mean_results.sort(key=lambda x: x[2])
    labels, _, exec_times = zip(*mean_results) # Separate into individual lists

    # Sort throughput results in descending order (highest first)
    mean_throughputs.sort(key=lambda x: x[2], reverse=True)
    labels_tp, _, throughput = zip(*mean_throughputs) # Separate into individual lists

    # Wrap long labels into multiple lines
    wrapped_labels = ['\n'.join(textwrap.wrap(label, width=12)) for label in labels]
    wrapped_labels_tp = ['\n'.join(textwrap.wrap(label, width=12)) for label in labels_tp]

    os.makedirs("overall-plots", exist_ok=True)

    # --- Plot execution time ---
    plt.figure(figsize=(16,9))
    bars = plt.bar(wrapped_labels, exec_times, label="Execution Time (s)")
    _show_value_on_top_of_bar(plt, bars)
    plt.xlabel("Cipher Method")
    plt.ylabel("Time (seconds)")
    plt.title(f"{category} time of {_TEST_SIZE_MIB} MiB [Lower is better]")
    plt.legend()
    plt.tight_layout()
    plt.savefig("overall-plots/" + category + "_exec_time.png")

    # --- Plot throughput ---
    plt.figure(figsize=(16,9))
    bars = plt.bar(wrapped_labels_tp, throughput, label="Throughput (MiB/s)")
    _show_value_on_top_of_bar(plt, bars)
    plt.xlabel("Cipher Method")
    plt.ylabel("Throughput (MiB/s)")
    plt.title(f"{category} throughput [Higher is better]")
    plt.legend()
    plt.tight_layout()
    plt.savefig("overall-plots/" + category + "_throughput.png")


def plot_side_by_side_benchmark(encrypt_result: CipherBenchmarkResult, decrypt_result: CipherBenchmarkResult):
    os.makedirs("side-by-side-plots", exist_ok=True)

    labels = ["Encrypt", "Decrypt"]
    mean_time = [mean(encrypt_result.list_exec_time_second), mean(decrypt_result.list_exec_time_second)]
    mean_throughput = [
        mean(_to_MiBps(encrypt_result.data_size, encrypt_result.list_exec_time_second)),
        mean(_to_MiBps(decrypt_result.data_size, decrypt_result.list_exec_time_second))
    ]
    _, axes = plt.subplots(1, 2, figsize=(12, 6))
    # Plot execution time
    time_bars = axes[0].bar(labels, mean_time, color='skyblue')
    axes[0].set_title(f'{encrypt_result.label} Time of {_TEST_SIZE_MIB} MiB data')
    axes[0].set_ylabel('Time (s)')

    _show_value_on_top_of_bar(axes[0], time_bars)

    # plot throughput
    throughput_bars = axes[1].bar(labels, mean_throughput, color='lightgreen')
    axes[1].set_title(f'{encrypt_result.label} Throughput')
    axes[1].set_ylabel('Throughput (MiB/s)')

    _show_value_on_top_of_bar(axes[1], throughput_bars)

    plt.tight_layout()
    plt.savefig(f"side-by-side-plots/{encrypt_result.label.replace(' ', '_')}_encrypt_and_decrypt.png")
