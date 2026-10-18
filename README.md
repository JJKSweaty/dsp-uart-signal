# DSP UART Signal Lab

Small Python exercises for working with noisy digital signals.

The notebooks start with lists, slices, loops, and functions. Later exercises cover moving averages, median filters, UART frames, and OOK signals. The filter and decoder functions are left as TODOs in the practice notebooks so they can be implemented and tested one at a time.

## Start here

Open these files in VS Code with the Python and Jupyter extensions installed:

- `01_python_for_embedded.ipynb` — Python basics
- `02_noise_and_filters.ipynb` — filter exercises
- `03_noisy_uart.ipynb` — UART decoding
- `04_ook_demodulation.ipynb` — OOK demodulation
- `signal_decoder.ipynb` — a longer decoder exercise

Run notebook cells from top to bottom. The small command-line version can be run with:

```bash
python3 signal_lab.py
python3 -m unittest -v
```

The `Medium_45min_Signal_Mock` folder contains a challenge notebook, a separate solution notebook, and a CSV capture. Open the challenge first.

Everything here uses Python's standard library. `matplotlib` is optional for the plotting cell.
