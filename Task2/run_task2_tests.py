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

from dsp_operations import AccumulationSignal,SquaringSignal,NormalizeSignal,SubSignals
from Task1Test import  SignalSamplesAreEqual

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

    try:

        # -----------------------------------------------------------
        #                        TASK 2 TESTS
        # -----------------------------------------------------------
        
        # 1. Testing Subtraction
        print("\nTesting Subtraction (Signal1 - Signal2):")
        ind1, val1 = ReadSignalFileM('../Task1/input/Signal1.txt')
        ind2, val2 = ReadSignalFileM('../Task1/input/Signal2.txt')
        ind_sub, val_sub = SubSignals([(ind1, val1), (ind2, val2)])
  
        SignalSamplesAreEqual("Subtraction", "./OUTPUT Arithmetic operations/signal1-signal2.txt", ind_sub, val_sub)
        print("-----------------------------------------------------------")

        print("\nTesting Subtraction (Signal1 - Signal3):")
        ind1, val1 = ReadSignalFileM('../Task1/input/Signal1.txt')
        ind2, val2 = ReadSignalFileM('../Task1/input/Signal3.txt')
        ind_sub, val_sub = SubSignals([(ind1, val1), (ind2, val2)])
    
        SignalSamplesAreEqual("Subtraction", "./OUTPUT Arithmetic operations/signal1-signal3.txt", ind_sub, val_sub)
        print("-----------------------------------------------------------")


        # 2. Testing Squaring
        print("\nTesting Squaring for Signal1:")
        ind_sq, val_sq = ReadSignalFileM('../Task1/input/Signal1.txt')
        val_squared = SquaringSignal(val_sq)
       
        SignalSamplesAreEqual("Squaring", "./OUTPUT Arithmetic operations/Output squaring signal 1.txt", ind_sq, val_squared)
        print("-----------------------------------------------------------")

        # 3. Testing Normalization (0 to 1)
        print("\nTesting Normalization (0 to 1) for Signal2:")
        ind_n1, val_n1 = ReadSignalFileM('../Task1/input/Signal2.txt')
        val_norm1 = NormalizeSignal(val_n1, "0_to_1")
  
        SignalSamplesAreEqual("Normalization (0 to 1)", "./OUTPUT Arithmetic operations/normlize signal 2 (from 0 to 1 )-- output.txt", ind_n1, val_norm1)
        print("-----------------------------------------------------------")

        # 4. Testing Normalization (-1 to 1)
        print("\nTesting Normalization (-1 to 1) for Signal1:")
        ind_n2, val_n2 = ReadSignalFileM('../Task1/input/Signal1.txt')
        val_norm2 = NormalizeSignal(val_n2, "-1_to_1")

        SignalSamplesAreEqual("Normalization (-1 to 1)", "./OUTPUT Arithmetic operations/normalize of signal 1 (from -1 to 1)-- output.txt", ind_n2, val_norm2)
        print("-----------------------------------------------------------")

        # 5. Testing Accumulation
        print("\nTesting Accumulation for Signal1:")
        ind_acc, val_acc = ReadSignalFileM('../Task1/input/Signal1.txt')
        val_accumulated = AccumulationSignal(val_acc)
  
        SignalSamplesAreEqual("Accumulation", "./OUTPUT Arithmetic operations/output accumulation for signal1.txt", ind_acc, val_accumulated)
        print("-----------------------------------------------------------")

    except FileNotFoundError as e:
        print(f"File Error: {e}")
        print("Test skipped: Make sure the './input/' and './output/' folders exist and have the correct files.")
    except Exception as e:
        print(f"An error occurred during testing: {e}")

if __name__ == "__main__":
    run_quantization_tests()
    
