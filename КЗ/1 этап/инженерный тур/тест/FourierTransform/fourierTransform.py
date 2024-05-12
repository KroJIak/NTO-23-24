from sineWave import SAMPLE_RATE, DURATION
from additionSignals import NAME_WAV_FILE
import numpy as np
from matplotlib import pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft, rfft, fftfreq, rfftfreq, rfft, irfft

def main():
    _, normalizedTone = wavfile.read(NAME_WAV_FILE)

    # число точек в normalizedTone
    N = SAMPLE_RATE * DURATION

    # yf = fft(normalizedTone)
    # xf = fftfreq(N, 1 / SAMPLE_RATE)
    yf = rfft(normalizedTone)
    xf = rfftfreq(N, 1 / SAMPLE_RATE)

    # plt.plot(xf, np.abs(yf))
    # plt.show()

    # Максимальная частота составляет половину частоты дискретизации
    pointsPerFreq = len(xf) / (SAMPLE_RATE / 2)

    # Наша целевая частота - 4000 Гц
    targetIdx = int(pointsPerFreq * 4000)
    yf[targetIdx - 2:targetIdx + 2] = 0

    # plt.plot(xf, np.abs(yf))
    # plt.show()

    newSig = irfft(yf)

    normNewSig = np.int16(newSig * (32767 / newSig.max()))
    wavfile.write('mysinewave-clean.wav', SAMPLE_RATE, normNewSig)

    plt.plot(newSig[:1000])
    plt.show()

if __name__ == '__main__':
    main()