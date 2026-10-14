#!/usr/bin/env python
# coding: utf-8

# In[ ]:



def ReadSignalFile(file_name): 
    expected_indices=[]
    expected_samples=[]
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L=line.strip()
            if len(L.split(' '))==2:
                L=line.split(' ')
                V1=int(L[0])
                V2=float(L[1])
                expected_indices.append(V1)
                expected_samples.append(V2)
                line = f.readline()
            else:
                break
    return expected_indices,expected_samples


# In[ ]:


def AddSignalSamplesAreEqual(userFirstSignal,userSecondSignal,Your_indices,Your_samples):
    if(userFirstSignal=='Signal1.txt' and userSecondSignal=='Signal2.txt'):
        file_name="./output/Signal1+signal2.txt" # write here path of signal1+signal2

    elif(userFirstSignal=='Signal1.txt' and userSecondSignal=='Signal3.txt'):
        file_name="./output/Signal1+signal3.txt" # write here path of signal1+signal3
        
    expected_indices,expected_samples=ReadSignalFile(file_name)          
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print("Addition Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print("Addition Test case failed, your signal have different indicies from the expected one") 
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Addition Test case failed, your signal have different values from the expected one") 
            return
    print("Addition Test case passed successfully")


# In[ ]:


def MultiplySignalByConst(User_Const,Your_indices,Your_samples):
    if(User_Const==5):
        file_name="./output/MultiplySignalByConstant-Signal1 - by 5.txt" 
    elif(User_Const==10):
        file_name="./output/MultiplySignalByConstant-Signal2 - by 10.txt" 
        
    expected_indices,expected_samples=ReadSignalFile(file_name)      
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print("Multiply by "+str(User_Const)+ " Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print("Multiply by "+str(User_Const)+" Test case failed, your signal have different indicies from the expected one") 
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Multiply by "+str(User_Const)+" Test case failed, your signal have different values from the expected one") 
            return
    print("Multiply by "+str(User_Const)+" Test case passed successfully")


# In[ ]:


#TaskName => choose it (string explain the name of task like (adding sig1+sig2,subtracting, .... etc.))
#output_file_name => output file path (output file given by TAs)
# Your_indices => your indices list from your code (generated/calculated by you)
# Your_samples => your samples list from your code (generated/calculated by you)
def SignalSamplesAreEqual(TaskName,output_file_name,Your_indices,Your_samples):
    expected_indices=[]
    expected_samples=[]
    with open(output_file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L=line.strip()
            if len(L.split(' '))==2:
                L=line.split(' ')
                V1=int(L[0])
                V2=float(L[1])
                expected_indices.append(V1)
                expected_samples.append(V2)
                line = f.readline()
            else:
                break
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
         print(TaskName+" Test case failed, your signal have different length from the expected one")
         return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print(TaskName+" Test case failed, your signal have different indicies from the expected one") 
            return             
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print(TaskName+" Test case failed, your signal have different values from the expected one") 
            return
    print(TaskName+" Test case passed successfully")

#============================================
if __name__ == "__main__":
    import os
    from dsp_operations import (
        ReadSignalFileM,
        SubSignals,
        SquaringSignal,
        NormalizeSignal,
        AccumulationSignal,
    )

    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(base_dir, "..", "Task1", "input")
    output_dir = os.path.join(base_dir, "OUTPUT Arithmetic operations")

    def read_signal(name):
        return ReadSignalFileM(os.path.join(input_dir, name))

    def run_test(name, output_file, indices, samples):
        path = os.path.join(output_dir, output_file)
        if not os.path.exists(path):
            print(f"SKIPPED {name}: expected file not found")
            return

        SignalSamplesAreEqual(
            name, path, indices, samples
        )

    idx1, sig1 = read_signal("Signal1.txt")
    idx2, sig2 = read_signal("Signal2.txt")
    idx3, sig3 = read_signal("signal3.txt")

    print("\n=== Task 2 Original Tests ===")

    idx, result = SubSignals([(idx1, sig1), (idx2, sig2)])
    run_test("Subtraction Signal1 - Signal2",
             "signal1-signal2.txt", idx, result)

    idx, result = SubSignals([(idx1, sig1), (idx3, sig3)])
    run_test("Subtraction Signal1 - Signal3",
             "signal1-signal3.txt", idx, result)

    run_test("Squaring Signal1",
             "Output squaring signal 1.txt",
             idx1, SquaringSignal(sig1))

    run_test("Normalization Signal2 (0 to 1)",
             "normlize signal 2 (from 0 to 1 )-- output.txt",
             idx2, NormalizeSignal(sig2, "0_to_1"))

    run_test("Normalization Signal1 (-1 to 1)",
             "normalize of signal 1 (from -1 to 1)-- output.txt",
             idx1, NormalizeSignal(sig1, "-1_to_1"))

    run_test("Accumulation Signal1",
             "output accumulation for signal1.txt",
             idx1, AccumulationSignal(sig1))