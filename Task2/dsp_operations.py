
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
            result_samples[i] -= current_samples[i]

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
# =======================================================
#                      Testing
# =======================================================
# if __name__ == "__main__":
#     from Task1Test import ReadSignalFile, MultiplySignalByConst, AddSignalSamplesAreEqual, SignalSamplesAreEqual

#     try:
#         print("Testing Addition For Signal1 and Signal2:")
#         ind1, val1 = ReadSignalFileM('./input/Signal1.txt')
#         ind2, val2 = ReadSignalFileM('./input/Signal2.txt')

#         ind_add, val_add = AddSignals([(ind1, val1), (ind2, val2)])
#         AddSignalSamplesAreEqual('Signal1.txt', 'Signal2.txt', ind_add, val_add)

#         print("-----------------------------------------------------------")

#         print("Testing Addition For Signal1 and Signal3:")
#         ind1, val1 = ReadSignalFileM('./input/Signal1.txt')
#         ind2, val2 = ReadSignalFileM('./input/Signal3.txt')

#         ind_add, val_add = AddSignals([(ind1, val1), (ind2, val2)])
#         AddSignalSamplesAreEqual('Signal1.txt', 'Signal3.txt', ind_add, val_add)

#         print("-----------------------------------------------------------")

#         print("\nTesting Multiplication by 5:")
#         ind_m, val_m = ReadSignalFileM('./input/Signal1.txt')

#         val_mul = MultiplySignal(val_m, 5) 
#         ind_mul = ind_m  
#         MultiplySignalByConst(5, ind_mul, val_mul)

#         print("-----------------------------------------------------------")

#         print("\nTesting Multiplication by 10:")
#         ind_m, val_m = ReadSignalFileM('./input/Signal2.txt')

#         val_mul = MultiplySignal(val_m, 10) 

#         ind_mul = ind_m  
#         MultiplySignalByConst(10, ind_mul, val_mul)
        
#     except FileNotFoundError:
#         print("Test skipped: Run the GUI directly, or make sure the './input/' folder exists if you want to run this file alone.")
