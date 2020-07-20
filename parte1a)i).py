# -*- coding: utf-8 -*-
### importamos las librerías que usaremos ###
#Pía Contreras
#parte 1 a) i)
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
    
#definimos una funcion m para cada componente del vector x que se le entregará
def M_i(x):
    ydata=x[0]*np.sin(tdata[i]*x[1]+x[2])+x[3]*tdata[i]
    return ydata

#Se creó el jacobiano a mano, es decir llenando fila por fila y columna por
#columna, lo que se obtuvo de derivar manualmente la funcion R
def J(x): #750x4
    J=np.zeros((N,4))
    for i in range (0,N):
        J[i,0]=-1*np.sin(x[1]*tdata[i]+x[2])
    for i in range (0,N):
        J[i,1]=-x[0]*np.cos(x[1]*tdata[i]+x[2])*tdata[i]
    for i in range (0,N):
        J[i,2]=-x[0]*np.cos(x[1]*tdata[i]+x[2])
    for i in range (0,N):
        J[i,3]=-1*tdata[i]
    return J

#Se definió la funcion R que permite ajustar los datos como dice el anunciado
def R(x):
    r=np.zeros(N)
    for i in range(0,N):
        r[i]=ydata[i]-(x[0]*np.sin(tdata[i]*x[1]+x[2])+x[3]*tdata[i])                
    return np.transpose(r)

#Se creó a mano también la matriz S como se especifica en el enunciado
#Se fue llenando fila por fila y columna por columna                   
def S(x): #4x4
    S=np.zeros((4,4))
    r=R(x)
    S[0,0]=0
    S[0,3]=0
    S[1,3]=0
    S[2,3]=0
    S[3,0]=0
    S[3,1]=0
    S[3,2]=0
    S[3,3]=0               
    S[0,1]=0
    S[0,2]=0
    S[1,0]=0
    S[1,1]=0
    S[1,2]=0
    S[2,0]=0
    S[2,1]=0
    S[2,2]=0
    for i in range (0,N):
        aux1= -1*r[i]*np.cos(x[1]*tdata[i]+x[2])*tdata[i]
        S[0,1] = S[0,1]+aux1
        aux2=-1*r[i]*np.cos(x[1]*tdata[i]+x[2])
        S[0,2]=S[0,2]+aux2
        aux3=-1*r[i]*np.cos(x[1]*tdata[i]+x[2])*tdata[i]
        S[1,0]=S[1,0]+aux3
        aux4=r[i]*x[0]*tdata[i]**2*np.sin(x[1]*tdata[i]+x[2])
        S[1,1]=S[1,1]+aux4
        aux5=r[i]*x[0]*tdata[i]*np.sin(x[1]*tdata[i]+x[2])
        S[1,2]=S[1,2]+aux5
        aux6=-1*r[i]*np.cos(x[1]*tdata[i]+x[2])
        S[2,0]=S[2,0]+aux6
        aux7=r[i]*x[0]*tdata[i]*np.sin(x[1]*tdata[i]+x[2])
        S[2,1]=S[2,1]+aux7
        aux8=r[i]*x[0]*np.sin(x[1]*tdata[i]+x[2])
        S[2,2]=S[2,2]+aux8
    return S
    

#Se creó el vector de valores iniciales, se eligió al ojo, es decir donde convergiera
#el método, y resultaron ser valores muy cercanos a los valores a los cuales se debe llegar
x0=np.array([8.98, 0.95, 0.60, 0.30])


#Se definió una iteracion
iteracion=0
#Se definió el numero máximo de iteracion, el cual se puede ir modificando
#para poder visualizar en que numero de iteración converge
Maxiteracion=3


#se creó un ciclo while que recorra x1 como se define en el enunciado, y si
#además cumple la condición de que el error debe ser menor a la diferencia absoluta entre el
#xk+1 y el xk, si esto se cumple, se sigue iterando hasta llegar a un valor optimo.
while iteracion<Maxiteracion:
      r=R(x0)
      Jacobiano=J(x0)
      Ss=S(x0)
      Err=np.linalg.norm(Jacobiano)
      x1 = x0 - np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(Jacobiano),Jacobiano)+ Ss),np.transpose(Jacobiano)),r)
      if np.amax(abs(np.all(x1-x0)))<Err:
          x0=x1
          iteracion=iteracion+1
      

#impresion del x al cual se quiere llegar     
print(xobjetivo)
#impresion del x luego de la iteracion y aplicacion del metodo de newton
print(x0)
    

#creacion nueva variale con el x al que se le aplicó el método de newton 
newdata=x0[0]*np.sin(x0[1]*tdata+x0[2])+tdata*x0[3]



    


#grafica de datos originales vs grafica luego de aplicar el metodo de newton
plt.plot(tdata, ydata, color='blue', marker='.', linestyle='', markersize=1)
plt.plot (tdata,newdata,color="red", marker='.',linestyle='',markersize=1)
plt.xlabel("tdata")
plt.ylabel("ydata v/s newdata")
plt.show()






                   
                
                   

