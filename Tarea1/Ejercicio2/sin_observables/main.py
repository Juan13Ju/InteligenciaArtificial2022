import seis_cuartos

class Simulation:

    def simulator(self, entorno, agente, s, T=10, c=0):
        """
        Simulación de un agente en un entorno.
        @param entorno: Objeto de la clase Entorno.
        @param agente: Objeto de la clase Agent.
        @param s: Tupla con un estado legal del entorno.
        @param T: int con el número de pasos a simular.
        @param c: float con el costo hasta s.
        @return: [(a_1, s_1, c_1), ..., (a_T, s_T, c_T)] 
        Lista (record) de ternas con la acción, estado y costo total
        en cada paso de simulación.
        """
        action = agente.programa(entorno.perception(s))
        new_state, cost = entorno.transition(s, action)
        if T <= 1:
            record = [(action, new_state, c+cost)]
        else:
            record = [(action, new_state, c+cost)] + self.simulator(entorno, agente, new_state, T-1, c+cost)
        return record

    def print_simulation(self, record, s_0):
        """
        Imprime una secuencia generada por simulador.
        @param record: el resultado de simulador.
        @param s_0: estado inicial.
        """
        print("\n\nSimulación, iniciando en el estado: " + str(s_0) + "\n\n") 
        print(
            'Paso'.center(10) +
            'Acción'.center(12) +
            'Costo'.center(10) +
            'Nuevo Estado'.ljust(30)
        )
        print('_' * (10 + 20 + 25 + 47))

        for (i, (a_i, s_i, c_i)) in enumerate(record):
            print(
                str(i).center(10) +
                str(a_i).center(12) +
                str(c_i).center(10) +
                str(s_i).center(40)
            )
        print('_' * (10 + 20 + 25 + 47) + '\n\n')


class Main():

    def test(self, agent):
        """
        Se carga la información necesaria y se construye la simulación.
        """
        # Para el Agente Basado en Modelos, parece que va de A a F, pero 
        # eso es porque empieza en A. Si comienza con cualquier otra letra, 
        # el comportamiento cambia. 
        state = ('A', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio')
        # Número de iteraciones
        N = 100
        # Inicio de la simulación.
        simulation = Simulation()
        record = simulation.simulator(seis_cuartos.SeisCuartos(),agent,state,N)
        simulation.print_simulation(record, state)

    def print_test(self):
        """
        Imprime la simulación.
        """
        print("Prueba del entorno con un agente aleatorio.")
        self.test(seis_cuartos.AgenteAleatorio())
        print("Prueba del entorno con un agente reactivo")
        self.test(seis_cuartos.AgenteReactivoSeisCuartos())
        print("Prueba del entorno con un agente reactivo con modelo")
        self.test(seis_cuartos.AgenteReactivoModeloSeisCuartos())

main = Main()
main.print_test()

# Se observa que es más eficiente el agente basado en modelos, le sigue
# el agente reactivo simple y el menos eficiente es el agente aleatorio.