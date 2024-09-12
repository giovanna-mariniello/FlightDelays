from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._all_aeroporti = DAO.get_all_aeroporti()
        self.id_map_aer = {}

        for a in self._all_aeroporti:
            self.id_map_aer[a.ID] = a

        self._grafo = nx.Graph()

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



