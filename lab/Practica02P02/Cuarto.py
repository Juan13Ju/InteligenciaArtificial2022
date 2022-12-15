import numpy as np
import random
from queue import Queue
from Arbol import Arbol
# Clase que simula el cuarto en el cual se encuentra la aspiradora
class cuarto:
    # 0 - Espacio libre y limpio
    # 1 - Obstaculo inanimado
    # 2 - Obstaculo animado
    # 3 - Espacio libre y sucio
    # 4 - Donde se encuentra la aspiradora
    def __init__(self, largo, ancho, rangoVision):
        # Por ahora tomamos el numero de losetas en vez de las medidas
        self.largo = largo
        self.ancho = ancho
        self.espacio = np.zeros((largo, ancho))
        self.agentes = []
        self.rangoVision = rangoVision

    # Agrega los obstaculos inmoviles
    def agregarInmoviles(self, arr):

        for coord in arr:
            self.espacio[coord] = 1
    # Agrega los obstaculos moviles
    def agregarMoviles(self, arr):
        self.agentes = arr
        for agente in self.agentes:
            i = agente[0]
            j = agente[1]
            self.espacio[i][j] = 2
    # Agrega las coordenadas de la suciedad
    def agregarSuciedad(self, arr):
       for coord in arr:
            self.espacio[coord] = 3
    # Agrega la posicion inicial de la aspiradora. Solo puede haber 1 aspiradora
    def agregarAspiradora(self, pos):
        self.aspiradoraPos = pos
        self.espacio[pos[0]][pos[1]] = 4

    # Genera la vision de la aspiradora de acuerdo a su rango de vision
    def generarVistaAspiradora(self):
        # -1 invisible
        # 0 - Espacio libre y limpio
        # 1 - Obstaculo inanimado
        # 2 - Obstaculo animado
        # 3 - Espacio libre y sucio
        # 4 - Donde se encuentra la aspiradora
        self.visionAsp = np.full((2*self.rangoVision+1, 2*self.rangoVision+1), -1)
        q = Queue()
        visitados = list()
        # La ubicacion relativa a la vision del robot
        x = self.rangoVision
        y = self.rangoVision
        # La ubicacion en el cuarto
        i = self.aspiradoraPos[0]
        j = self.aspiradoraPos[1]
        q.put((i, j, x, y, 0))
        posInicial = (x,y)
        while(not q.empty()):
            actual = q.get()
            iPos = actual[0]
            jPos = actual[1]
            xPos = actual[2]
            yPos = actual[3]
            dist = actual[4]
            visitados.append((iPos, jPos))
            self.visionAsp[xPos][yPos] = self.espacio[iPos][jPos]
            
            posibles = self.calcularPosibles(iPos,jPos, True)
            for dir in posibles:
                if(dist < 3 and (iPos + dir[0], jPos + dir[1]) not in visitados):
                    q.put([iPos + dir[0], jPos + dir[1], xPos + dir[0], yPos + dir[1], dist+1])

        self.visionAsp[posInicial] = 4

    # Movemos a la aspiradora de forma inteligente usando minmax
    def moverAspiradora(self):
        # En donde estamos
        i = self.aspiradoraPos[0]
        j = self.aspiradoraPos[1]
        # Si no detecta suciedad, entonces genera un movimiento aleatorio
        if(np.all(self.visionAsp != 3)):
            print("Ya que no detectamos suciedad, nos movemos aleatoriamente...")
            posibles = self.calcularPosibles(self.aspiradoraPos[0], self.aspiradoraPos[1])
            dir = random.choice(posibles)
            x = dir[0]
            y = dir[1]
            print(f"Direccion de movimiento aleatoria: {(x,y)}")
            print(f"Moviendonos a : {x+i, y+j}")
            self.espacio[i][j] = 0
            self.espacio[i + x][j + y] = 4
            self.aspiradoraPos[0] = i + x
            self.aspiradoraPos[1] = j + y
            return

        arbol = Arbol(self.visionAsp, [self.rangoVision, self.rangoVision])
        arbol.expandirArbolAsp()
        arbol.minMax(True)
        # print([h.vision for h in arbol.hijos])
        # A donde nos vamos a mover
        x = arbol.mejorMovimiento[0]
        y = arbol.mejorMovimiento[1]
        

        print(f"Pos : {self.aspiradoraPos}")
        print(f"Direccion elegida : {(x,y)}")
        print(f"Moviendome a : {(i+x, j+y)}")
        self.espacio[i][j] = 0
        if(self.espacio[i + x][j + y] == 3):
            print("Limpiando... no estorben")
        self.espacio[i + x][j + y] = 4
        self.aspiradoraPos[0] = i + x
        self.aspiradoraPos[1] = j + y


    # Movemos a los agentes en una de las 4 direcciones posibles
    def moverAgentes(self):
        # Primero encontramos al agente movil
        for agente in self.agentes:
            i = agente[0]
            j = agente[1]
            if(self.espacio[i][j] == 2):
                pos = self.calcularPosibles(i,j)
                direccion = random.choice(pos)
                self.espacio[i][j] = 0
                self.espacio[i + direccion[0]][j + direccion[1]] = 2
                agente[0] = i + direccion[0]
                agente[1] = j + direccion[1]

    # Calcula las posibles direcciones de movimiento           
    def calcularPosibles(self, i,j, aspiradora = False):
        
        direcciones = [(1,0), (-1,0), (0,1), (0,-1)]
        posibles = list()
        for dir in direcciones:
            # Se puede ir en esa direccion
            if((i + dir[0]) >= 0 and (i + dir[0]) < self.largo and (j + dir[1]) < self.ancho and (j + dir[1]) >= 0):
                # No hay otro agente u loseta sucia en esa direccion
                if(not aspiradora):
                    if(self.espacio[i + dir[0]][j + dir[1]] == 0):
                        posibles.append(dir)
                else:
                    if(self.espacio[i + dir[0]][j + dir[1]] == 0 or self.espacio[i + dir[0]][j + dir[1]] == 3):
                        posibles.append(dir)
                    
        return posibles
    # Agregamos suciedad aleatoriamente dada una probabilidad
    def suciedadAleatoria(self):
        prob = 0.01
        for i in range(self.ancho):
            for j in range(self.largo):
                if(self.espacio[i][j] == 0):
                    if(np.random.rand() < prob):
                        print("-------")
                        print(f"Agregando suciedad en {(i,j)}")
                        print("-------")
                        self.espacio[i][j] = 3


# Aqui para dimensiones del cuerto y vision del robot
# cuarto(largo, ancho, visionRobot)
c = cuarto(6,6,4)

# Aqui para colocar las cosas
# Agregar objetos inmoviles
c.agregarInmoviles([(0,0), (2,2)])
# Agregar objetos moviles
c.agregarMoviles([[2,4], [1,4]])
# Agregar suciedad inicial
c.agregarSuciedad([(1,1), (1,3), (3,3)])
# Agregar posicion de aspiradora, solo puede haber 1
c.agregarAspiradora([2,3])
print(c.espacio)
print("-----")
flag = True
while(flag):
    c.generarVistaAspiradora()
    c.moverAspiradora()
    c.moverAgentes()
    c.suciedadAleatoria()
    print(c.espacio)
    if(input("Deseas continuar? \n") == "n"):
        flag = False
    print("----------")
    
