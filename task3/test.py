import math
import os

from dsp_operations import (
    ReadSignalFileM, ReadFrequencyFile, Transform,
    GetAmplitudes, GetPhases, FromPolar, RemoveDC,
)
from signalcompare import SignalComapreAmplitude, SignalComaprePhaseShift
from CompareSignals import SignalsAreEqual


def exists(*paths):
    for p in paths:
        if not os.path.exists(p):
            print(f"  Skipped, file not found: {p}")
            return False
    return True


def idft_real(amps, phases):
    X = FromPolar(amps, phases)
    return [v.real for v in Transform(X, inverse=True)]


# ---------------------------------------------------------
# 1) DFT: time signal -> expected (amplitude, phase) file
# ---------------------------------------------------------
def test_dft(name, input_file, expected_file):
    print(f"\n{name}")
    if not exists(input_file, expected_file):
        return

    _, samples = ReadSignalFileM(input_file)
    X = Transform(samples)
    amps, phases = GetAmplitudes(X), GetPhases(X)
    print("Your amplitudes:", amps)
   
    exp_amps, exp_phases = ReadFrequencyFile(expected_file)
    print("Expected amplitudes:", exp_amps) 
    # Phase of a ~zero component is meaningless: ignore it in the comparison
    my_ph, ex_ph = [], []
    for a, p, ea, ep in zip(amps, phases, exp_amps, exp_phases):
        if ea < 0.01:
            my_ph.append(0.0)
            ex_ph.append(0.0)
        else:
            my_ph.append(p)
            ex_ph.append(ep)

            
    amps_test = [round(a, 10) for a in amps]
    exp_amps_test = [round(a, 10) for a in exp_amps]
    print("  Amplitude:", "PASSED" if SignalComapreAmplitude(amps_test, exp_amps_test) else "FAILED")
    print("  Phase    :", "PASSED" if SignalComaprePhaseShift(my_ph, ex_ph) else "FAILED")


# ---------------------------------------------------------
# 2) IDFT: (amplitude, phase) file -> expected time signal
# ---------------------------------------------------------
def test_idft(name, freq_file, expected_time_file):
    print(f"\n{name}")
    if not exists(freq_file, expected_time_file):
        return
    amps, phases = ReadFrequencyFile(freq_file)
    samples = idft_real(amps, phases)
    SignalsAreEqual(name, expected_time_file, list(range(len(samples))), samples)

# ---------------------------------------------------------
# 3) Remove DC: time signal -> DFT -> F(0)=0 -> IDFT
# ---------------------------------------------------------
def test_remove_dc(name, input_file, expected_time_file):
    print(f"\n{name}")
    if not exists(input_file, expected_time_file):
        return

    indices, samples = ReadSignalFileM(input_file)
    X = RemoveDC(Transform(samples))
    result = [v.real for v in Transform(X, inverse=True)]
    SignalsAreEqual(name, expected_time_file, indices, result)


# ---------------------------------------------------------
# 4) Round trip: DFT then IDFT must return the original signal
# ---------------------------------------------------------
def test_round_trip(name, input_file):
    print(f"\n{name}")
    if not exists(input_file):
        return

    indices, samples = ReadSignalFileM(input_file)
    X = Transform(samples)
    back = [v.real for v in Transform(X, inverse=True)]
    ok = SignalComapreAmplitude(samples, back, tol=1e-6)
    print("  Round trip:", "PASSED" if ok else "FAILED")


if __name__ == "__main__":
    # >>> Change these paths to your real files <<<
    test_dft("DFT test",
             "./Test Cases/DFT/input_Signal_DFT.txt",
             "./Test Cases/DFT/Output_Signal_DFT_A,Phase.txt")

    test_idft("IDFT test",
              "./Test Cases/IDFT/Input_Signal_IDFT_A,Phase.txt",
              "./Test Cases/IDFT/Output_Signal_IDFT.txt")

    test_remove_dc("Remove DC test",
                   "./DC_component_input.txt",
                   "./DC_component_output.txt")

    # test_round_trip("Round trip test", "../Task1/input/Signal1.txt")