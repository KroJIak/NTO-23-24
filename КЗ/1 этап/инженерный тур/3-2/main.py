import os

d = {i: 0 for i in range(5)}
fileList = os.listdir('labels/')
for name in fileList:
    with open(f'labels/{name}') as file:
        arr = [int(line.strip().split()[0]) for line in file.readlines()]
        for num in set(arr): d[num] += 1
print(d)

{'deer': 133, 'fox': 127, 'wolf': 147, 'rabbit': 135, 'pig': 134}
{'deer': 120, 'fox': 112, 'wolf': 132, 'rabbit': 120, 'pig': 119}