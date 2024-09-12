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
        pass

    def handle_itinerario(self, e):
        pass