class Nodo:
    def __init__(self, name, estCostToTarget):
        self.childNodes = []
        self.explorados = 0
        self.childNodesCost = {}
        self.parentNodes = []
        self.name = name
        self.estCostToTarget = estCostToTarget

    def addChild(self, childNode, realCost):
        self.childNodes.append(childNode)
        self.childNodesCost[childNode.name] = realCost

    def getChildrenNodes(self):
            return self.childNodes

    def getChildrenRealCost(self) -> float:
        return self.childNodesCost

    def addParent(self, nodeName):
        self.parentNodes.append(nodeName)

    def getParentNodes(self):
        return self.parentNodes
    def assignEstimatedCost(self, value):
        self.estCostToTarget = value

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name