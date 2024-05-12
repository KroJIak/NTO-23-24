from math import cos, sin

L = 150
H = 100

alpha, beta = map(float, input().split())
x = L * cos(alpha) + H * cos(alpha + beta)
y = L * sin(alpha) + H * sin(alpha + beta)
print(round(x), round(y))