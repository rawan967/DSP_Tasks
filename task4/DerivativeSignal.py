from dsp_operations import FirstDerivative, SecondDerivative


def DerivativeSignal():
    InputSignal = [float(i) for i in range(1, 101)]          # 1, 2, ..., 100
    expectedOutput_first = [1] * 99
    expectedOutput_second = [0] * 98

    """
    Write your Code here:
    Start
    """
    indices = list(range(len(InputSignal)))
    _, FirstDrev = FirstDerivative(indices, InputSignal)      # y(n) = x(n) - x(n-1)
    _, SecondDrev = SecondDerivative(indices, InputSignal)    # y(n) = x(n+1) - 2x(n) + x(n-1)
    """
    End
    """

    """
    Testing your Code
    """
    if (len(FirstDrev) != len(expectedOutput_first)) or (len(SecondDrev) != len(expectedOutput_second)):
        print("mismatch in length")
        return
    first = second = True
    for i in range(len(expectedOutput_first)):
        if abs(FirstDrev[i] - expectedOutput_first[i]) >= 0.01:
            first = False
            print("1st derivative wrong")
            return
    for i in range(len(expectedOutput_second)):
        if abs(SecondDrev[i] - expectedOutput_second[i]) >= 0.01:
            second = False
            print("2nd derivative wrong")
            return
    if first and second:
        print("Derivative Test case passed successfully")
    else:
        print("Derivative Test case failed")


  
    DerivativeSignal()