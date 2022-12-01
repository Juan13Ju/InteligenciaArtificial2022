#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random as rand
import numpy as np
import pandas as pd
def f_1(x,y,z): return 80+184*x+96*y+68*z
def f_2(x,y,z): return (0.2*435)+415*x+501*y+300*z
def f_3(x,y,z): return (0.2*58)+50*x+82*y+15*z
def f_4(x,y,z): return (0.2*430)+439*x+520*y+263*z
σ=0.2


# In[2]:


x = 8
while True:
    pick = rand.sample(range(0, x), 3)
    if sum(pick) == x:
        break
print(pick)        
result = [pick[i]*0.1 for i in range(0,3)]
result


# In[3]:


def evaluete(lista): 
    w_0=f_1(lista[0], lista[1], lista[2])
    w_1=f_2(lista[0], lista[1], lista[2])
    w_2=f_3(lista[0], lista[1], lista[2])
    w_3=f_4(lista[0], lista[1], lista[2])
    return [w_0, w_1, w_2, w_3]


# In[4]:


def mutacion(vector):
    a= [abs(vector[i]+np.random.normal(0, σ))  for i in range(0, len(vector))]
    a= np.dot(a, 1/(sum(a)+0.2))
    
    return a
    


# In[5]:


def seleccion_nat(lista):
    i_t, c, σ=0, 0.817, 0.2
    padre=lista
    padre_V=evaluete(lista)
    hijo=mutacion(lista)
    hijo_V=evaluete(hijo)
    #print(σ)
    while i_t<=1000:
        H, HT, i=0, 0, 1
        while i <= 10:
            correct=0
            if hijo_V[0]<padre_V[0]:
                correct+=1
            if hijo_V[1]>400 and hijo_V[1]>padre_V[1]:
                correct+=1
            if hijo_V[2]<60 and hijo_V[2]<padre_V[2]:
                correct+=1
            if hijo_V[3]>=410 and hijo_V[3]>padre_V[3]:
                correct+=1
            if correct>3:
                padre_V=hijo_V
                padre=hijo
                H+=1
            HT+=1
            i+=1
            hijo=mutacion(padre)
            hijo_V=evaluete(hijo)
            i_t+=1
        e_c=H/HT
        if e_c>0.2:
            σ=σ/e_c
        elif e_c==0.2:
            continue
        else:
            σ=σ*c
#         print(σ)
            
    return hijo


# In[9]:


coeficientes=[seleccion_nat(result) for i in range(0, 100)]
coe=np.dot(coeficientes, 100) 
coef=pd.DataFrame(data=coe, columns=["Mat_B %", "Mat_C %", "Mat_D %" ])
coef['Mat_A %']=20

b=[evaluete(i) for i in coeficientes]


df =pd.DataFrame(data=b, columns=["Costo", "Dureza", "Peso", "D_Calor" ])
df=pd.merge(df, coef, left_index=True, right_index=True)
df=df[df.Dureza > 400]
df=df[df.D_Calor > 410]
df=df[df.Peso <= 60]
df=df.sort_values('Costo')
df=df.reset_index()
df=df.drop(['index'], axis=1)
print(df.head(10))

