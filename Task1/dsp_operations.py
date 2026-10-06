def ReadSignalFile(file_name):
    indices = []
    samples = []

    with open(file_name, 'r') as f:

        # Skip first 3 lines
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


def AddSignals(file1, file2):
    indices1, samples1 = ReadSignalFile(file1)
    indices2, samples2 = ReadSignalFile(file2)

    result_indices = []
    result_samples = []

    for i in range(len(samples1)):
        result_indices.append(indices1[i])
        result_samples.append(samples1[i] + samples2[i])

    return result_indices, result_samples


# indices, samples = AddSignals(
#     "./Task1/input/Signal1.txt",
#     "./Task1/input/Signal2.txt"
# )
# print("-------------------------Result indices-----------------------------")

# print("Result indices:", indices)
# print("Result samples:", samples)

def MultiplySignal(file_name, constant):
    indices, samples = ReadSignalFile(file_name)

    result_indices = []
    result_samples = []

    for i in range(len(samples)):
        result_indices.append(indices[i])
        result_samples.append(samples[i] * constant)

    return result_indices, result_samples

# indices, samples = MultiplySignal(
#     "./Task1/input/Signal1.txt",
#     5
# )

# print("--------------------------- Multiply indices ---------------------------")

# print("Multiply indices:", indices)
# print("Multiply samples:", samples)
