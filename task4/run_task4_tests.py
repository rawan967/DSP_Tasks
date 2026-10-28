"""Run all Task 4 test cases (Moving Average, Derivatives, Convolution, Shifting & Folding, Remove DC)."""
import io
import os
import sys
from contextlib import redirect_stdout

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from CompareSignals import SignalsAreEqual
from dsp_operations import (
    ReadSignalFileM,
    MovingAverage,
    ShiftSignal,
    FoldSignal,
    ShiftFoldedSignal,
    RemoveDCTime,
    ConvolveSignals,
)

sys.path.insert(0, os.path.join(BASE_DIR, "TestCases", "Convolution"))
sys.path.insert(0, os.path.join(BASE_DIR, "TestCases", "Derivative Updated"))
sys.path.insert(0, os.path.join(BASE_DIR, "TestCases", "Shifting and Folding"))

from ConvTest import ConvTest
from DerivativeSignal import DerivativeSignal
from Shift_Fold_Signal import Shift_Fold_Signal


def run_all_tests():
    buf = io.StringIO()
    with redirect_stdout(buf):
        print("=== 1) Moving Average (Smoothing) ===")
        sig1_path = os.path.join(BASE_DIR, "..", "Task1", "input", "Signal1.txt")
        sig2_path = os.path.join(BASE_DIR, "..", "Task1", "input", "Signal2.txt")
        idx1, s1 = ReadSignalFileM(sig1_path)
        idx2, s2 = ReadSignalFileM(sig2_path)

        ma1_idx, ma1_s = MovingAverage(idx1, s1, 3)
        SignalsAreEqual(
            "Moving Average (M=3)",
            os.path.join(BASE_DIR, "TestCases", "Moving Average", "OutMovAvgTest1.txt"),
            ma1_idx,
            ma1_s,
        )

        ma2_idx, ma2_s = MovingAverage(idx2, s2, 5)
        SignalsAreEqual(
            "Moving Average (M=5)",
            os.path.join(BASE_DIR, "TestCases", "Moving Average", "OutMovAvgTest2.txt"),
            ma2_idx,
            ma2_s,
        )

        print("\n=== 2) Sharpening (First & Second Derivatives) ===")
        DerivativeSignal()

        print("\n=== 3) Convolution ===")
        c_idx1, c_s1 = ReadSignalFileM(
            os.path.join(BASE_DIR, "TestCases", "Convolution", "Input_conv_Sig1.txt")
        )
        c_idx2, c_s2 = ReadSignalFileM(
            os.path.join(BASE_DIR, "TestCases", "Convolution", "Input_conv_Sig2.txt")
        )
        conv_idx, conv_s = ConvolveSignals(c_idx1, c_s1, c_idx2, c_s2)
        ConvTest(conv_idx, conv_s)

        print("\n=== 4) Shifting and Folding ===")
        f_idx, f_s = ReadSignalFileM(
            os.path.join(BASE_DIR, "TestCases", "Shifting and Folding", "input_fold.txt")
        )
        fold_idx, fold_s = FoldSignal(f_idx, f_s)
        Shift_Fold_Signal(
            os.path.join(BASE_DIR, "TestCases", "Shifting and Folding", "Output_fold.txt"),
            fold_idx,
            fold_s,
        )

        sf_pos_idx, sf_pos_s = ShiftFoldedSignal(f_idx, f_s, 500, "delay")
        Shift_Fold_Signal(
            os.path.join(BASE_DIR, "TestCases", "Shifting and Folding", "Output_ShifFoldedby500.txt"),
            sf_pos_idx,
            sf_pos_s,
        )

        sf_neg_idx, sf_neg_s = ShiftFoldedSignal(f_idx, f_s, 500, "advance")
        Shift_Fold_Signal(
            os.path.join(BASE_DIR, "TestCases", "Shifting and Folding", "Output_ShiftFoldedby-500.txt"),
            sf_neg_idx,
            sf_neg_s,
        )

        print("\n=== 5) Remove DC Component (Time Domain) ===")
        dc_in = os.path.join(BASE_DIR, "..", "task3", "DC_component_input.txt")
        dc_out = os.path.join(BASE_DIR, "..", "task3", "DC_component_output.txt")
        dc_idx, dc_s = ReadSignalFileM(dc_in)
        rm_idx, rm_s = RemoveDCTime(dc_idx, dc_s)
        SignalsAreEqual("Remove DC (Time Domain)", dc_out, rm_idx, rm_s)

    return buf.getvalue()


if __name__ == "__main__":
    print(run_all_tests())
