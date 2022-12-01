import numpy as np


class tablero:
  def __init__(self):
    self.mesa = np.zeros((8,8))
    self.turno = 2
    
  def poner_ficha(self, pos, turno = None):
    if turno == None:
      turno = self.turno
    casillas_vacias = np.count_nonzero(self.mesa)
    #print(f'Posición: {pos} | Turno: {turno} | Casillas llenas: {casillas_vacias}')
    #Condición de las primeras tiradas
    if (casillas_vacias == 0 or casillas_vacias == 2 ) and turno == 2:
      if pos in self.calcular_posibles():
        self.mesa[pos] = turno
        self.turno = 1
      else:
        print('Posicion incorrecta')
    elif (casillas_vacias == 1 or casillas_vacias == 3 )and turno == 1:
      if pos in self.calcular_posibles():
        self.mesa[pos] = turno
        self.turno = 2
      else:
        print('Posicion incorrecta2')
    #Juego normal
    elif casillas_vacias >= 4:
      #print('Debes calcular las posibles')
      #print(self.calcular_posibles())
      if pos in self.calcular_posibles():
        #print('Jugada aceptable')
        self.mesa[pos] = self.turno
        cap = []
        # rectas
        cap += self.pos_izq(pos)
        cap += self.pos_der(pos)
        cap += self.pos_arr(pos)
        cap += self.pos_aba(pos)
        # diag
        cap += self.pos_aba_der(pos)
        cap += self.pos_aba_izq(pos)
        cap += self.pos_arr_der(pos)
        cap += self.pos_arr_izq(pos)
        cap = list(set(cap))
        for cap_aux in cap:
          self.mesa[cap_aux] = self.turno
        if self.turno == 1:
          self.turno = 2
        elif self.turno == 2:
          self.turno = 1
      else:
        #print('Jugada Inaplicable')
        if len(self.calcular_posibles()) == 0:
          print(pos,': No hay mas jugadas ')
        else:
          print(pos,': Jugada Invalida ')
  #--------------------Calculamos las jugada posible usando el Turno Interno-------------------------------------------------------------------
  def calcular_posibles(self):
    casillas_vacias = np.count_nonzero(self.mesa)
    if casillas_vacias == 0 and self.turno == 2:
      posibles = [(3,3),(3,4),(4,3),(4,4)]
      return posibles
    elif 4 > casillas_vacias >= 1:
      posibles = [(3,3),(3,4),(4,3),(4,4)]
      posibles_aux = []
      for aux in posibles:
        if self.mesa[aux] == 0:
          posibles_aux.append(aux)
      posibles = posibles_aux
      return posibles
    else:
      posibles = []
      for m_i in range(8):
        for m_j in range(8):
          if self.mesa[m_i,m_j] == 0:
            cap = []
            # rectas
            cap += self.pos_izq((m_i,m_j))
            cap += self.pos_der((m_i,m_j))
            cap += self.pos_arr((m_i,m_j))
            cap += self.pos_aba((m_i,m_j))
            # diag
            cap += self.pos_aba_der((m_i,m_j))
            cap += self.pos_aba_izq((m_i,m_j))
            cap += self.pos_arr_der((m_i,m_j))
            cap += self.pos_arr_izq((m_i,m_j))
            cap = list(set(cap)) # cap = [(2,2),(1,1),(2,2)] -> cap = [(2,2),(1,1)]
            if len(cap) > 0 :
              posibles.append((m_i,m_j))      
      return posibles
  #--------------Verticales y Horizontales-------------------------------------
  #Recorremos para izquierda
  def pos_izq(self,pos_aux):
    #print(f'Turno: {self.turno} pos_izq')
    #Necesitamos saber las casillas capturadas.
    casillas = []
    mesa_aux = self.mesa[pos_aux[0],:pos_aux[1]]

    for ind, aux in enumerate(reversed(mesa_aux)):
      #print(f'ind,aux: {(ind, aux)} mesaR:{ mesa_aux}')
      casillas.append((pos_aux[0],pos_aux[1]-ind))
      #Revisamos que exita la primer ficha 
      if ind == 0 and (aux == 0 or aux == self.turno):
        #print(f'Pos Invalid {aux} si 0 -> No hay ficha final, 2 -> No se captura nada')
        return []
      if ind > 0 and aux == 0:
        #print('No hay vecino del Turno contrario antes')
        return []
      if aux == self.turno:
        ##print('Encontramos la ultima')
        casillas.pop(0)
        #print('Encontramos la ultima')
        return casillas
    return []

  #Recorremos para derecha
  def pos_der(self,pos_aux):
    #print(f'Turno{self.turno} pos_der')
    #Necesitamos saber las casillas capturadas.
    casillas = []
    mesa_aux = self.mesa[pos_aux[0], pos_aux[1]+1:]

    for ind, aux in enumerate(mesa_aux):
      #print(f'ind,aux: {(ind, aux)} mesa:{ mesa_aux }')
      casillas.append((pos_aux[0],pos_aux[1]+ind))
      #Revisamos que exita la primer ficha 
      if ind == 0 and (aux == 0 or aux == self.turno):
        #print(f'Pos Invalid {aux} si 0 -> No hay ficha final, 2 -> No se captura nada')
        return []
      if ind > 0 and aux == 0:
        #print('No hay vecino del Turno contrario antes')
        return []
        #break
      if aux == self.turno:
        ##print('Encontramos la ultima')
        casillas.pop(0)
        #print('Encontramos la ultima')
        return casillas
        
    return []
  #Recorremos para abajo
  def pos_aba(self,pos_aux):
    #print(f'Turno{self.turno} pos_aba')
    #Necesitamos saber las casillas capturadas.
    casillas = []
    mesa_aux = self.mesa[pos_aux[0]+1:, pos_aux[1]]

    for ind, aux in enumerate(mesa_aux):
      #print(f'ind,aux: {(ind, aux)} mesa : {mesa_aux}')
      casillas.append((pos_aux[0]+ind,pos_aux[1]))
      #Revisamos que exita la primer ficha 
      if ind == 0 and (aux == 0 or aux == self.turno):
        #print(f'Pos Invalid {aux} si 0 -> No hay ficha final, 2 -> No se captura nada')
        return []
      if ind > 0 and aux == 0:
        #print('No hay vecino del Turno contrario antes')
        return []
      if aux == self.turno:
        casillas.pop(0)
        #print('Encontramos la ultima')
        return casillas
    return []

