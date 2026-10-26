"""DSP operations for Task 1 and Task 2."""
import cmath, math

def ReadSignalFileM(file_name):
    indices = []
    samples = []

    with open(file_name, "r", encoding="utf-8") as file:
        # Signal files have three header lines.
        for _ in range(3):
            next(file, None)

        for line in file:
            values = line.split()
            if len(values) == 2:
                try:
                    indices.append(int(values[0]))
                    samples.append(float(values[1]))
                except ValueError:
                    # Ignore non-data/footer lines.
                    continue

    return indices, samples


def AddSignals(signals_data):
    if not signals_data:
        return [], []

    indices = signals_data[0][0][:]
    if any(signal_indices != indices for signal_indices, _ in signals_data):
        raise ValueError("All signals must have matching indices.")

    if any(len(samples) != len(indices) for _, samples in signals_data):
        raise ValueError("Each signal must have the same number of indices and samples.")

    result = [0.0] * len(indices)
    for _, samples in signals_data:
        for i, sample in enumerate(samples):
            result[i] += sample

    return indices, result


def MultiplySignal(samples, constant):
    return [sample * constant for sample in samples]


def SubSignals(signals):
    """Calculate the absolute difference between signals."""
    if len(signals) < 2:
        raise ValueError("At least two signals are required.")

    indices = signals[0][0][:]
    result = signals[0][1][:]

    if len(indices) != len(result):
        raise ValueError("Invalid signal data.")

    for current_indices, current_samples in signals[1:]:
        if current_indices != indices:
            raise ValueError("Signals must have matching indices.")

        if len(current_samples) != len(result):
            raise ValueError("Signals must have matching lengths.")

        for i, sample in enumerate(current_samples):
            result[i] = abs(result[i] - sample)

    return indices, result


def SquaringSignal(samples):
    return [sample ** 2 for sample in samples]


def NormalizeSignal(samples, target_range):
    if target_range not in ("0_to_1", "-1_to_1"):
        raise ValueError("Invalid normalization range. Use '0_to_1' or '-1_to_1'.")

    if not samples:
        return []

    minimum = min(samples)
    maximum = max(samples)

    if maximum == minimum:
        # A constant signal cannot be stretched over a range; return zeros.
        return [0.0] * len(samples)

    normalized = []
    for sample in samples:
        scaled = (sample - minimum) / (maximum - minimum)
        if target_range == "-1_to_1":
            scaled = 2 * scaled - 1
        normalized.append(scaled)

    return normalized


def AccumulationSignal(samples):
    result = []
    running_total = 0.0

    for sample in samples:
        running_total += sample
        result.append(running_total)

    return result


def Quantization(signal, num_bits=None, num_levels=None):
    """Return interval numbers (1-based), binary codes, quantized samples and errors."""
    if num_levels is None:
        if num_bits is None:
            raise ValueError("Specify num_bits or num_levels.")
        if not isinstance(num_bits, int) or isinstance(num_bits, bool) or num_bits <= 0:
            raise ValueError("Number of bits must be a positive integer.")
        num_levels = 2 ** num_bits

    if not isinstance(num_levels, int) or isinstance(num_levels, bool) or num_levels <= 0:
        raise ValueError("Number of levels must be a positive integer.")

    if not signal:
        return [], [], [], []

    minimum = min(signal)
    maximum = max(signal)
    delta = (maximum - minimum) / num_levels
    bits = math.ceil(math.log2(num_levels))

    interval_indices = []
    encoded_values = []
    quantized_values = []
    sampled_errors = []

    if delta == 0:
        for sample in signal:
            interval_indices.append(1)
            encoded_values.append(format(0, f"0{bits}b"))
            quantized_values.append(round(sample, 4))
            sampled_errors.append(0.0)
        return interval_indices, encoded_values, quantized_values, sampled_errors

    for sample in signal:
        zero_based_index = math.ceil((sample - minimum) / delta) - 1
        zero_based_index = max(0, min(zero_based_index, num_levels - 1))

        quantized_value = minimum + (zero_based_index + 0.5) * delta 
        encoded_value = format(zero_based_index, f"0{bits}b")
        error = quantized_value - sample

        # Test files use 4 decimal places for the displayed numeric values.
        interval_indices.append(zero_based_index + 1)
        encoded_values.append(encoded_value)
        quantized_values.append(round(quantized_value, 4))
        sampled_errors.append(round(error, 4))

    return interval_indices, encoded_values, quantized_values, sampled_errors


