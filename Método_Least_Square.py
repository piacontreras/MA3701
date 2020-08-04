# -*- coding: utf-8 -*-
### importamos las librerías que usaremos ###
#Pía Contreras
#parte 1 a) ii)
import numpy as np
import matplotlib.pyplot as plt
import random
from scipy import *
from scipy.optimize import leastsq



# iniciamos la semilla para generar valores aleatorios
# recuerde cambiar '1' por su RUT
# es importante fijar la semilla para que los datos aleatorios generados
# siempre sean los mismos (de acuerdo a su RUT) y por lo tanto, sean replicables.

random.seed(19840187) # aca cambie a su rut

# Agregue su número de lista

nLista=23

# definimos los valores de los parámetros del modelo original
# estos son los parámetros que debemos buscar con los métodos de la tarea
# las 4 lineas que vienen NO pueden ser modificadas
a = (1+nLista/85)*8.967 + 0.05*random.random()
omega = 3.1415/3.0 - 0.1*random.random()
phi = 3.1415/6.0 + + 0.1*random.random()
b = (1+nLista/85)*0.345 - + 0.05*random.random()

xobjetivo=np.array([a,omega,phi,b])

#definimos la función del modelo M que asocia tiempo con temperatura
def M(t):
    ydata = a*np.sin(t*omega+phi) + b*t
    return ydata 
    
#definimos el arreglo de tiempo considerado, usted puede cambiar el intervalo
# de tiempo como el número de puntos utilizado
tdata = np.linspace(0.0, 25.0, num=750)

    
N = len(tdata)
ydata = np.zeros(N) #creamos el arreglo que contendrá los "datos medidos"
# los datos medidos en este caso son una perturbación de los datos originales
# esta perturbación es aleatoria y depende de su RUT

for i in range(0,N):
    rand = random.random()
    ydata[i] = M(tdata[i]) - 3.8546*rand*(-1)**i

#Se creó la función R para ajustar los datos obtenidos
def R(x):
    r=np.zeros(N)
    for i in range(0,N):
        r[i]=ydata[i]-(x[0]*np.sin(tdata[i]*x[1]+x[2])+x[3]*tdata[i])                
    return np.transpose(r)

#Se creó el vector de datos iniciales               
x0=np.array([8.98, 0.95, 0.60, 0.30])

#Se aplicó la funcion leastsq para R y datos iniciales x0
xoptimo=leastsq(R,x0)    
      
print(xobjetivo)
print(xoptimo[0])

#Se utilizó solo la primera componente de la salida de la funcion leastsq
xbacan=np.array(xoptimo[0])

#Se creó una función que permitiera el ajuste de datos con lo obtenido en la salida de leastsq
newdata=xbacan[0]*np.sin(xbacan[1]*tdata+xbacan[2])+tdata*xbacan[3]

#Graficar datos originales vs leastsq
plt.plot(tdata, ydata, color='blue', marker='.', linestyle='', markersize=1)  
plt.plot(tdata,newdata,color='red',marker='.',linestyle='',markersize=1)
plt.show ()
