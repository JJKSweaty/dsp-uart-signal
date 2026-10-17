# DSP UART Signal Lab

A small Python playground for learning signal processing with noisy digital captures.

The examples are intentionally plain: write a few lines, run the tests, and inspect what changed. It starts with simple list operations and builds toward moving averages, median filters, UART decoding, and on-off keying.

## Run it

```bash
python3 signal_lab.py
python3 -m unittest -v
```

Open `signal_lab.py` in VS Code and use it as the exercise file. The functions are kept small so you can replace an implementation, add print statements, or make a new test without setting up a framework.

## What is included

- Moving-average and exponential filters
- Median and high-pass difference filters
- Fixed-width bit decoding
- Center-sampled UART decoding
- OOK bit decoding
- Synthetic captures for `b"Hi!"` and `101100101011`

The project uses only the Python standard library. There is no service, account, or setup beyond Python 3.
