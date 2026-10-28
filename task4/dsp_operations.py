"""Task 4 - Time Domain operations.

A signal = (indices, samples): two python lists (indices are ints).
All functions return NEW lists (the input is never modified).
"""
import os


# ---------------------------------------------------------------- file I/O
def ReadSignalFileM(file_path):
    """Read a signal file: 3 header lines (SignalType, IsPeriodic, N) then 'index value' lines."""
    indices, samples = [], []
    with open(file_path, "r") as f:
        lines = f.read().splitlines()
    for line in lines[3:]:
        parts = line.replace(",", " ").split()
        if len(parts) >= 2:
            indices.append(int(float(parts[0])))
            samples.append(float(parts[1]))
    return indices, samples


def WriteSignalFile(file_path, indices, samples):
    """Save a signal in the same format the test cases use."""
    with open(file_path, "w") as f:
        f.write("0\n0\n%d\n" % len(indices))
        for i, v in zip(indices, samples):
            f.write("%d %f\n" % (i, v))


# ------------------------------------------------------- 1) Smoothing
def MovingAverage(indices, samples, M):
    """y(n) = (1/M) * sum_{k=0}^{M-1} x(n+k)   -> N-M+1 output samples.
    (Matches the test files: window starts at the current sample.)"""
    M = int(M)
    N = len(samples)
    if M < 1:
        raise ValueError("Number of points must be >= 1")
    if M > N:
        raise ValueError("Number of points (%d) is bigger than the signal length (%d)" % (M, N))
    out_idx, out = [], []
    for i in range(N - M + 1):
        out_idx.append(indices[i])
        out.append(sum(samples[i:i + M]) / M)
    return out_idx, out


# ------------------------------------------------------- 2) Sharpening
def FirstDerivative(indices, samples):
    """y(n) = x(n) - x(n-1)      -> N-1 samples (starts at the 2nd sample)."""
    out_idx = [indices[i] for i in range(1, len(samples))]
    out = [samples[i] - samples[i - 1] for i in range(1, len(samples))]
    return out_idx, out


def SecondDerivative(indices, samples):
    """y(n) = x(n+1) - 2x(n) + x(n-1)   -> N-2 samples."""
    out_idx = [indices[i] for i in range(1, len(samples) - 1)]
    out = [samples[i + 1] - 2 * samples[i] + samples[i - 1] for i in range(1, len(samples) - 1)]
    return out_idx, out


# --------------------------------------------- 3) Delay / advance by k
def ShiftSignal(indices, samples, k, direction="delay"):
    """delay:   y(n) = x(n-k)  -> indices + k
       advance: y(n) = x(n+k)  -> indices - k"""
    k = int(k)
    if direction not in ("delay", "advance"):
        raise ValueError("direction must be 'delay' or 'advance'")
    shift = k if direction == "delay" else -k
    return [i + shift for i in indices], list(samples)


# ------------------------------------------------------- 4) Folding
def FoldSignal(indices, samples):
    """y(n) = x(-n)"""
    return [-i for i in reversed(indices)], list(reversed(samples))


# ------------------------------------- 5) Delay / advance folded signal
def ShiftFoldedSignal(indices, samples, k, direction="delay"):
    """Fold first, then delay (y(n)=x(-(n-k))) or advance (y(n)=x(-(n+k)))."""
    f_idx, f_s = FoldSignal(indices, samples)
    return ShiftSignal(f_idx, f_s, k, direction)


# ------------------------------------------ 6) Remove DC (time domain)
def RemoveDCTime(indices, samples):
    """y(n) = x(n) - mean(x)"""
    mean = sum(samples) / len(samples)
    return list(indices), [s - mean for s in samples]


# ------------------------------------------- (extra) used by the test runner
def ConvolveSignals(idx1, s1, idx2, s2):
    """Linear convolution; output starts at idx1[0] + idx2[0]."""
    n_out = len(s1) + len(s2) - 1
    out = [0.0] * n_out
    for i, a in enumerate(s1):
        for j, b in enumerate(s2):
            out[i + j] += a * b
    start = idx1[0] + idx2[0]
    return [start + i for i in range(n_out)], out