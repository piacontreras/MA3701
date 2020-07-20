import numpy as np
import matplotlib.pyplot as plt
import random
from scipy import *
from scipy.optimize import linprog

#cambimos la semilla para que se repliquen los datos de igual manera  
random.seed(19840187)

#definimos n el cual es el numero de salas de cirujia 
n=2

#definimos m como el número de pacientes
m=4

#definimos T, en el cual solo pueden haber m operaciones
T=10

#tiempo aleatorio del paciente i en la sala j
a=3
b=5
t_ij=np.zeros((m,n))
for i in range (m):
    for j in range(n):
        t_ij[i,j]=a+(b-a)*random.random()



#se define c como dice el enunciado, es decir como transpuesta de t_ij
c=np.zeros((m*n))
contador =0
for i in range (0,m):
    for j in range (0,n):
        c[contador]=t_ij[i,j]
        contador=contador+1

#difiniendo los subs-vectores/matrices de A y b según indica el enunciado
#Definiendo los subs b
#b1 es un vector de dimensiones mx1 de unos
b1=np.ones((m,1))

#b2 es un vector de dimensiones nx1 de T
b2=np.zeros((n,1))
for i in range (0,n):
    b2[i,0]=T

#definiendo las submatrices A
#A1 es una matriz que tiene unos dependiendo de n
#y ceros con cierta cantidad de veces
#A1 es una matriz de dimensiones mx(m*n)
A1=np.zeros((m,m*n))
a=0
b=n-1 #1
for i in range (0,m):
    for j in range (0,n*m):
        if a<=i+j<=b:
            A1[i,j]=1
    a=a+(n+1)
    b=b+(n+1)

    
#A2 es una matriz compuesta de submatrices donde en su diagonal tiene t_ij
#las submatrices son de nxn
#A2 tiene dimensiones de nx(m*n)
#definí A2 componente a componente
#para un (m=4 y n=2) y (m=5 y n=3)
A2=np.zeros((n,m*n))
for i in range (0,n): 
    for j in range (0,m*n):
         #if A2[i,j]==1:
        if i==j:
            A2[0,0]=c[0]
            A2[1,3]=c[3]
        if(j%n)==i:
            A2[0,2]=c[2]
        if (j%n)!=i:
            A2[1,1]=c[1]
            A2[0,4]=c[4]
            A2[1,5]=c[5]
            A2[0,6]=c[6]
            A2[1,7]=c[7]
if m==5 and n==3:
    A2=np.zeros((n,m*n))
    for i in range (0,n):
        for j in range (0,m*n):
            if i==j:
                A2[0,0]=c[0]
                A2[1,4]=c[4]
                A2[2,8]=c[8]
            if (j%n)==i:
                A2[0,6]=c[6]
            if (j%n)!=i:
                A2[0,3]=c[1]
                A2[0,9]=c[9]
                A2[0,12]=c[12]
                A2[1,1]=c[1]
                A2[1,7]=c[7]
                A2[1,10]=c[10]
                A2[1,13]=c[13]
                A2[2,2]=c[2]
                A2[2,5]=c[5]
                A2[2,11]=c[11]
                A2[2,14]=c[14]
            

#concatenamos las submatrices para obtener la matriz más grande
#tanto para A como para b
A=np.concatenate((A1,A2))

b=np.concatenate((b1,b2))



#aplicamos la función linprog utilizando -c ya que estamos minimizando
#hacemos que x esté entre (0,1)
x=linprog(-c,A,b,bounds=(0,1),method='simplex')
print x

#impresion del valor c transpuesto * x (optimo)
opt=np.dot(c,x.x)
print opt
