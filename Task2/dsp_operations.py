#DSP Operations
def ReadSignalFileM(file_name):
    indices = []
    samples = []

    with open(file_name, 'r') as f:
        f.readline()
        f.readline()
        f.readline()
        line = f.readline()

        while line:
            values = line.strip().split()
            if len(values) == 2:
                index = int(values[0])
                sample = float(values[1])
                indices.append(index)
                samples.append(sample)
            line = f.readline()

    return indices, samples


def AddSignals(signals_data):
    if not signals_data:
        return [], []

    result_indices = signals_data[0][0][:]
    result_samples = [0.0] * len(result_indices)

    for indices, samples in signals_data:
        for i in range(len(samples)):
            if i < len(result_samples):
                result_samples[i] += samples[i]

    return result_indices, result_samples


def MultiplySignal(samples, constant):
    result_samples = []

    for sample in samples:
        result_samples.append(sample * constant)

    return result_samples

def SubSignals(signals):
    if len(signals) < 2:
        raise ValueError("At least two signals are required")

    indices, result_samples = signals[0]

    result_samples = result_samples.copy()

    for current_indices, current_samples in signals[1:]:
        if indices != current_indices:
            raise ValueError("Signals must have matching indices")

        for i in range(len(result_samples)):
            result_samples[i] = abs(result_samples[i] - current_samples[i])

    return indices[:], result_samples

def SquaringSignal(samples):
    result_samples = []
    for sample in samples:
        result_samples.append(sample ** 2)

    return result_samples

def NormalizeSignal(samples, target_range):
    if not samples:
        return []

    min_value = min(samples)
    max_value = max(samples)

    if max_value == min_value:
        return [0.0] * len(samples)

    result_samples = []

    for sample in samples:
        if target_range == "0_to_1":
            value = (sample - min_value) / (max_value - min_value)

        elif target_range == "-1_to_1":
            value = 2 * (sample - min_value) / (max_value - min_value) - 1

        else:
            raise ValueError("Invalid normalization range")

        result_samples.append(value)

    return result_samples


def AccumulationSignal(samples):
    result_samples = []
    accumulated_value = 0.0

    for sample in samples:
        accumulated_value += sample
        result_samples.append(accumulated_value)

    return result_samples

samples = [2, 3, 4, 1]

print(SquaringSignal(samples))
# [4, 9, 16, 1]

print(AccumulationSignal(samples))
# [2.0, 5.0, 9.0, 10.0]

print(NormalizeSignal(samples, "0_to_1"))
# [0.333..., 0.666..., 1.0, 0.0]

print(NormalizeSignal(samples, "-1_to_1"))
# [-0.333..., 0.333..., 1.0, -1.0]
#===================Quantization========================
import math


def Quantization(signal, num_bits=None, num_levels=None):

    if num_levels is None:
        if num_bits is None:
            raise ValueError("Specify num_bits or num_levels")

        num_levels = 2 ** num_bits

    if num_levels <= 0:
        raise ValueError("Number of levels must be positive")

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
            interval_indices.append(0)
            encoded_values.append("0" * bits)
            quantized_values.append(sample)
            sampled_errors.append(0.0)

        return (
            interval_indices,
            encoded_values,
            quantized_values,
            sampled_errors
        )

    for sample in signal:

        index = math.ceil((sample - minimum) / delta) - 1

        index = max(0, min(index, num_levels - 1))

        quantized_value = minimum + (index + 0.5) * delta

        encoded_value = format(index, f"0{bits}b")

        error = quantized_value - sample

        interval_indices.append(index)
        encoded_values.append(encoded_value)
        quantized_values.append(round(quantized_value, 4))
        sampled_errors.append(round(error, 4))

    return (
        interval_indices,
        encoded_values,
        quantized_values,
        sampled_errors
    )
# =======================================================
#                      Testing
# =======================================================
if __name__ == "__main__":
    from Task1Test import ReadSignalFile, MultiplySignalByConst, AddSignalSamplesAreEqual, SignalSamplesAreEqual

    try:
        print("Testing Addition For Signal1 and Signal2:")
        ind1, val1 = ReadSignalFileM('../Task1/input/Signal1.txt')
        ind2, val2 = ReadSignalFileM('../Task1/input/Signal2.txt')

        ind_add, val_add = AddSignals([(ind1, val1), (ind2, val2)])
        AddSignalSamplesAreEqual('Signal1.txt', 'Signal2.txt', ind_add, val_add)

        print("-----------------------------------------------------------")

        print("Testing Addition For Signal1 and Signal3:")
        ind1, val1 = ReadSignalFileM('../Task1/input/Signal1.txt')
        ind2, val2 = ReadSignalFileM('../Task1/input/Signal3.txt')

        ind_add, val_add = AddSignals([(ind1, val1), (ind2, val2)])
        AddSignalSamplesAreEqual('Signal1.txt', 'Signal3.txt', ind_add, val_add)

        print("-----------------------------------------------------------")

        print("\nTesting Multiplication by 5:")
        ind_m, val_m = ReadSignalFileM('../Task1/input/Signal1.txt')

        val_mul = MultiplySignal(val_m, 5) 
        ind_mul = ind_m  
        MultiplySignalByConst(5, ind_mul, val_mul)

        print("-----------------------------------------------------------")

        print("\nTesting Multiplication by 10:")
        ind_m, val_m = ReadSignalFileM('../Task1/input/Signal2.txt')

        val_mul = MultiplySignal(val_m, 10) 

        ind_mul = ind_m  
        MultiplySignalByConst(10, ind_mul, val_mul)
        
    except FileNotFoundError:
        print("Test skipped: Run the GUI directly, or make sure the './input/' folder exists if you want to run this file alone.")


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
        print("\nTesting Normalization (0 to 1) for Signal1:")
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