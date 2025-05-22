import numpy as np
import matplotlib.pyplot as plt
import pywt

infos = (1, 500, 1, 3)
infos_20 = (20, 500, 1, 1)
infos_10 = (10, 500, 1, 0.5)

t = np.linspace(0, infos[2], int(infos[1] * infos[2]), endpoint=False)

sinal = np.sin(2 * np.pi * infos[0] * t) * infos[3]
sinal_20 = np.sin(2 * np.pi * infos_20[0] * t) * infos_20[3]
sinal_10 = np.sin(2 * np.pi * infos_10[0] * t) * infos_10[3]

sinal += sinal_10 + sinal_20

escala = np.arange(1, 128)
coeficientes, frequencias = pywt.cwt(sinal, escala, 'morl')

plt.figure(figsize=(10, 6))
plt.imshow(np.abs(coeficientes), aspect='auto', extent=[0, 1, escala[-1], escala[0]], cmap='jet')
plt.colorbar(label='Magnitude')
plt.ylabel('Escalas')
plt.xlabel('Tempo [s]')
plt.show()
