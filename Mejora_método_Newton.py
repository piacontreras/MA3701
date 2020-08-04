# -*- coding: utf-8 -*-
### importamos las librerías que usaremos ###
#Pía Contreras
#Parte b)
import numpy as np
import matplotlib.pyplot as plt
import random 

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

#Se definio la funcion R que permite ajustar los datos como dice el enunciad
def R(x):
    r=np.zeros(N)
    for i in range(0,N):
        r[i]=ydata[i]-(x[0]*np.sin(tdata[i]*x[1]+x[2])+x[3]*tdata[i])                
    return np.transpose(r)

#Se definió el jacobiano a mano, es decir, llenando fila por fila y columna por columna
#lo que se obtuvo de derivar manualment la funcion R
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


#se creó el vector de valores inciales con igual motivo que la parte a)i)
x0=np.array([8.98, 0.95, 0.60, 0.30])


#Se definio la iteracion
iteracion=0
#se definio un numero maximo de iteracion, el cual se puede ir modificando para
#poder visualizar en que numero de iteracion converge
Maxiteracion=4


#se creo un ciclo while que recorra x1 como se define en el enunciado y que además
#cumpla la condicion de que el error debe ser menos a la diferencia abosluta
#entre xk+1 y xk, si esto se cumple, se sigue iterando hasta obtener el valor optimo
while iteracion<Maxiteracion:
      r=R(x0)
      Jacobiano=J(x0)
      Err=np.linalg.norm(Jacobiano)
      #multiplicacion jacobiano con su transpuesta
      A=np.dot(np.transpose(Jacobiano),Jacobiano)
      #multiplicación jacobiano con r
      B=np.dot(np.transpose(Jacobiano),r)
      #invierto A
      C=np.linalg.inv(A)
      x1 = x0 - np.dot(C,B)
      if np.amax(abs(np.all(x1-x0)))<Err:
          x0=x1
          iteracion=iteracion+1
          
      
#impresion del x al cual quiero llegar      
print(xobjetivo)
#impresion del x luego de aplicar el metodo
print(x0)
    
#creacion nueva variable con x la variable en el metodo de la parte b)
newdata=x1[0]*np.sin(x1[1]*tdata+x1[2])+tdata*x1[3]

#grafico datos iniciales vs grafco metodo parte b
plt.plot(tdata, ydata, color='blue', marker='.', linestyle='', markersize=1)
plt.plot (tdata,newdata,color="red", marker='.',linestyle='',markersize=1)
plt.xlabel("tdata")
plt.ylabel("ydata v/s newdata")
plt.show()



