"""Run Task 2 checks from the Task2 directory.

Command:
    python run_task2_tests.py

Quantization tests use the TA-provided input/output files. Arithmetic reference
tests run when the sibling Task1 input files and Task2 output files are present.
"""
from pathlib import Path
import math

from dsp_operations import (
    ReadSignalFileM, SubSignals, SquaringSignal, NormalizeSignal,
    AccumulationSignal, Quantization
)
from Quantization.QuanTest1 import QuantizationTest1
from Quantization.QuanTest2 import QuantizationTest2

ROOT = Path(__file__).resolve().parent
QUANT = ROOT / "Quantization"
ARITH_OUT = ROOT / "OUTPUT Arithmetic operations"
TASK1_INPUT = ROOT.parent / "Task1" / "input"


def run_quantization_tests():
    print("\n=== Quantization Test 1: 3 bits ===")
    _, samples1 = ReadSignalFileM(str(QUANT / "Quan1_input.txt"))
    _, encoded1, quantized1, _ = Quantization(samples1, num_bits=3)
    QuantizationTest1(str(QUANT / "Quan1_Out.txt"), encoded1, quantized1)

    print("\n=== Quantization Test 2: 4 levels ===")
    _, samples2 = ReadSignalFileM(str(QUANT / "Quan2_input.txt"))
    intervals2, encoded2, quantized2, errors2 = Quantization(samples2, num_levels=4)
    QuantizationTest2(
        str(QUANT / "Quan2_Out.txt"),
        intervals2, encoded2, quantized2, errors2
    )


def read_reference(path):
    indices, samples = [], []
    with open(path, "r", encoding="utf-8") as file:
        for _ in range(3):
            next(file, None)
        for line in file:
            parts = line.split()
            if len(parts) != 2:
                continue
            try:
                indices.append(int(parts[0]))
                samples.append(float(parts[1]))
            except ValueError:
                continue
    return indices, samples


def compare_signal(label, expected_path, indices, samples):
    if not expected_path.exists():
        print(f"SKIPPED {label}: reference file not found: {expected_path}")
        return

    expected_indices, expected_samples = read_reference(expected_path)

    print(f"\nChecking: {label}")
    print(f"Your samples count: {len(samples)}")
    print(f"Expected samples count: {len(expected_samples)}")

    if indices != expected_indices:
        print("FAILED: Indices are different.")
        print("Your first indices:", indices[:5])
        print("Expected first indices:", expected_indices[:5])
        return

    if len(samples) != len(expected_samples):
        print("FAILED: Different signal lengths.")
        return

    for i, (actual, expected) in enumerate(zip(samples, expected_samples)):
        if abs(actual - expected) >= 0.01:
            print(f"First mismatch at sample {i}:")
            print(f"Your value:     {actual}")
            print(f"Expected value: {expected}")
            print(f"Absolute difference: {abs(actual - expected)}")
            print("Your first 10 samples:", samples[:10])
            print("Expected first 10 samples:", expected_samples[:10])
            print("Expected absolute subtraction at this sample:",
                  abs(actual))
            return

    print(f"PASSED {label}")


def run_arithmetic_tests_if_available():
    signal1 = TASK1_INPUT / "Signal1.txt"
    signal2 = TASK1_INPUT / "Signal2.txt"
    signal3 = TASK1_INPUT / "Signal3.txt"

    if not all(p.exists() for p in (signal1, signal2, signal3)):
        print("\nArithmetic reference tests skipped: expected Task1/input/Signal1.txt, Signal2.txt and Signal3.txt were not found.")
        print("This does not affect the Quantization tests above.")
        return

    idx1, val1 = ReadSignalFileM(str(signal1))
    idx2, val2 = ReadSignalFileM(str(signal2))
    idx3, val3 = ReadSignalFileM(str(signal3))

    compare_signal(
        "Subtraction Signal1 - Signal2",
        ARITH_OUT / "signal1-signal2.txt",
        *SubSignals([(idx1, val1), (idx2, val2)])
    )
    compare_signal(
        "Subtraction Signal1 - Signal3",
        ARITH_OUT / "signal1-signal3.txt",
        *SubSignals([(idx1, val1), (idx3, val3)])
    )

    compare_signal(
        "Squaring Signal1",
        ARITH_OUT / "Output squaring signal 1.txt",
        idx1, SquaringSignal(val1)
    )
    compare_signal(
        "Normalization Signal2 (0 to 1)",
        ARITH_OUT / "normlize signal 2 (from 0 to 1 )-- output.txt",
        idx2, NormalizeSignal(val2, "0_to_1")
    )
    compare_signal(
        "Normalization Signal1 (-1 to 1)",
        ARITH_OUT / "normalize of signal 1 (from -1 to 1)-- output.txt",
        idx1, NormalizeSignal(val1, "-1_to_1")
    )
    compare_signal(
        "Accumulation Signal1",
        ARITH_OUT / "output accumulation for signal1.txt",
        idx1, AccumulationSignal(val1)
    )


if __name__ == "__main__":
    run_quantization_tests()
    run_arithmetic_tests_if_available()
