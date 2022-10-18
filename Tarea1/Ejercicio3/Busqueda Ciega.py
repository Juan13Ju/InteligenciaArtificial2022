#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[1]:


from collections import deque
 
# Creamos la clase para un grafo
class Grafo:
 
    v_grado = None # almacena el grado de un vértice
 
    
    def __init__(objeto, edges, n):

        objeto.adjLista = [[] for _ in range(n)] # Crea una lista de adyacencia

        objeto.v_grado = [0] * n # Pone el grado de cada vértice en 0 
 
        # agrega los edges al grafo
        for (org, dest) in edges:
 
            objeto.adjLista[org].append(dest) # agrega un edge desde el origen hasta 
                                              # el destino
 
            objeto.v_grado[dest] = objeto.v_grado[dest] + 1 # incrementa el grado del  
                                                            # vértice de destino en 1
 
 
# Función para realizar una ordenación topológica 
def TopologicalSort(grafo, n):
 
    L = []  # Lista # para almacenar los elementos ordenados

    v_grado = grafo.v_grado # obtener inarray en grado del grafo
 
    G = deque([i for i in range(n) if v_grado[i] == 0]) # Conjunto de todos los nodos
                                                        # sin bordes entrantes
 
    while G:

        n = G.pop() # elimina el nodo n de G
 
        L.append(n) # añade n al final de L
 
        for m in grafo.adjLista[n]:
            
            v_grado[m] = v_grado[m] - 1 # elimina una arista de n a m del grafo
 
            # si m no tiene otros bordes entrantes, inserte m en G
            if v_grado[m] == 0:
                G.append(m)
 
    # si un grafo tiene bordes, entonces el grafo tiene al menos un ciclo
    for i in range(n):
        if v_grado[i]:
            return None
 
    return L

 
if __name__=='__main__':

     
    edges = [(0,4), (0, 2), (1, 3), (1, 2), (2, 4), (3, 2), (3, 0)] # Lista de edges 
                                                                    # del grafo
    n = 5 # número total de nodos en el grafo

    grafo = Grafo(edges, n) # construye un grafo a partir de los edges dados
 
    L = TopologicalSort(grafo, n) # Realizar clasificación topológica
 
    if L:
        print(L)    
    else:
        print('Topological sorting no es posible, el grafo tiene un ciclo')

