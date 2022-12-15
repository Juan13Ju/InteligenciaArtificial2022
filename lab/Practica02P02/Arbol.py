import numpy as np
import itertools
from queue import Queue
class Arbol:
    def __init__(self, vision, posInicial, depth = None, movimiento = None):
        self.vision = vision
        if(depth == None):
            self.depth = 2 * BFSdist(self.vision, posInicial, v = True)
        else:
            self.depth = depth
        self.posInicial = posInicial
        self.largo = len(vision)
        self.ancho = len(vision)
        self.agentes = list()
        self.hijos = []
        # Encontramos la posicion de los agentes
        for i in range(len(vision)):
            for j in range(len(vision)):
                if(vision[i][j] == 2):
                    self.agentes.append([i,j])
        # Para la raiz del arbol
        if(movimiento != None):
            self.movimiento = movimiento
        else:
            self.movimiento = (0,0)
        

    # Expande el arbol tomando en cuenta que se mueve la aspiradora
    def expandirArbolAsp(self):
        self.hijos = self.generarHijosAsp()
        # print(f"Hijos generados : {[h.vision for h in self.hijos]}")
        if(self.depth > 0):
            for hijo in self.hijos:
                hijo.expandirArbolAgentes()

    # Expande el arbol tomando en cuenta que se mueven los agentes
    def expandirArbolAgentes(self):

        self.hijos = self.generarHijosAgentes()

        if(self.depth > 0):
            for hijo in self.hijos:
                hijo.expandirArbolAsp()

    # Generemos un hijo por cada movimiento permitido de la aspiradora
    def generarHijosAsp(self):
        # Lo llamamos con 0,0 ya que en el metodo estos parametros no se tomaran en cuenta
        posibles = self.calcularPosibles(0,0)
        hijos = list()
        for pos in posibles:
            
            visionHijo = np.array([row[:] for row in self.vision])
            posHijo = [self.posInicial[0] + pos[0], self.posInicial[1] + pos[1]]
    
            visionHijo[self.posInicial[0]][self.posInicial[1]] = 0
            visionHijo[posHijo[0]][posHijo[1]] = 4
            
            hijo = Arbol(visionHijo, posHijo, self.depth-1, pos)
            hijos.append(hijo)
        
        return hijos
    
    # Genereamos un hijo por cada combinacion de movimientos de los agentes
    # notamos que entre mas agentes, sera mas tardado
    def generarHijosAgentes(self):
        # En caso de que no haya agentes, devolvemos el cuarto
        if(len(self.agentes) == 0):
            arbol = Arbol(np.array([row[:] for row in self.vision]), self.posInicial, self.depth-1)
            return [arbol]
        
        movAgentes = list()
        for agente in self.agentes:
            posibles = self.calcularPosibles(agente[0], agente[1], True) # Calculamos los posibles de cada agente
            movAgentes.append(posibles)
        combMovimientos = list(itertools.product(*movAgentes))
        hijos = list()
        for i in range(len(combMovimientos)):
            visionHijo = np.array([row[:] for row in self.vision])
            for j in range(len(self.agentes)):
                # Coordenadas actuales de los agentes
                iPos = self.agentes[j][0]
                jPos = self.agentes[j][1]
                visionHijo[iPos][jPos] = 0
                visionHijo[iPos + combMovimientos[i][j][0]][jPos + combMovimientos[i][j][1]] = 2
                hijo = Arbol(visionHijo, self.posInicial, self.depth-1, combMovimientos[i])
                hijos.append(hijo)
        return hijos



    def calcularPosibles(self, i,j, aspiradora = False):

        if(not aspiradora):
            i = self.posInicial[0]
            j = self.posInicial[1]

        direcciones = [(1,0), (-1,0), (0,1), (0,-1)]
        posibles = list()
        for dir in direcciones:
            # Se puede ir en esa direccion
            if((i + dir[0]) >= 0 and (i + dir[0]) < self.largo and (j + dir[1]) < self.ancho and (j + dir[1]) >= 0):
                # No hay otro agente u loseta sucia en esa direccion
                if(not aspiradora):
                    if(self.vision[i + dir[0]][j + dir[1]] == 0 or self.vision[i + dir[0]][j + dir[1]] == 3):
                        posibles.append(dir)
                else:
                    if(self.vision[i + dir[0]][j + dir[1]] == 0):
                        posibles.append(dir)

        return posibles

    def evaluarVision(self):
        # Contamos el numero de losetas sucias
        score = 0
        
        for i in range(self.largo):
            for j in range(self.ancho):
                if(self.vision[i][j] == 3):
                    score = score - 1
                    
                elif(self.vision[i][j] == 0):
                    score = score + 2
        score = score - BFSdist(self.vision,self.posInicial)
        
        return score
        
    def minMax(self, maximizingPlayer, alfa = None, beta = None): # True si es turno de la aspiradora
        if(len(self.hijos) == 0):
            score = self.evaluarVision()
            return (score, self.movimiento, self.vision)

        if(alfa == None):
            alfa = float("-inf")
        if(beta == None):
            beta = float("inf")
        
        if(maximizingPlayer):
            
            maxEva = float("-inf")
            
            for hijo in self.hijos:
                result = hijo.minMax(False, alfa, beta)
                eva = result[0]
                if(eva > maxEva):
                    maxEva = eva
                    self.mejorMovimiento = result[1]
                    # print(f"Mejor sig : \n {result[2]}")
                    alfa = max(alfa, maxEva)
                    if(beta <= alfa):
                        
                        break
            
            return (maxEva, self.movimiento, self.vision)
        else:
            minEva = float("inf")
            for hijo in self.hijos:
                
                result = hijo.minMax(True, alfa, beta)
                eva = result[0]
                if eva < minEva:
                    minEva = eva
                    self.mejorMovimiento = result[1]
                    beta = min(beta, minEva)
                    if(beta <= alfa):
                        
                        break
                    
            return (minEva, self.movimiento, self.vision)

# Nos regresa la distancia mas corta para limpiar cada loseta sucia
def BFSdist(arr, posInicial, n = 0, visitados = None, v = False):
    if(visitados == None):
        visitados = []
    q = Queue()
    q.put((posInicial[0], posInicial[1], n))
    while(not q.empty()):
        actual = q.get()
        x = actual[0]
        y = actual[1]
        dist = actual[2]
        visitados.append([x,y])
        for pos in calcularPosiblesAux(arr, x ,y):
            if [x+pos[0], y + pos[1]] not in visitados:
                if(arr[x+pos[0]][y+pos[1]] == 3):
                    
                    return dist + 1 + BFSdist(arr, [x+pos[0], y+pos[1]], 0, visitados)
                q.put((x+pos[0], y+pos[1], dist+1)) 

    return 0

def calcularPosiblesAux(vision, i,j, aspiradora = False):

        direcciones = [(1,0), (-1,0), (0,1), (0,-1)]
        posibles = list()
        for dir in direcciones:
            # Se puede ir en esa direccion
            if((i + dir[0]) >= 0 and (i + dir[0]) < len(vision) and (j + dir[1]) < len(vision) and (j + dir[1]) >= 0):
                # No hay otro agente u loseta sucia en esa direccion
                # Este dice nos aspiradora pero quiere decir que si es la aspiradora xd
                if(not aspiradora):
                    if(vision[i + dir[0]][j + dir[1]] == 0 or vision[i + dir[0]][j + dir[1]] == 3):
                        posibles.append(dir)
                else:
                    if(vision[i + dir[0]][j + dir[1]] == 0):
                        posibles.append(dir)

        return posibles
