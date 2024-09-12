from datetime import datetime

import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view:View, model:Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self.aer_part = None
        self.aer_arr = None

    def handle_analizza_aer(self, e):
        self._view.txt_result.controls.clear()

        x = self._view.txt_num_comp.value
        try:
            int(x)
        except ValueError:
            self._view.create_alert("Per favore inserisci un valore intero.")
            self._view.update_page()
            return

        self._model.costruisci_grafo(int(x))

        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txt_result.controls.append(ft.Text(f"Numero nodi: {self._model.get_num_nodi()}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero archi: {self._model.get_num_archi()}"))

        self._view.dd_aeroporto_part.disabled = False
        self._view.dd_aeroporto_arr.disabled = False
        self._view.btn_aeroporti_connessi.disabled = False
        self._view.txt_num_tratte_max.disabled = False
        self._view.btn_connessione.disabled = False
        self._view.btn_cerca_itinerario.disabled = False

        self.riempi_dd()

        self._view.update_page()

    def riempi_dd(self):
        nodi = self._model.get_nodi()
        for n in nodi:
            self._view.dd_aeroporto_part.options.append(ft.dropdown.Option(text=n.AIRPORT, data=n, on_click=self.leggi_dd_part))
            self._view.dd_aeroporto_arr.options.append(ft.dropdown.Option(text=n.AIRPORT, data=n, on_click=self.leggi_dd_arr))

    def leggi_dd_part(self, e):
        if e.control.data is None:
            self.aer_part = None
        else:
            self.aer_part = e.control.data

    def leggi_dd_arr(self, e):
        if e.control.data is None:
            self.aer_arr = None
        else:
            self.aer_arr = e.control.data

    def handle_aer_connessi(self, e):

        self._view.txt_result.controls.clear()

        a0 = self.aer_part
        if a0 is None:
            self._view.create_alert("Per favore seleziona un aeroporto di partenza.")
            return

        vicini = self._model.get_sorted_vicini(a0)
        self._view.txt_result.controls.append(ft.Text(f"Ecco i vicini di {a0}:"))
        for v in vicini:
            self._view.txt_result.controls.append(ft.Text(f"{v[1]} - {v[0]}"))

        self._view.update_page()



    def handle_connessione(self, e):
        self._view.txt_result.controls.clear()
        a1 = self.aer_part
        a2 = self.aer_arr

        # verificare che ci sia un percorso
        if (not self._model.esiste_percorso(a1, a2)):
            self._view.txt_result.controls.append(ft.Text(f"Non esiste un percorso tra {a1} e {a2}."))
            return
        else:
            self._view.txt_result.controls.append(ft.Text(f"Esiste un percorso tra {a1} e {a2}"))

        # trovare un possibile percorso
        path = self._model.trova_cammino_BFS(a1, a2)
        self._view.txt_result.controls.append(ft.Text(f"Il cammino (con minor numero di archi) tra {a1} e {a2} è:"))
        for p in path:
            self._view.txt_result.controls.append(ft.Text(f"{p}"))

        self._view.txt_num_tratte_max.disabled = False
        self._view.btn_cerca_itinerario.disabled = False
        self._view.update_page()

    def handle_itinerario(self, e):
        a1 = self.aer_part
        a2 = self.aer_arr
        t = self._view.txt_num_tratte_max.value

        try:
            t_int = int(t)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Per favore inserire un valore intero."))

        tic = datetime.now()
        path, score = self._model.get_cammino_ottimo(a1, a2, t_int)

        self._view.txt_result.controls.clear()

        self._view.txt_result.controls.append(ft.Text(f"Il percorso ottimo tra {a1} e {a2} è:"))
        for p in path:
            self._view.txt_result.controls.append(ft.Text(f"{p}"))

        self._view.txt_result.controls.append(ft.Text(f"Numero totale di voli: {score}"))
        self._view.txt_result.controls.append(ft.Text(f"La ricerca ha impegato un tempo pari a {datetime.now()-tic}"))

        self._view.update_page()
