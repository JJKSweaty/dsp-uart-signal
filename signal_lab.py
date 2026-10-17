"""Small signal-processing exercises for Python practice."""

from __future__ import annotations

from statistics import median
from typing import Iterable, Sequence


def moving_average(samples: Sequence[float], window: int = 3) -> list[float]:
    """Return a causal moving average with a short warm-up at the start."""
    if window < 1:
        raise ValueError("window must be at least 1")

    filtered: list[float] = []
    for index in range(len(samples)):
        start = max(0, index - window + 1)
        section = samples[start : index + 1]
        filtered.append(sum(section) / len(section))
    return filtered


def exponential_filter(samples: Sequence[float], alpha: float = 0.25) -> list[float]:
    """Return an exponential moving average."""
    if not 0 < alpha <= 1:
        raise ValueError("alpha must be greater than 0 and at most 1")
    if not samples:
        return []

    filtered = [float(samples[0])]
    for sample in samples[1:]:
        previous = filtered[-1]
        filtered.append(alpha * sample + (1 - alpha) * previous)
    return filtered


def median_filter(samples: Sequence[float], window: int = 3) -> list[float]:
    """Replace each sample with the median of its local neighborhood."""
    if window < 1 or window % 2 == 0:
        raise ValueError("window must be a positive odd number")

    radius = window // 2
    filtered: list[float] = []
    for index in range(len(samples)):
        start = max(0, index - radius)
        end = min(len(samples), index + radius + 1)
        filtered.append(float(median(samples[start:end])))
    return filtered


def high_pass_difference(samples: Sequence[float]) -> list[float]:
    """Highlight changes between neighboring samples."""
    if not samples:
        return []
    return [0.0] + [samples[index] - samples[index - 1] for index in range(1, len(samples))]


def decode_grouped_bits(samples: Sequence[float], samples_per_bit: int, threshold: float = 0.5) -> str:
    """Average fixed-size sample groups and turn them into 0/1 bits."""
    if samples_per_bit < 1:
        raise ValueError("samples_per_bit must be at least 1")

    bits: list[str] = []
    for start in range(0, len(samples) - samples_per_bit + 1, samples_per_bit):
        group = samples[start : start + samples_per_bit]
        average = sum(group) / len(group)
        bits.append("1" if average >= threshold else "0")
    return "".join(bits)


def decode_uart(samples: Sequence[float], samples_per_bit: int, threshold: float = 0.5) -> bytes:
    """Decode idle-high, 8-N-1 UART frames using center sampling."""
    if samples_per_bit < 1:
        raise ValueError("samples_per_bit must be at least 1")

    levels = [sample >= threshold for sample in samples]
    decoded = bytearray()
    index = 0
    frame_length = 10 * samples_per_bit

    while index + frame_length <= len(levels):
        if levels[index]:
            index += 1
            continue

        centers = [index + int((bit + 0.5) * samples_per_bit) for bit in range(10)]
        if centers[-1] >= len(levels):
            break
        data_bits = [levels[centers[bit]] for bit in range(1, 9)]
        stop_bit = levels[centers[9]]
        if stop_bit:
            value = sum((1 << bit) for bit, is_high in enumerate(data_bits) if is_high)
            decoded.append(value)
            index += frame_length
        else:
            index += samples_per_bit
    return bytes(decoded)


def decode_ook(samples: Sequence[float], samples_per_bit: int, threshold: float = 0.5) -> str:
    """Decode an on-off keyed signal by sampling each bit center."""
    if samples_per_bit < 1:
        raise ValueError("samples_per_bit must be at least 1")
    bits: list[str] = []
    for start in range(0, len(samples) - samples_per_bit + 1, samples_per_bit):
        center = start + samples_per_bit // 2
        bits.append("1" if samples[center] >= threshold else "0")
    return "".join(bits)


def repeat_bits(bits: Iterable[int | str], samples_per_bit: int) -> list[float]:
    """Make an ideal sample capture from a sequence of bit values."""
    if samples_per_bit < 1:
        raise ValueError("samples_per_bit must be at least 1")
    return [float(bit) for bit in bits for _ in range(samples_per_bit)]


def uart_capture(text: bytes, samples_per_bit: int = 4) -> list[float]:
    """Make a simple idle-high UART capture for experiments."""
    bits: list[int] = [1] * samples_per_bit
    for value in text:
        frame = [0] + [(value >> bit) & 1 for bit in range(8)] + [1]
        bits.extend(repeat_bits(frame, samples_per_bit))
    bits.extend([1] * samples_per_bit)
    return [sample + (0.08 if index % 7 == 0 else 0) for index, sample in enumerate(bits)]


def main() -> None:
    """Run a small end-to-end example from the terminal."""
    uart_samples = uart_capture(b"Hi!")
    print("UART:", decode_uart(uart_samples, samples_per_bit=4))

    ook_bits = "101100101011"
    ook_samples = repeat_bits(ook_bits, samples_per_bit=4)
    print("OOK :", decode_ook(ook_samples, samples_per_bit=4))

    noisy = [0.0, 1.0, 0.0, 1.0, 8.0, 1.0, 0.0]
    print("Median filter:", median_filter(noisy))


if __name__ == "__main__":
    main()
