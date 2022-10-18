import entornos
from random import choice

class SeisCuartos(entornos.Entorno):
    """
    Estado: (robot,state_A,state_B,state_C,state_D,state_E,state_F)
    Los estados (state_A, etc) toman los valores: limpio o sucio.
    robot toma los valores: A, B, C, D, E o F.
    Acciones válidas: ('subir','bajar','derecha','izquierda','limpiar','nada')
    Sensores: (robot, robot_state).
    robot_state es el estado en el cual se encuentra el robot.
    Si robot = B, entonces robot_state = state_B.
    """

    def transition(self, state, action):
        """
        Función de transición de un estado a otro.
        Recibe un estado y una acción.
        Regresa la pareja (new_state, cost)
        """
        new_state = self.get_new_state(state, action)
        cost = self.check_cost(action)
        return (new_state, cost)

    def get_new_state(self, state, action):
        """
        Función auxiliar para transition().
        Recibe un estado y una acción.
        Regresa el nuevo (siguiente) estado new_state.
        """
        robot, sA, sB, sC, sD, sE, sF = state
        if action == 'nada':
            new_state = state
        elif (
            action == 'subir'
            or action == 'bajar'
            or action == 'derecha'
            or action == 'izquierda'):
            new_robot = self.new_robot(robot, action)
            new_state = (new_robot, sA, sB, sC, sD, sE, sF)
        elif action == 'limpiar':
            new_state = self.new_cleaned_state(state)
        return new_state

    def new_robot(self, robot, action):
        """
        Función auxiliar para get_new_state().
        Recibe la posición (robot) del robot y una acción.
        Regresa la nueva posición del robot, new_robot.
        """
        if robot == 'A':
            if action == 'subir':
                new_robot = 'A'
            elif action == 'bajar':
                new_robot = 'F'
            elif action == 'derecha':
                new_robot = 'B'
            elif action == 'izquierda':
                new_robot = 'A'

        if robot == 'B':
            if action == 'subir':
                new_robot = 'B'
            elif action == 'bajar':
                new_robot = 'B'
            elif action == 'derecha':
                new_robot = 'C'
            elif action == 'izquierda':
                new_robot = 'A'

        if robot == 'C':
            if action == 'subir':
                new_robot = 'C'
            elif action == 'bajar':
                new_robot = 'D'
            elif action == 'derecha':
                new_robot = 'C'
            elif action == 'izquierda':
                new_robot = 'B'

        if robot == 'D':
            if action == 'subir':
                new_robot = 'C'
            elif action == 'bajar':
                new_robot = 'D'
            elif action == 'derecha':
                new_robot = 'D'
            elif action == 'izquierda':
                new_robot = 'E'

        if robot == 'E':
            if action == 'subir':
                new_robot = 'E'
            elif action == 'bajar':
                new_robot = 'E'
            elif action == 'derecha':
                new_robot = 'D'
            elif action == 'izquierda':
                new_robot = 'F'

        if robot == 'F':
            if action == 'subir':
                new_robot = 'A'
            elif action == 'bajar':
                new_robot = 'F'
            elif action == 'derecha':
                new_robot = 'E'
            elif action == 'izquierda':
                new_robot = 'F'

        return new_robot

    def new_cleaned_state(self, state):
        """
        Función auxiliar para get_new_state().
        Recibe un estado en el cual la acción es limpiar.
        Regresa el estado con robot_state limpio.
        """
        robot, sA, sB, sC, sD, sE, sF = state
        if robot == 'A':
            new_state = (robot,'limpio',sB, sC, sD, sE, sF)
        elif robot == 'B':
            new_state = (robot, sA, 'limpio', sC, sD, sE, sF)
        elif robot == 'C':
            new_state = (robot, sA, sB, 'limpio', sD, sE, sF)
        elif robot == 'D':
            new_state = (robot, sA, sB, sC, 'limpio', sE, sF)
        elif robot == 'E':
            new_state = (robot, sA, sB, sC, sD, 'limpio', sF)
        elif robot == 'F':
            new_state = (robot, sA, sB, sC, sD, sE, 'limpio')
        return new_state

    def check_cost(self, action):
        """
        Función auxiliar para transition().
        Recibe una acción.
        Regresa el costo generado por la acción.
        """
        if action == 'nada':
            cost = 0
        elif (action == 'bajar'
            or action == 'derecha'
            or action == 'izquierda'
            or action == 'limpiar'):
            cost = 1
        elif action == 'subir':
            cost = 2
        return cost

    def perception(self, state):
        """
        Función de percepción.
        Se percibe el estado (limpio o sucio) en el que se encuentra el robot.
        Recibe un estado.
        Regresa la pareja: (robot, robot_state).
        """
        robot = state[0]
        robot_state = state[' ABCDEF'.find(state[0])]
        return (robot, robot_state)

