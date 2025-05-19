# In[]:
# Cargar los datos

import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter
from numpy import mean, pi
import numpy as np
from scipy.signal import find_peaks

#----------------------------
# Obtener las señakes
#----------------------------

filename = "grafica_ejemplo.txt"

with open(filename, encoding='utf-8') as f:
    lines = f.readlines()[1:]

    t_s = np.array([float(line.split()[0]) for line in lines])
    v_V = np.array([float(line.split()[1]) for line in lines])
    i_A = np.array([float(line.split()[2]) for line in lines])

t_s -= t_s[0]

fig, ax1 = plt.subplots()
ax1.plot(t_s, v_V, label='Voltaje (V)', color='blue')
ax1.set_ylabel('Voltaje (V)', color='blue')

ax2 = ax1.twinx()
ax2.plot(t_s, i_A, label='Corriente (A)', color='red')
ax2.set_ylabel('Corriente (A)', color='red')

plt.savefig('signals.png')
plt.show()

#In[]:
# Calcular el desfasaje y la diferencia de amplitud

# Convertir la corriente a mA para poder compararlos mejor
i_mA = i_A*1e3

# amplitudes
amp_v = (v_V.max() - v_V.min()) / 2
amp_i = (i_mA.max() - i_mA.min()) / 2

pv, _ = find_peaks(v_V)        # peaks of v_V
pi, _ = find_peaks(i_mA)       # peaks of i_mA

T  = t_s[pv[1]] - t_s[pv[0]]       # period from first two v_V peaks
dt = t_s[pi[0]] - t_s[pv[0]]       # time shift between first peaks

phase_rad  = 2*np.pi * dt / T
phase_deg  = np.degrees(phase_rad)


#In[]:
# Graficar los fasores

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.set_theta_zero_location('E')
ax.set_theta_direction(1)

# plot phasors
ax.plot([0, 0], [0, amp_v], color='blue', linewidth=2, label='v_V')
ax.plot([phase_deg, phase_deg], [0, amp_i], color='red', linewidth=2, label='i_mA')

ax.legend(loc='upper right')

plt.savefig('phasors.png')
plt.show()
