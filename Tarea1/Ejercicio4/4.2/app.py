import sys
import math

from AStarAlgorithm import AStarAlgorithm
from Nodo import Nodo
import csv
from unidecode import unidecode


class App(object):
    def __init__(self):
        print("Creando grafica del metro: ", end="")
        # Primero creamos un diccionario en el cual guardamos {nombre: [lat, lon]}
        self.coordenadas = {}
        with open("LineasMetro.csv", mode="r") as file:
            csv_reader = csv.DictReader(file)

            for row in csv_reader:
                self.coordenadas[unidecode(row["nombre"].lower())] = (float(row["lat"]), float(row["lon"]))
        target = "lazaro cardenas"
        targetLat = self.coordenadas[target][0]
        targetLon = self.coordenadas[target][1]
        # Representamos los vertices con un diccionario {nombre : nodo}
        self.vertices = {}
        for estacion in self.coordenadas:
            dLat = self.coordenadas[estacion][0] - targetLat
            dLon = self.coordenadas[estacion][1] - targetLon
            h = math.sqrt((dLat ** 2) + (dLon ** 2))
            self.vertices[estacion] = Nodo(estacion, h)
        # Ahora podemos añadir sus adyacencias
        with open("metro.csv", mode="r") as file:
            csv_reader = csv.DictReader(file)

            for row in csv_reader:
                origen = unidecode(row["origen"].lower())
                destino = unidecode(row["destino"].lower())
                longitud = int(row["longitud"])
                nodoActual = self.vertices[origen]
                nodoDestino = self.vertices[destino]
                # Añadimos las adyacencias en ambos vertices
                nodoActual.addChild(nodoDestino, longitud)
                nodoDestino.addChild(nodoActual, longitud)
        print("Terminando de contruir grafica")

    def AStarSearchAlgorithm(self):
        print("\n Buscando la mejor rura con A*")
        astar = AStarAlgorithm(self.vertices["coyoacan"], self.vertices["lazaro cardenas"])
        print("Nodo Inicial: %s -----> Nodo Final %s" % (
        self.vertices["coyoacan"].name, self.vertices["lazaro cardenas"].name))
        astar.run()


app = App()
app.AStarSearchAlgorithm()