# Los agentes no toman decisiones en base a información de los estados
# anteriores, sólo toman decisiones en base a la información del estado actual.

# Agente Aleatorio.
# No percibe nada localmente ni el estado de los demás cuartos, sólo 
# realiza una acción al azar.

# Agente Reactivo.
# Percibe información local, pero no percibe el estado de los cuartos vecinos.
# Realiza una acción de acuerdo a la percepción local.

# Agente Reactivo Basado en Modelos.
# Percibe información local.
# Percibe información de los cuartos vecinos inmediatos a los que puede moverse.
# Realiza una acción de acuerdo a ambas percepciones.

class AgenteAleatorio(entornos.Agent):
    """
    Agente aleatorio.
    """
    def __init__(self):
        self.actions = ('subir','bajar','derecha','izquierda','limpiar','nada')

    def programa(self, _):
        """
        Regresa una acción al azar.
        """
        action = choice(self.actions)
        return action

class AgenteReactivoSeisCuartos(entornos.Agent):
    """
    Agente reactivo simple.
    """

    def programa(self, perception):
        """
        Recibe la percepción del agente.
        Regresa una acción de acuerdo a la percepción local del agente.
        No percibe el estado de los demás cuartos.
        """
        robot, robot_status = perception
        if robot_status == 'sucio':
            action = 'limpiar'
        elif robot_status == 'limpio':
            if robot == 'A':
                action = choice(['bajar', 'derecha'])
            elif robot == 'B':
                action = choice(['izquierda', 'derecha'])
            elif robot == 'C':
                action = choice(['bajar', 'izquierda'])
            elif robot == 'D':
                action = choice(['subir', 'izquierda'])
            elif robot == 'E':
                action = choice(['izquierda', 'derecha'])
            elif robot == 'F':
                action = choice(['subir', 'derecha'])
        return action

class AgenteReactivoModeloSeisCuartos(entornos.Agent):
    """
    Agente reactivo basado en modelo.
    """

    def __init__(self):
        self.modelo = ['A','sucio','sucio','sucio','sucio','sucio','sucio']

    def programa(self, perception):
        """
        Recibe la percepción del agente.
        Regresa una acción de acuerdo a la percepción: 
            1. Local del agente.
            2. De los cuartos inmediatos vecinos a los que puede moverse.
        No percibe el estado de los cuartos que no son vecinos inmediatos.
        """
        robot, robot_state = perception
        # Actualiza el modelo interno.
        self.modelo[0] = robot
        self.modelo[' ABCDEF'.find(robot)] = robot_state
        # Decide sobre el modelo interno.
        if (self.modelo[1] == self.modelo[2] == self.modelo[3]
            == self.modelo[4] == self.modelo[5] == self.modelo[6]
            == 'limpio'):
            action = 'nada'
        # Limpia si el estado del robot es sucio.
        elif robot_state == 'sucio':
            action = 'limpiar'
        # Se mueve si el estado del robot es sucio.
        elif robot_state == 'limpio':
            # La elección de la acción movimiento depende de la percepción
            # de los cuartos vecinos inmediatos, con preferencia a los 
            # cuartos que están sucios.

            if robot == 'A':
                if self.modelo[2] == 'sucio':
                    action = 'derecha'
                elif self.modelo[6] == 'sucio':
                    action = 'bajar'
                else:
                    action = choice(['bajar', 'derecha'])

            elif robot == 'B':
                if self.modelo[1] == 'sucio':
                    action = 'izquierda'
                elif self.modelo[3] == 'sucio':
                    action = 'derecha'
                else:
                    action = choice(['izquierda', 'derecha'])

            elif robot == 'C':
                if self.modelo[2] == 'sucio':
                    action = 'izquierda'
                elif self.modelo[4] == 'sucio':
                    action = 'bajar'
                else:
                    action = choice(['bajar', 'izquierda'])

            elif robot == 'D':
                if self.modelo[3] == 'sucio':
                    action = 'subir'
                elif self.modelo[5] == 'sucio':
                    action = 'izquierda'
                else:
                    action = choice(['subir', 'izquierda'])

            elif robot == 'E':
                if self.modelo[4] == 'sucio':
                    action = 'derecha'
                elif self.modelo[6] == 'sucio':
                    action = 'izquierda'
                else:
                    action = choice(['izquierda', 'derecha'])

            elif robot == 'F':
                if self.modelo[1] == 'sucio':
                    action = 'subir'
                elif self.modelo[5] == 'sucio':
                    action = 'derecha'
                else:
                    action = choice(['subir', 'derecha'])

        return action