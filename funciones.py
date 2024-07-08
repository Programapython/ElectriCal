import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial import Polynomial

# Función para calcular los coeficientes del polinomio
def calcular_polinomio(x, y):
    return Polynomial.fit(x, y, deg=len(x)-1)

# Función para graficar el polinomio
def graficar_polinomio_original(graf, x_vals, y_vals):
    graf.plot(x_vals, y_vals, label='Demanda energética 2023 de Kallpa')
    graf.scatter(x_vals, y_vals, color='red')
    graf.legend()
    graf.grid(True)


def graficar_polinomio_ajustado(graf, pol, x_vals, y_vals, trunc):
    x_plot = np.linspace(min(x_vals) - 0.01, max(x_vals) + 0.01, 100)
    y_plot = pol(x_plot)
    graf.plot(x_plot, y_plot, label='Polinomio ajustado')
    graf.scatter(x_vals, y_vals, color='red')
    graf.scatter(x_vals[trunc:], pol((x_vals[trunc:])), color='green')
    graf.legend()
    graf.grid(True)

def calcular_tabla(pol,x_vals,y_vals):
    resultados=[['Mes','Valor predicho (kW)','Valor real (kW)','Diferencia (kW)','Error relativo(%)']]
    mes=x_vals
    valor_predicho=pol(x_vals)
    valor_real=y_vals
    diferencia=[]
    error_relativo=[]
    for i in range(len(mes)):
        dif = valor_real[i]-valor_predicho[i]
        diferencia.append(dif)
        porc=(dif/valor_real[i])*100
        error_relativo.append(porc)

    for i in range(len(mes)):
        result_i = [str(mes[i]),str(round(valor_predicho[i],5)),str(valor_real[i]),str(round(diferencia[i],5)),str(round(error_relativo[i],5))]
        resultados.append(result_i)

    return resultados

