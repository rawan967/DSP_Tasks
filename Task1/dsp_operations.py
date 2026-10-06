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
    
    for i in range(len(samples)):
        result_samples.append(samples[i] * constant)

    return result_samples


