import numpy as np

loadArray = np.load('assets/arr_0.npy')
sampleMatrix = np.array([np.array([np.array([1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])]),
                         np.array([np.array([1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])]),
                         np.array([np.array([1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])]),
                         np.array([np.array([1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])]),
                         np.array([np.array([1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])]),
                         np.array([np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])]),
                         np.array([np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])]),
                         np.array([np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])]),
                         np.array([np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                                   np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])])])
print(len(sampleMatrix), len(sampleMatrix[0]), len(sampleMatrix[0][0]))

for numMatrix, matrix in enumerate(loadArray):
    boolArray = np.ones((11, 11), dtype=bool)
    matrixReshaped = matrix.swapaxes(0, 2)
    resArr = []
    for oneDim in range(11):
        for twoDim in range(11):
            line = matrixReshaped[oneDim][twoDim]
            if len(set(list(line))) == 1: continue
            firstNonzero = np.argmax(line != 0)
            lastNonzero = len(line)-1 - np.argmax(line[::-1] != 0)
            result = line[firstNonzero:lastNonzero+1]
            for i, num in enumerate(result):
                if num == 0: resArr.append([firstNonzero+i, twoDim, oneDim])
    if not len(resArr): resArr = [0]

    stringResArr = str([str(arr).replace(',', '') for arr in resArr]).replace("'", '')
    if numMatrix + 1 < len(loadArray): stringResArr += ','
    print(numMatrix, stringResArr)