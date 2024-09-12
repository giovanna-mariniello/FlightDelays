from datetime import datetime

import networkx as nx

from model.model import Model

mymodel = Model()
mymodel.costruisci_grafo(5)
mymodel.print_dettagli_grafo()

a1 = mymodel.get_nodi()[0]

connessa = list(nx.node_connected_component(mymodel._grafo, a1))
a2 = connessa[10]

pathD = mymodel.trova_cammino_dijkstra(a1, a2)
pathBFS = mymodel.trova_cammino_BFS(a1, a2)
pathDFS = mymodel.trova_cammino_DFS(a1, a2)

print("Metodo di Dijkstra")
print(*pathD, sep=" \n")
print("-------------------")
print("Metodo albero Breadth first")
print(*pathBFS, sep= "\n")
print("------------------")
print("Metodo albero Depth first")
print(*pathDFS, sep= "\n")

tic = datetime.now()
bestPath, bestScore = mymodel.get_cammino_ottimo(a1, a2, 4)
print("------------------")
print(f"Cammino ottimo fra {a1} e {a2} ha peso = {bestScore}. \n Trovato in {datetime.now() - tic} secondi")
print(*bestPath, sep = "\n")  # *bestPath fa unpack della lista e ne stampa gli elementi separati da sep