#  ==================   Task 3 ===============


def Transform(values, inverse=False):
    N = len(values)
    sign = 1 if inverse else -1          # IDFT: +  |  DFT: -
    result = []
    for k in range(N):
        total = 0
        for n in range(N):
            angle = sign * 2 * math.pi * k * n / N
            total += values[n] * cmath.exp(1j * angle)
        if inverse:
            total = total / N            # القسمة على N في الـ IDFT بس
        result.append(total)
    return result

def GetAmplitudes(X):
    return [abs(v)for v in X]

def GetPhases(X):
    return [cmath.phase(v) for v in X]

def NormalizeAmplitudes(amps):
    m = max(amps) if amps else 0
    if m == 0:
        return [0.0 for _ in amps]
    return [a / m for a in amps]

def GetFrequencies(N, fs):
    return [k * fs / N for k in range(N)]

def DominantFrequencies(freqs, norm_amps, threshold=0.5):
    return [(f, a) for f, a in zip(freqs, norm_amps) if a > threshold]

def FromPolar(amps, phases):
    return [a * cmath.exp(1j * p) for a, p in zip(amps, phases)]

def ModifyComponent(amps, phases, k, new_amp=None, new_phase=None):
    if k < 0 or k >= len(amps):
        raise ValueError("k out of range")
    amps, phases = amps[:], phases[:]
    if new_amp is not None:
        amps[k] = new_amp
    if new_phase is not None:
        phases[k] = new_phase
    return amps, phases

def RemoveDC(X):
    if not X:
        raise ValueError("empty")
    Y = X[:]
    Y[0] = 0
    return Y

def ReadFrequencyFile(file_name):
    amps, phases = [], []
    with open(file_name, "r", encoding="utf-8") as f:
        for _ in range(3):
            next(f, None)
        for line in f:
            v = line.split()
            if len(v) == 2:
                try:
                    amps.append(float(v[0].rstrip("fF")))
                    phases.append(float(v[1].rstrip("fF")))
                except ValueError:
                    continue
    return amps, phases


def ReadFileType(file_name):
    """Return the first header line of a signal file: 0 = time domain, 1 = frequency domain."""
    with open(file_name, "r", encoding="utf-8") as f:
        return int(f.readline().strip())


def CompareFrequencyData(amps, phases, exp_amps, exp_phases, tol=0.01):
    """Compare amplitude/phase lists with expected ones. Returns (passed, message)."""
    if len(amps) != len(exp_amps) or len(phases) != len(exp_phases):
        return False, "Different length from the expected signal."
    for k in range(len(amps)):
        if abs(amps[k] - exp_amps[k]) > tol:
            return False, f"Amplitude differs at k={k}: got {amps[k]:.4f}, expected {exp_amps[k]:.4f}"
        # Phase of a (near) zero component is meaningless, so skip it.
        if exp_amps[k] > tol:
            diff = abs(((phases[k] - exp_phases[k] + math.pi) % (2 * math.pi)) - math.pi)
            if diff > tol:
                return False, f"Phase differs at k={k}: got {phases[k]:.4f}, expected {exp_phases[k]:.4f}"
    return True, "Amplitude and phase match the expected file."


def CompareTimeData(indices, samples, exp_indices, exp_samples, tol=0.01):
    """Compare a time-domain signal with the expected one. Returns (passed, message)."""
    if len(samples) != len(exp_samples) or len(indices) != len(exp_indices):
        return False, "Different length from the expected signal."
    for i in range(len(samples)):
        if indices[i] != exp_indices[i]:
            return False, f"Index differs at position {i}: got {indices[i]}, expected {exp_indices[i]}"
        if abs(samples[i] - exp_samples[i]) > tol:
            return False, f"Value differs at n={indices[i]}: got {samples[i]:.4f}, expected {exp_samples[i]:.4f}"
    return True, "Signal matches the expected file."


