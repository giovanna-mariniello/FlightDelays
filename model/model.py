import copy

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._all_aeroporti = DAO.get_all_aeroporti()
        self.id_map_aer = {}

        for a in self._all_aeroporti:
            self.id_map_aer[a.ID] = a

        self._grafo = nx.Graph()

        self._bestPath = []
        self._bestObjFun = 0

    def costruisci_grafo(self, n_min):
        self._nodi = DAO.get_aereoporti_filtrati(n_min, self.id_map_aer)
        self._grafo.add_nodes_from(self._nodi)
        self.add_archi_v1()

    def add_archi_v1(self):
        all_connessioni = DAO.get_all_connessioni_v1(self.id_map_aer)

        for c in all_connessioni:
            a1 = c.a1
            a2 = c.a2
            peso = c.n
            if a1 in self._grafo and a2 in self._grafo:  # controllo che i nodi facciano parte del grafo (visto che i nodi non sono tutti gli aeroporti, ma sono filtrati)
                if self._grafo.has_edge(a1, a2): # visto che il grafo non è orientato, controllo se l'arco esiste già
                    self._grafo[a1][a2]["weight"] += peso  # se esiste già aumento il peso
                else:
                    self._grafo.add_edge(a1, a2, weight=peso)  # se non esiste lo aggiungo


    def add_archi_v2(self):
        all_connessioni = DAO.get_all_connessioni_v2()

        for c in all_connessioni:
            if c.a1 in self._grafo and c.a2 in self._grafo:
                self._grafo.add_edge(c.a1, c.a2, weight=c.n)

    def get_num_nodi(self):
        return len(self._grafo.nodes)

    def get_num_archi(self):
        return len(self._grafo.edges)

    def get_nodi(self):
        return self._nodi

    def print_dettagli_grafo(self):
        print(f"Numero nodi: {len(list(self._grafo.nodes))}")
        print(f"Numero archi: {len(list(self._grafo.edges))}")

    def get_sorted_vicini(self, a0):
        vicini = self._grafo.neighbors(a0)

        vicini_tuple = []
        for v in vicini:
            vicini_tuple.append((v, self._grafo[a0][v]["weight"]))
        vicini_tuple.sort(key=lambda x:x[1], reverse=True)

        return vicini_tuple

    def esiste_percorso(self, a1, a2):
        connessa = nx.node_connected_component(self._grafo, a1)
        if a2 in connessa:  # verifico che a2 sia presente nella componente connessa che contiene a1
            return True

        return False

    def trova_cammino_dijkstra(self, a1, a2):
        # ci è richiesto un cammino qualsiasi (non necessariamente quello ottimo)
        return nx.dijkstra_path(self._grafo, a1, a2) # restituisce una lista di nodi 8(cammino ottimo che minimizza il peso degli archi)
        # si assume che esista un cammino tra a1 e a2
    def trova_cammino_BFS(self, a1, a2):  # garantisce il cammino con il minor numero di archi
        # costruisco l'albero di visita (DFS o BFS)
        tree = nx.bfs_tree(self._grafo, a1)
        if a2 in tree:
            print(f"{a2} è contenuto nell'albero di visita BFS")

        path = [a2] # parto dalla fine
        while path[-1] != a1:  # finché l'ultimo elemento non è a1
            path.append(list(tree.predecessors(path[-1]))[0])  # inserisco nel cammino il primo predecessore dell'ultimo elemento contenuto in path

        path.reverse()  # giro il cammino per fare in modo di partire da a1 e arrivare ad a2 (nell'albero partiamo dalla foglia e arriviamo alla radice)
        return path

    def trova_cammino_DFS(self, a1, a2): # va in profondità, quindi restituisce il cammino più lungo
        tree = nx.dfs_tree(self._grafo, a1)
        if a2 in tree:
            print(f"{a2} è contenuto nell'albero di visita DFS")

        path = [a2]  # parto dalla fine
        while path[-1] != a1:  # finché l'ultimo elemento non è a1
            path.append(list(tree.predecessors(path[-1]))[0])  # inserisco nel cammino il primo predecessore dell'ultimo elemento contenuto in path

        path.reverse()
        return path

    def get_cammino_ottimo(self, a1, a2, t):
        self._bestPath = []
        self._bestObjFun = 0

        parziale = [a1]   # cerco un cammino tra a1 e a2, quindi a1 fa sicuramente parte del parziale
        self.ricorsione(parziale, a2, t)

        return self._bestPath, self._bestObjFun


    def ricorsione(self, parziale, target, t):
        # verificare che parziale sia una possibile soluzione
            # verificare che parziale è meglio di best
            # esco

        if len(parziale) == t+1:   # perché parziale appende i nodi (t archi -> t+1 nodi)
            return

        if self.getObjFun(parziale) > self._bestObjFun and parziale[-1] == target:  # controllo anche che l'ultimo nodo di parziale sia effettivamente il mio nodo target
            self._bestObjFun = self.getObjFun(parziale)
            self._bestPath = copy.deepcopy(parziale)


        for n in self._grafo.neighbors(parziale[-1]):  # ciclo tra i vicini dell'ultimo nodo che ho aggiunto in parziale
            if n not in parziale: # controllo che il nodo non sia già nella soluzione (in questo caso non era richiesto)
                parziale.append(n)
                self.ricorsione(parziale, target, t)
                parziale.pop()


        # se non sono ancora uscito, posso ancora aggiungere nodi
            # prendo i vicini e provo ad aggiungerli
            # ricorsione

        pass

    def getObjFun(self, listaNodi):
        objVal = 0
        for i in range(0, len(listaNodi)-1):  # metto -1 perché altrimenti alla fine prendo un arco che non esiste
            objVal += self._grafo[listaNodi[i]][listaNodi[i+1]]["weight"]  # quando i=0 prendo l'arco tra 0 e 1, quando i=1 prendo l'arco tra 1 e 2, ecc..

        return objVal













