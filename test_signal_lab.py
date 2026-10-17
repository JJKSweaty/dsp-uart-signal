import unittest

from signal_lab import (
    decode_grouped_bits,
    decode_ook,
    decode_uart,
    exponential_filter,
    high_pass_difference,
    median_filter,
    moving_average,
    repeat_bits,
    uart_capture,
)


class SignalLabTests(unittest.TestCase):
    def test_moving_average(self) -> None:
        self.assertEqual(moving_average([0, 2, 4, 6], window=2), [0.0, 1.0, 3.0, 5.0])

    def test_exponential_filter(self) -> None:
        self.assertEqual(exponential_filter([0, 10, 10], alpha=0.5), [0.0, 5.0, 7.5])

    def test_median_filter_removes_impulse(self) -> None:
        self.assertEqual(median_filter([0, 1, 8, 1, 0]), [0.5, 1.0, 1.0, 1.0, 0.5])

    def test_high_pass_difference(self) -> None:
        self.assertEqual(high_pass_difference([2, 5, 1]), [0.0, 3, -4])

    def test_grouped_bits(self) -> None:
        samples = repeat_bits("1011", samples_per_bit=3)
        self.assertEqual(decode_grouped_bits(samples, samples_per_bit=3), "1011")

    def test_uart_capture_decodes_hi(self) -> None:
        self.assertEqual(decode_uart(uart_capture(b"Hi!"), samples_per_bit=4), b"Hi!")

    def test_ook_capture_decodes_expected_bits(self) -> None:
        samples = repeat_bits("101100101011", samples_per_bit=4)
        self.assertEqual(decode_ook(samples, samples_per_bit=4), "101100101011")


if __name__ == "__main__":
    unittest.main()
