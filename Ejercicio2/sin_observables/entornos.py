
class Entorno:
    """
    Clase de entornos.
    """

    def transition(self, s, a):
        """
        @param s: Tupla con un estado legal del entorno.
        @param a: Acción en el entorno.
        @return: (new_state, cost)
        Nuevo estado y el costo de ir de s a new_state con la acción a.
        """
        pass

    def perception(self, s):
        """
        @param s: Tupla con un estado legal del entorno.
        @return: Tupla con valores que se perciben del entorno.
        """
        return s

class Agent(object):
    """
    Clase de un agente en un entorno discreto determinista observable.
    """

    def programa(self, p):
        """
        @param p: Lista con los valores que se perciben de un entorno.
        @return: Acción seleccionada por el agente.
        """
        pass