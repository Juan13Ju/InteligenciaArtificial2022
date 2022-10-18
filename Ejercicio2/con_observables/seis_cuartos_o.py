import entornos_o
from random import choice

class SeisCuartos(entornos_o.Entorno):
    """
    Clase para un entorno de dos cuartos. Muy sencilla solo regrupa métodos.
    El estado se define como (robot, A, B)
    donde robot puede tener los valores "A", "B"
    A y B pueden tener los valores "limpio", "sucio"
    Las acciones válidas en el entorno son ("ir_A", "ir_B", "limpiar", "nada").
    Todas las acciones son válidas en todos los estados.
    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza
    """

    # Aquí se modifica el estado inicial, si se cambia A por cualquier otra
    # letra, el comportamiento cambia. Por ejemplo, si comienza en C. 
    def __init__(self,x0=['A','sucio','sucio','sucio','sucio','sucio','sucio']):
        """
        Por default inicialmente el robot está en A y los dos cuartos
        están sucios
        """
        # Estado inicial.
        self.state = x0[:] 
        # Desempeño.
        self.performance = 0

    def legal_action(self, action):
        """
        Revisa acciones legales.
        """
        actions = ['subir','bajar','derecha','izquierda','limpiar','nada']
        if action in actions:
            return True
        else:
            return False

    def transition(self, action):
        """
        Función de transición de un estado a otro.
        Recibe una acción.
        Modifica self.state y self.performance.
        """

        if not self.legal_action(action):
            raise ValueError('La action no es legal para este estado')

        # Variables necesarias para medir el desempeño.
        old_robot = self.state[0]
        old_robot_state = self.state[' ABCDEF'.find(self.state[0])]

        # Actualización de información.
        robot = self.state[0]
        if action == 'limpiar':
            self.state[' ABCDEF'.find(self.state[0])] = 'limpio'

        if robot == 'A':
            if action == 'subir':
                self.state[0] = 'A'
            elif action == 'bajar':
                self.state[0] = 'F'
            elif action == 'derecha':
                self.state[0] = 'B'
            elif action == 'izquierda':
                self.state[0] = 'A'

        if robot == 'B':
            if action == 'subir':
                self.state[0] = 'B'
            elif action == 'bajar':
                self.state[0] = 'B'
            elif action == 'derecha':
                self.state[0] = 'C'
            elif action == 'izquierda':
                self.state[0] = 'A'

        if robot == 'C':
            if action == 'subir':
                self.state[0] = 'C'
            elif action == 'bajar':
                self.state[0] = 'D'
            elif action == 'derecha':
                self.state[0] = 'C'
            elif action == 'izquierda':
                self.state[0] = 'B'

        if robot == 'D':
            if action == 'subir':
                self.state[0] = 'C'
            elif action == 'bajar':
                self.state[0] = 'D'
            elif action == 'derecha':
                self.state[0] = 'D'
            elif action == 'izquierda':
                self.state[0] = 'E'

        if robot == 'E':
            if action == 'subir':
                self.state[0] = 'E'
            elif action == 'bajar':
                self.state[0] = 'E'
            elif action == 'derecha':
                self.state[0] = 'D'
            elif action == 'izquierda':
                self.state[0] = 'F'

        if robot == 'F':
            if action == 'subir':
                self.state[0] = 'A'
            elif action == 'bajar':
                self.state[0] = 'F'
            elif action == 'derecha':
                self.state[0] = 'E'
            elif action == 'izquierda':
                self.state[0] = 'F'

        # Se mide el desempeño después de que se han realizado las acciones.
        # Los valores que toma son: 1, 0, -1.
        #  1: El comportamiento es el esperado.
        #  0: No hace nada en donde no hay que limpiar.
        # -1: El comportamiento no es el esperado.

        # Variables necesarias para obtener el desempeño.
        new_robot = self.state[0]
        new_robot_state = self.state[' ABCDEF'.find(self.state[0])]
        moves = ['subir', 'bajar', 'derecha', 'izquierda']

        # Neutro si no hace nada en un cuarto limpio.
        if action == 'nada' and old_robot_state == 'limpio':
            self.performance = 0

        # Positivo si se mueve a un cuarto sucio.
        elif (
            action in moves
            and new_robot_state == 'sucio'
            and new_robot != old_robot
            ):
            self.performance = 1
        # Positivo si limpia un cuarto que está sucio.
        elif action == 'limpiar' and old_robot_state == 'sucio':
            self.performance = 1

        # Negativo si no hace nada en un cuarto sucio.
        elif action == 'nada' and old_robot_state == 'sucio':
            self.performance = -1
        # Negativo si se mueve sin limpiar el cuarto.
        elif action in moves and old_robot_state == 'sucio':
            self.performance = -1
        # Negativo si se mueve a un cuarto limpio.
        elif action in moves and new_robot_state == 'limpio':
            self.performance = -1
        # Negativo si se mueve al mismo cuarto.
        elif action in moves and old_robot == new_robot:
            self.performance = -1
        # Negativo si limpia un cuarto que está limpio.
        elif action == 'limpiar' and old_robot_state == 'limpio':
            self.performance = -1


    def perception(self):
        """
        Función de percepción.
        Se percibe el estado (limpio o sucio) en el que se encuentra el robot.
        Regresa la pareja: [robot, robot_state].
        """
        robot = self.state[0]
        robot_state = self.state[' ABCDEF'.find(self.state[0])]
        return [robot, robot_state] 

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

class AgenteAleatorio(entornos_o.Agent):
    """
    Agente aleatorio.
    """
    def __init__(self):
        self.actions = ['subir','bajar','derecha','izquierda','limpiar','nada']

    def programa(self, perception):
        """
        Regresa una acción al azar.
        """
        action = choice(self.actions)
        return action

class AgenteReactivoSeisCuartos(entornos_o.Agent):
    """
    Agente reactivo simple.
    """

    def programa(self, perception):
        """
        Recibe la percepción del agente.
        Regresa una acción de acuerdo a la percepción local del agente.
        No percibe el estado de los demás cuartos.
        """
        robot, robot_state = perception
        if robot_state == 'sucio':
            action = 'limpiar'
        elif robot_state == 'limpio':
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

class AgenteReactivoModeloSeisCuartos(entornos_o.Agent):
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
        # Se mueve si el estado del robot es limpio.
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