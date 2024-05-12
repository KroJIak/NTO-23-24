#N, M = map(int, input().split())
N, M = 4, 4
matrix = [list(map(int, input().split())) for i in range(N)]
resultMatrix = [[0] * M for i in range(N)]

resultMatrix[0][0] = matrix[0][0]
for j in range(1, M):
    resultMatrix[0][j] = resultMatrix[0][j-1] + matrix[0][j]
for i in range(1, N):
    resultMatrix[i][0] = resultMatrix[i-1][0] + matrix[i][0]

for i in range(1, N):
    for j in range(1, M):
        resultMatrix[i][j] = matrix[i][j] + max(resultMatrix[i-1][j], resultMatrix[i][j-1])

print(resultMatrix[-1][-1])