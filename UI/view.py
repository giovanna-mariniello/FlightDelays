import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Flight Delay"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.DARK
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.txt_aeroporto = None
        self.btn_analizza_aeroporti = None
        self.dd_aeroporto_part = None
        self.dd_aeroporto_arr = None
        self.btn_aeroporti_connessi = None
        self.txt_num_tratte_max = None
        self.btn_connessione = None
        self.btn_cerca_itinerario = None
        self.txt_result = None
        self.txt_container = None

    def load_interface(self):
        self._title = ft.Text("Flight Delay", text_align=ft.TextAlign.CENTER)

        self.txt_num_comp = ft.TextField(label="Compagnie aeree minime", width=200, text_align=ft.TextAlign.CENTER)
        self.btn_analizza_aeroporti = ft.ElevatedButton("Analizza aeroporti", width=200,
                                                        on_click=self._controller.handle_analizza_aer)

        self.dd_aeroporto_part = ft.Dropdown(hint_text="Aeroporto di partenza", width=500, disabled=True)
        self.dd_aeroporto_arr = ft.Dropdown(hint_text="Aeroporto di arrivo", width=500, disabled=True)
        self.btn_aeroporti_connessi = ft.ElevatedButton("Aeroporti connessi", width=200, on_click=self._controller.handle_aer_connessi, disabled=True)

        self.txt_num_tratte_max = ft.TextField(label="Numero tratte massimo", width=230, disabled=True)
        self.btn_connessione = ft.ElevatedButton("Test connessione", on_click=self._controller.handle_connessione, disabled=True)
        self.btn_cerca_itinerario = ft.ElevatedButton("Cerca itinerario", on_click=self._controller.handle_itinerario, disabled=True)


        row1 = ft.Row([ft.Container(self.txt_num_comp, width=500), ft.Container(self.btn_analizza_aeroporti, width=500)], alignment=ft.MainAxisAlignment.CENTER)
        row2 = ft.Row([ft.Container(self.dd_aeroporto_part, width=500), ft.Container(self.btn_aeroporti_connessi, width=500)], alignment=ft.MainAxisAlignment.CENTER)
        row3 = ft.Row([ft.Container(self.dd_aeroporto_arr, width=500), ft.Container(self.btn_connessione, width=500)], alignment=ft.MainAxisAlignment.CENTER)
        row4 = ft.Row([ft.Container(self.txt_num_tratte_max, width=500), ft.Container(self.btn_cerca_itinerario, width=500)], alignment=ft.MainAxisAlignment.CENTER)

        self._page.controls.append(row1)
        self._page.controls.append(row2)
        self._page.controls.append(row3)
        self._page.controls.append(row4)

        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
