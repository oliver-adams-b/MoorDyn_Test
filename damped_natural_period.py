import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
from scipy.optimize import curve_fit


full_df = pd.read_csv("/home/oliver/Desktop/kelson/MoorDyn-dev/kelson_test/specifications/line_stretched_Line1.out", 
                      sep = "\t", 
                      dtype= str)

 
tension = full_df[["Time", " Seg1Te "]]
tension = tension.iloc[20000::1000, :]

t = tension["Time"].apply(float).to_numpy()
T = tension[" Seg1Te "].apply(float).to_numpy()

def damping(x, A, lamb, w, phi, h):
    return A*np.exp(-lamb*x)*np.cos(w*x - phi)+h

popt, pcov = curve_fit(damping,t, T)
A, lamb, w, phi, h = popt
pred_T = [damping(x, A, lamb, w, phi, h) for x in t]

plt.plot(t, pred_T, c = "r", 
         linestyle = "-", 
         label = "Approximation: $T = A \exp(-\lambda t) \cos(\omega t - \phi)$")
plt.plot(t, T, c = "b", label = "Simulation Data")
plt.legend(loc = "best")
plt.xlabel("Time (s)")
plt.ylabel("Tension (N)")
plt.title("Tension at Top Chain Node, Damped Period $T = 2\pi/\omega = {}(s)$".format(str(2*np.pi / w)[:5]))
