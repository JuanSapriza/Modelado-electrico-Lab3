# Cargar los datos

import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter
from numpy import mean, pi
import numpy as np
from scipy.signal import find_peaks

#----------------------------
# Obtener las señales
#----------------------------

#escriba el nombre del documento que tiene los datos de la simulacion LTSPICE
filename = "/content/Ejemplo.txt"

#este programa asume que hay solo dos señales, la primera es el V y la segunda la corriente
#si desea puede modificar esto
#es importante que la señal incluya varios picos (al menos 3)
with open(filename, encoding='utf-8') as f:
    lines = f.readlines()[1:]

    t_s = np.array([float(line.split()[0]) for line in lines])
    v_V = np.array([float(line.split()[1]) for line in lines])
    i_A = np.array([float(line.split()[2]) for line in lines])

# Toma como tiempo 0 donde comienza la simulacion
t_s -= t_s[0]

#grafica las señales en el tiempo, para revisar que es correcto
fig, ax1 = plt.subplots()
ax1.plot(t_s, v_V, label='Voltaje (V)', color='blue')
ax1.set_ylabel('Voltaje (V)', color='blue')

ax2 = ax1.twinx()
ax2.plot(t_s, i_A, label='Corriente (A)', color='red')
ax2.set_ylabel('Corriente (A)', color='red')

plt.savefig('signals.png')
plt.show()

# Calcular el desfasaje y la diferencia de amplitud

# Convertir la corriente a mA para poder compararlos mejor
# Esto se puede cambiar
i_mA = i_A*1e3

# amplitudes
amp_v = (v_V.max() - v_V.min()) / 2
amp_i = (i_mA.max() - i_mA.min()) / 2

pv, _ = find_peaks(v_V)        # peaks of v_V
pi, _ = find_peaks(i_mA)       # peaks of i_mA

T  = t_s[pv[1]] - t_s[pv[0]]         # period from first two v_V peaks
dt1 = -t_s[pi[0]] + t_s[pv[0]]       # time shift between first peak V and first peak I
dt2 = -t_s[pi[1]] + t_s[pv[0]]       # time shift between second peak V and first peak I

#selects lower absolute value
if abs(dt1)<abs(dt2):
  dt=dt1
else:
  dt=dt2

#calcula el desfasaje
phase_rad  = 2*np.pi * dt / T
phase_deg  = np.degrees(phase_rad)
#toma valor entre -180 y 180 
if abs(phase_deg)>180:
  if phase_deg<0:
    phase_deg = 360 + phase_deg
  else:
    phase_deg = -360 + phase_deg

# Graficar los fasores

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.set_theta_zero_location('E')
ax.set_theta_direction(1)

# plot phasors
ax.plot([0, 0], [0, amp_v], color='blue', linewidth=2, label='v_V')
ax.plot([phase_rad, phase_rad], [0, amp_i], color='red', linewidth=2, label='i_mA')

ax.legend(loc='upper right')

plt.savefig('phasors.png')
plt.show()

print("Angulo de desfasaje: %4.1f" % phase_deg)
