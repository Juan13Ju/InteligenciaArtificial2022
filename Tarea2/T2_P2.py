import numpy as np
class genAlgo:
    def __init__(self, n_pop, iter, r_cross, r_mut, tablero = 8):
        # Aqui definimos el tamaño del tablero  
        self.tablero = tablero
        # Tamaño de la poblacion
        self.n_pop = n_pop
        # Numero de generaciones
        self.iter = iter
        # crossover rate
        self.r_cross = r_cross
        # mutation rate
        self.r_mut = r_mut
        # El numero maximo de conflictos para el tamaño del tablero
        self.maxConflicts = self.getMaxConflicts()

    # Funcion para determinar los conflictos de un gen
    def countConflicts(self, gen):
        conflictos = 0
        for i in range(self.tablero):
            for j in range(i+1, self.tablero):
                # Conflictos horizontales
                if(gen[i] == gen[j]):
                    conflictos = conflictos + 1
                # Conflictos diagonales
                if(abs(i-j) == abs(gen[i] - gen[j])):
                    conflictos = conflictos + 1
        return conflictos


    # Funcion para determinar la mayor cantidad de conflictos para un tamaño de tabla
    def getMaxConflicts(self):
        # Ya que aun no se me ocurre una formula, pero creo tener la idea de como generar una configuracion
        # con el mayor numero de conflictos, vamos a generar esa configuracion y contar los conflictos
        gen = list()
        # La idea es que para maximizar los conflictos, cada reina estara en conflicto con otra en la diagonal
        # y otra en la horizontal
        for i in range(self.tablero):
            # if( i % 2 == 0):
            #     gen.append(0)
            # else:
            #     gen.append(1)
            gen.append(0)
        
        # Ahora contamos el numero de conflictos
        maxConflicts = self.countConflicts(gen)
        print(f"El mayor numero de conflictos para {self.tablero} reinas es : {maxConflicts}")
        return maxConflicts

    # Funcion que determina el fitness de un gen en particular
    def fitness(self, gen):
        return self.maxConflicts - self.countConflicts(gen)

    def selection(self, pop, scores, k=3):
        # first random selection
        selection_ix = np.random.randint(len(pop))
        for ix in np.random.randint(0, len(pop), k-1):
            if(scores[ix] > scores[selection_ix]):
                selection_ix = ix
        return pop[selection_ix]

    def crossover(self, p1, p2):
        c1, c2 = p1.copy(), p2.copy()
        if(np.random.rand() < self.r_cross):
            pt = np.random.randint(1, len(p1)-2)
            c1 = p1[:pt] + p2[pt:]
            c2 = p2[:pt] + p1[pt:]
        return [c1, c2]

    def mutation(self, gen):
        for i in range(len(gen)):
            if(np.random.rand() < self.r_mut):
                gen[i] = np.random.randint(0, self.tablero)

    def geneticAlgo(self):
        # Primero generamos la poblacion inicial
        pop = [np.random.randint(0,self.tablero-1, self.tablero).tolist() for _ in range(self.n_pop)]
        best = 0
        bestEval = float("-inf")
        for generation in range(self.iter):
            scores = [self.fitness(g) for g in pop]
            for i in range(self.n_pop):
                if(scores[i] > bestEval):
                    best = pop[i]
                    bestEval = scores[i]
                    print(f"El nuevo mejor gen es : {best}, con fitness : {bestEval}")
            # Elegimos a los mejores genes
            selected = [self.selection(pop, scores) for _ in range(self.n_pop)]
            # Creamos la siguiente generacion
            children = list()
            for i in range(0, self.n_pop, 2):
                p1,p2 = selected[i], selected[i+1]
                # Crossover y mutacion
                for c in self.crossover(p1,p2):
                    self.mutation(c)
                    children.append(c)
            pop = children
        return [best, bestEval]


# Modificar aqui (numero de poblacion, iteraciones, crossover rate, mutation rate, tamaño de tablero)
# Tamaño de tablero es opcional y el valor por default es 8
# Nota : El numero de poblacion debe ser par
nPob = int(input("Ingresa un numero de poblacion por generacion (Debe ser par): "))
it = int(input("Ingresa cuantas generaciones deseas simular: "))
cross = float(input("Ingresa un valor de r_cross en [0,1): "))
mut = float(input("Ingresa un valot de r_mut en [0,1): "))
tablero = int(input("Ingresa un entero con el tamaño del tablero: "))
p = genAlgo(nPob, it, cross, mut, tablero)
mejor = p.geneticAlgo()
mejorGen = mejor[0]
print("----------------")
print(f"La mejor solucion: {mejorGen}")
c = p.countConflicts(mejorGen)
f = p.fitness(mejorGen)
print(f"Conflictos de la solucion : {c}")
print(f"Fitness de la solucion : {f}")