import numpy as np
import matplotlib.pyplot as plt

space = np.linspace(-2*np.pi, 2*np.pi, 256)

# frequencia, amostragem, duração, amplitude
infos = (1, 500, 1, 3)
infos_20 = (20, 500, 1, 1)
infos_10 = (10, 500, 1, 0.5)

t = np.linspace(0, infos[2], int(infos[1] * infos[2]), endpoint=False)

sinal = np.sin(2 * np.pi * infos[0] * t) * infos[3]
sinal_20 = np.sin(2 * np.pi * infos_20[0] * t) * infos_20[3]
sinal_10 = np.sin(2 * np.pi * infos_10[0] * t) * infos_10[3]

plt.plot((sinal_10 + sinal + sinal_20), color='r')
# plt.show()

# -----------------------------------------------------------------------------

sinal += sinal_20 + sinal_10

fourier = np.fft.fft(sinal)

n = len(sinal) / 2

# plt.plot(np.abs(fourier)/n)
# plt.show()

# -----------------------------------------------------------------------------

eixo_freq = np.fft.fftfreq(len(sinal), d=1/infos[1])

inversa = np.fft.ifft(fourier)

# plt.bar(eixo_freq, np.abs(fourier)/n)
# plt.xlim((-25, 25))
# plt.show()
