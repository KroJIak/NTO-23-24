from sineWave import generateSineWave, SAMPLE_RATE, DURATION
import numpy as np
from matplotlib import pyplot as plt
from scipy.io import wavfile

NAME_WAV_FILE = 'mysinewave.wav'

def main():
    _, niceTone = generateSineWave(400, SAMPLE_RATE, DURATION)
    _, noiseTone = generateSineWave(4000, SAMPLE_RATE, DURATION)

    noiseTone = noiseTone * 0.3
    mixedTone = niceTone + noiseTone

    normalizedTone = np.int16((mixedTone / mixedTone.max()) * 32767)

    wavfile.write(NAME_WAV_FILE, SAMPLE_RATE, normalizedTone)

    plt.plot(normalizedTone[:1000])
    plt.show()



if __name__ == '__main__':
    main()