with open('test.txt') as file:
    arr = [line.strip() for line in file.readlines()]

di = {name: arr.count(name) for name in set(arr)}
print(di)