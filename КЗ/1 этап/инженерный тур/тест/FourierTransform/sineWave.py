import numpy as np
from matplotlib import pyplot as plt

SAMPLE_RATE = 44100  # Гц
DURATION = 5  # Секунды

def generateSineWave(freq, sample_rate, duration):
    x = np.linspace(0, duration, sample_rate*duration, endpoint=False)
    frequencies = x * freq
    # 2pi для преобразования в радианы
    y = np.sin((2 * np.pi) * frequencies)
    return x, y

def main():
    # Генерируем волну с частотой 2 Гц, которая длится 5 секунд
    x, y = generateSineWave(2, SAMPLE_RATE, DURATION)
    plt.plot(x, y)
    plt.show()

if __name__ == '__main__':
    main()