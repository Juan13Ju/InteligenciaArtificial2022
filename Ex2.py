import numpy as np
# Juarez Ubaldo Juan Aurelio - 421095568
class genAlgo:
    def __init__(self, n_pop, iter, r_cross, r_mut, longitud):
        # El tamaño de la poblacion
        self.n_pop = n_pop
        # El numero de generaciones a simular
        self.iter = iter
        # crossover rate
        self.r_cross = r_cross
        # mutation rate
        self.r_mut = r_mut
        # Longitud de la representacion binaria del numero entrada
        self.longitud = longitud

    def fitness(self, gen):
        # Esto es para pasar de la representacion binaria a int porque me pide un string
        genstr = [str(i) for i in gen]

        x = "".join(genstr)
        # Pasamos el gen de binario a entero decimal
        num = int(x,2)
        return 100 - ((num-10)**4) + (50*((num-10)**2)) - (8 * num) 
    
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
            pt = np.random.randint(0, len(p1)-2)
            c1 = p1[:pt] + p2[pt:]
            c2 = p2[:pt] + p1[pt:]
        return [c1, c2]

    def mutation(self, gen):
        for i in range(len(gen)):
            if(np.random.rand() < self.r_mut):
                gen[i] = np.random.randint(0, 2)

    def geneticAlgo(self):
        # Primero generamos la poblacion inicial
        pop = [np.random.randint(0,2, self.longitud).tolist() for _ in range(self.n_pop)]
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

gen = genAlgo(10, 50, .3, .9, 10)
res = gen.geneticAlgo()
print(f"El mejor gen es : {res[0]}, con valor : {res[1]}")