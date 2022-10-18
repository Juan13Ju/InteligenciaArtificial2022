
class Entorno:
    """
    Clase de entornos.
    """

    def __init__(self, x0=[]):
        """
        Inicializa la clase con el estado inicial como una lista.
        """
        self.state = x0[:]
        self.performance = 0

    def legal_action(self, action):
        """
        @param action: Una acción en el entorno
        @return: True si la acción es legal.
        """
        return True

    def transition(self, action):
        """
        @param action: Acción legal en el estado.
        Modifica self.state y self.performance.
        """
        pass

    def perception(self):
        """
        @return: Tupla con los valores que se perciben del entorno 
        por default el estado completo.
        """
        return self.state

class Agent(object):
    """
    Clase de un agente en un entorno discreto determinista observable.
    """

    def programa(self, perception):
        """
        @param perception: Lista con los valores que se perciben de un entorno.
        @return: action: Acción seleccionada por el agente.
        """
        pass