import seis_cuartos_o

class Simulation:

    def simulator(self, entorno, agent, steps=10, verbose=True):
        """
        Simulación de un agente en un entorno.
        @param entorno: Objeto de la clase Entorno.
        @param agent: Objeto de la clase Agent.
        @param steps: int con el número de pasos a simular.
        @param verbose: Si True, imprime el resultado de la simulación.
        @return: (states_record,actions_record,performance_record)
        Donde cada una es una lista con los estados, acciones y medida 
        de performance encontradas a lo largo de la simulación.
        """
        performance_record = [entorno.performance]
        states_record = [entorno.state[:]]
        actions_record = []

        for step in range(steps):
            p = entorno.perception()
            a = agent.programa(p)
            entorno.transition(a)
            performance_record.append(entorno.performance)
            states_record.append(entorno.state[:])
            actions_record.append(a)
        actions_record.append(None)

        if verbose:
            print(u"\n\nSimulación de entorno tipo " +
                str(type(entorno)) +
                " con el agent tipo " +
                str(type(agent)) + "\n"
            )
            print('Paso'.center(10) +
                u'Acción'.center(10) +
                u'Desempeño'.center(15) + 
                'Nuevo Estado'.ljust(40)
            )
            print('_' * (10 + 40 + 25 + 20))
            for i in range(steps):
                print(str(i).center(10) +
                    str(actions_record[i]).center(10) +
                    str(performance_record[i+1]).center(15) +
                    str(states_record[i+1]).ljust(40)
                )
            print('_' * (10 + 40 + 25 + 20) + '\n\n')
        return states_record, actions_record, performance_record

class Main:

    def test(self):
        """
        Se construye e imprime la simulación.
        """
        # Número de iteraciones.
        N = 100
        # Inicio de la simulación.
        simulation = Simulation()
        print("Prueba del entorno con un agente aleatorio")
        simulation.simulator(
            seis_cuartos_o.SeisCuartos(),
            seis_cuartos_o.AgenteAleatorio(),
            N
        )
        print("Prueba del entorno con un agente reactivo")
        simulation.simulator(
            seis_cuartos_o.SeisCuartos(),
            seis_cuartos_o.AgenteReactivoSeisCuartos(),
            N
        )
        print("Prueba del entorno con un agente reactivo con modelo")
        simulation.simulator(
            seis_cuartos_o.SeisCuartos(),
            seis_cuartos_o.AgenteReactivoModeloSeisCuartos(),
            N
        )

main = Main()
main.test()

# Se observa que es más eficiente el agente basado en modelos, le sigue
# el agente reactivo simple y el menos eficiente es el agente aleatorio.