#Recorremos para arriba
  def pos_arr(self,pos_aux):
    #print(f'Turno: {self.turno} pos_arr')
    
    #Necesitamos saber las casillas capturadas.
    casillas = []
    mesa_aux = self.mesa[:pos_aux[0], pos_aux[1]]

    for ind, aux in enumerate(reversed(mesa_aux)):
      #print(f'ind,aux: {(ind, aux)} mesa : {mesa_aux}')
      casillas.append((pos_aux[0]-ind,pos_aux[1]))
      #Revisamos que exita la primer ficha 
      if ind == 0 and (aux == 0 or aux == self.turno):
        #print(f'Pos Invalid {aux} si 0 -> No hay ficha final, 2 -> No se captura nada')
        return []
      if ind > 0 and aux == 0:
        #print('No hay vecino del Turno contrario antes')
        return []
      if aux == self.turno:
        casillas.pop(0)
        #print('Encontramos la ultima')
        return casillas
        
    return []
  #---------------Diagonales-----------------------------------
  
  # Diagonal arriba e izquierda
  def pos_arr_izq(self,pos_aux):
    #print(f'Turno: {self.turno} pos_arr_izq')
    #Necesitamos saber las casillas capturadas.
    casillas = []
    #print(f'pos_aux:{pos_aux}')
    
    for cont, ind_ax in enumerate(range(0, max(pos_aux[0],pos_aux[1]))):
      #print(cont, ind_ax,'count,aux')
      
      coor = (pos_aux[0] - cont, pos_aux[1] - cont)
      #print('coor', coor)
      casillas.append(coor)
      if cont == 1 and self.mesa[coor] == self.turno:
        #print('Misma pieza sin camturar',self.mesa[coor])
        return []
      elif cont == 1 and self.mesa[coor] == 0:
        #print('Movimiento sin ficha vecina',self.mesa[coor])
        return []
      if cont > 1 and self.mesa[coor] == 0:
        #print('No hay vecina del turno antes del final')
        return []
      if cont > 1 and self.mesa[coor] == self.turno:
        #print('Se encontro la piesa')
        casillas.pop(-1)
        casillas.pop(0)
        return casillas
    return []
  
  # Diagonal abajo y derecha
  def pos_aba_der(self,pos_aux):
    #print(f'Turno: {self.turno} pos_aba_der')
    #Necesitamos saber las casillas capturadas.
    casillas = []
    #print(f'pos_aux:{pos_aux}')
    #recorremos
    for cont, ind_ax in enumerate(range(max(pos_aux[0],pos_aux[1]),8)):
      #print(cont, ind_ax,'count,aux')
      coor = (pos_aux[0] + cont, pos_aux[1] + cont) 
      #print(coor ,'coor')
      casillas.append(coor)
      if cont == 1 and self.mesa[coor] == self.turno:
        #print('Misma pieza sin camptura', self.mesa[coor])
        return []
      elif cont == 1 and self.mesa[coor] == 0:
        #print('Movimiento sin ficha vecina',self.mesa[coor])
        return []
      if cont > 1 and self.mesa[coor] == 0:
        #print('No hay vecina del turno antes del final')
        return []
      if cont > 1 and self.mesa[coor] == self.turno:
        #print('Se encontro la piesa aliada')
        casillas.pop(-1)
        casillas.pop(0)
        return casillas
    return []
  # Diagonal abajo e izqquieda
  def pos_aba_izq(self,pos_aux):
    ##print(f'Turno: {self.turno} pos_aba_izq')
    #Necesitamos saber las casillas capturadas.
    casillas = []
    #print(f'pos_aux:{pos_aux}')
    #for ind_ax in range(1,min(pos_aux[0],pos_aux[1])+1):
    for cont, ind_ax in enumerate(range(max(pos_aux[0],pos_aux[1]),8)):
      #print(cont, ind_ax,'count,aux')
      coor = (pos_aux[0] + cont, pos_aux[1] - cont)
      #print('coor', coor)
      casillas.append(coor)
      if cont == 1 and self.mesa[coor] == self.turno:
        #print('Misma pieza sin camturar',self.mesa[coor])
        return []
      elif cont == 1 and self.mesa[coor] == 0:
        #print('Movimiento sin ficha vecina',self.mesa[coor])
        return []
      if cont > 1 and self.mesa[coor] == 0:
        #print('No hay vecina del turno antes del final')
        return []
      if cont > 1 and self.mesa[coor] == self.turno:
        #print('Se encontro la piesa')
        casillas.pop(-1)
        casillas.pop(0)
        return casillas
    return []
  # Diagonal arriba y derecha
  def pos_arr_der(self,pos_aux):
    #print(f'Turno: {self.turno} pos_arr_der')
    #Necesitamos saber las casillas capturadas.
    casillas = []
    #print(f'pos_aux:{pos_aux}')
    #for ind_ax in range(1,min(pos_aux[0],pos_aux[1])+1):
    for cont, ind_ax in enumerate(range(max(pos_aux[0],pos_aux[1]),8)):
      #print(cont, ind_ax,'count,aux')
      
      coor = (pos_aux[0] - cont, pos_aux[1] + cont)
      #print('coor', coor)
      casillas.append(coor)
      if cont == 1 and self.mesa[coor] == self.turno:
        #print('Misma pieza sin camturar',self.mesa[coor])
        return []
      elif cont == 1 and self.mesa[coor] == 0:
        #print('Movimiento sin ficha vecina',self.mesa[coor])
        return []
      
      if cont > 1 and self.mesa[coor] == self.turno:
        #print('Se encontro la piesa')
        casillas.pop(-1)
        casillas.pop(0)
        return casillas
    return []
  #------------------------------------------------------------------19------09 -----------------------2022------------------------
  # Definimos una función que calcula el valor del tablero
  def score_tab (self):
    #Vamos a contar el número de fichas de color blanco 1 y las de color negro 2
    x = np.count_nonzero(self.mesa == 2) # ¿Cuantas fichas negras hay?
    y = np.count_nonzero(self.mesa == 1) # ¿Cuantas fichas blancas hay?
    return (x,y)
  #Funcion de valor
  def val_fun(self):
    posibles = self.calcular_posibles()
    val_list = []
    for tir_var in posibles:
      tablero_ax = tablero()
      tablero_ax.mesa = self.mesa.copy()
      tablero_ax.turno = self.turno
      tablero_ax.poner_ficha(tir_var)
      ng_val, bl_val = tablero_ax.score_tab()
      val_list.append(ng_val-bl_val)
    return val_list

