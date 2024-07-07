import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial import Polynomial

# Función para calcular los coeficientes del polinomio
def calcular_polinomio(x, y):
    return Polynomial.fit(x, y, deg=len(x)-1)

# Función para graficar el polinomio
def graficar_polinomio(polynomial, x_vals, y_vals):
    plt.plot(x_vals, y_vals, label=f'Polinomio ajustado')
    plt.scatter(x_vals, y_vals, color='red')
    plt.title('Demanda energética 2023')
    plt.xlabel('Mes')
    plt.ylabel('Potencia [MW]')
    plt.legend()
    plt.grid(True)
    plt.show()

# Solicitar al usuario los puntos
num_puntos = int(input("Ingresa el número de puntos a ingresar: "))
x_vals = [1,2,3,4]
y_vals = [1,2,3,4]
for i in range(num_puntos):
    x = float(input(f"Ingrese # mes{i+1}: "))
    y = float(input(f"Ingrese potencia{i+1}: "))
    x_vals.append(x)
    y_vals.append(y)

# Calcular el polinomio que pasa por los puntos
polynomial = calcular_polinomio(x_vals, y_vals)
print(f'Polinomio: {polynomial}')

# Graficar el polinomio
x_plot = np.linspace(min(x_vals) - 1, max(x_vals) + 1, 100)
y_plot = polynomial(x_plot)
graficar_polinomio(polynomial, x_vals, y_vals)
