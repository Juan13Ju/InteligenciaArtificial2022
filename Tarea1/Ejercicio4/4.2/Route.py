import sys

class Route(object):
        def __init__(self, name, value, realCost, iteration, node):
                self.name = name
                self.value = value
                self.realCost = realCost
                self.iteration = iteration
                self.node = node