## MINMAX
class Arbol:
  def __init__(self, tab: tablero, depth, tirada = None):
    self.raiz = tab
    self.depth = depth
    self.hijos = []
    if(tirada != None):
      # tirada que se realizo para llegar a ese estado
      self.tirada = tirada
    else:
      # Para la raiz del arbol
      self.tirada = (0,0)
  def expandirArbol(self):
    self.hijos = self.generarHijos()
    if(self.depth > 0):
      for hijo in self.hijos:
        hijo.expandirArbol()

  def generarHijos(self):
    posibles = self.raiz.calcular_posibles()
    hijos = []
    for pos in posibles:
      # En cada iteracion creamos una copia del tablero original y lo agregamos a la lista de hijos
      # despues de agregar una ficha en un lugar posible
      tableroHijo = tablero()
      mesaHijo = np.array([row[:] for row in self.raiz.mesa])
      tableroHijo.mesa = mesaHijo
      tableroHijo.turno = self.raiz.turno
      tableroHijo.poner_ficha((pos[0], pos[1]))
      hijo = Arbol(tableroHijo, self.depth-1, (pos[0], pos[1]))
      hijos.append(hijo)
    return hijos

  def minMax(self, maximizingPlayer):
    if len(self.hijos) == 0:
      score = self.raiz.score_tab()
      value = score[0] - score[1]
      print(f"x : {score[0]}, y : {score[1]}")
      return (value, self.tirada)

    # Jugador max
    maxEva = float("-inf")
    if maximizingPlayer:
      for hijo in self.hijos:
        result = hijo.minMax(False)
        eva = result[0]
        if eva > maxEva:
          maxEva = eva
          self.mejorTirada = result[1]
      return (maxEva, self.tirada)
    else:
      # Jugador min
      minEva = float("inf")
      for hijo in self.hijos:
        result = hijo.minMax(True)
        eva = result[0]
        if eva < minEva:
          minEva = eva
          self.mejorTirada = result[1]
      return (minEva, self.tirada)
