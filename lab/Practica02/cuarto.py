import numpy as np
# Clase que simula el cuarto en el cual se encuentra la aspiradora
class cuarto:
    # 0 - Espacio libre y limpio
    # 1 - Obstaculo inanimado
    # 2 - Obstaculo animado
    # 3 - Espacio libre y sucio
    def __init__(self, largo, ancho):
        # Por ahora tomamos el numero de losetas en vez de las medidas
        self.largo = largo
        self.ancho = ancho
        self.espacio = np.zeros((largo, ancho))

    def agregarInmoviles(self, arr):

        for coord in arr:
            self.espacio[coord] = 1

    def agregarMoviles(self, arr):
        for coord in arr:
            self.espacio[coord] = 2

    def agregarSuciedad(self, arr):
       for coord in arr:
            self.espacio[coord] = 3

    # Movemos a los agentes en una de las 4 direcciones posibles
    def moverAgentes(self):
        # Primero encontramos al agente movil
        for i in range(self.largo):
            for j in range(self.ancho):
                if(self.espacio[i][j] == 2):
                    pos = self.calcularPosibles(i,j)
                    print(pos)

    
    def calcularPosibles(self, i,j):
        
        direcciones = [(1,0), (-1,0), (0,1), (0,-1)]
        posibles = list()
        for dir in direcciones:
            if((i + dir[0]) >= 0 and (i + dir[0]) < self.largo and (j + dir[1]) < self.ancho and (j + dir[1]) >= 0):
                posibles.append(dir)
        return posibles


c = cuarto(3,6)
print(c.espacio)
c.agregarInmoviles([(0,0), (2,2)])
c.agregarMoviles([(2,5)])
c.agregarSuciedad([(1,1), (0,4), (1,3)])
print(c.espacio)
c.moverAgentes()
