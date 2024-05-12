n = int(input())
result = ''
for i in range(n):
    symb, count = input().split()
    result += symb * int(count)
print(result)