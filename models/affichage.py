"""
UML :
    LIB : Rich

    class Affichage {
        +DisplayVue(vue: Function)
        +ShowError(error: String)
        +create_info_box(titre: String, info: String, box_color: String, text_color: String) Panel
        +create_select_box(titre: String, items: List~Item~, index: int, box_color: String, text_color: String, hover_color: String) Panel
    }
"""

from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.align import Align
from rich.table import Table
from rich.live import Live

class Affichage:
    _instance = None  # Variable de classe pour stocker l'instance unique

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Affichage, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):  # Vérifie si l'instance a déjà été initialisée
            self.initialized = True
            self.console = Console()
            self.live = None  # Pour gérer l'affichage en direct si nécessaire

    def DisplayVue(self, vue: callable):
        """
        Affiche la vue passée en paramètre.
        """
        self.stop_live()
        self.console.clear()
        vue()

    def update_live(self, vue: callable):
        if self.live is None:
            self.live = Live(vue, console=self.console, refresh_per_second=4)
            self.live.start()
        else:
            self.live.update(vue)

    def stop_live(self):
        if self.live is not None:
            self.live.stop()
            self.live = None

    def ShowError(self, error: str):
        self.console.print(f"[bold red]Erreur : {error}[/bold red]")

    def create_info_box(self, titre: str, info: str, box_color="blue", text_color="white"):
        panel = Panel(
            Align.center(info, vertical="middle"),
            title=titre,
            border_style=box_color,
            style=text_color,
            padding=(1, 2),
        )
        return panel

    def create_multiples_info_boxes(self, titre: str, infos: list, box_color="blue", text_color="white"):
        grid = Table.grid(expand=True, padding=(0, 1))
        info_panels = []

        for info in infos:
            grid.add_column(ratio=1)  # même largeur pour chaque colonne
            info_panels.append(Panel(
                Align.center(info["content"], vertical="middle"),
                title=info.get("title"),
                style=text_color,
                padding=(0, 2),
            ))

        grid.add_row(*info_panels)  # tous les panneaux sur la même ligne

        return Panel(
            grid,
            title=titre,
            border_style=box_color,
            padding=(1, 2),
        )

    def create_select_box(self, titre: str, items: list, index=0, box_color="blue", text_color="white", hover_color="green"):
        item_panels = []
        for i, item in enumerate(items):
            if i == index:
                item_panel = Panel(
                    Align.center(item, vertical="middle"),
                    style=f"bold {hover_color}",
                    padding=(0, 2),
                )
            else:
                item_panel = Panel(
                    Align.center(item, vertical="middle"),
                    style=text_color,
                    padding=(0, 2),
                )
            item_panels.append(item_panel)

        columns = Columns(item_panels, expand=True)
        panel = Panel(
            columns,
            title=titre,
            border_style=box_color,
            padding=(1, 2),
        )
        return panel

    @classmethod
    def get_affichage(cls):
        return cls._instance


# Example
# affichage = Affichage()
# affichage.DisplayVue(lambda: affichage.console.print(affichage.create_info_box("Titre", "Ceci est une info box")))
# affichage.DisplayVue(lambda: affichage.console.print(affichage.create_select_box("Titre", ["Option 1", "Option 2", "Option 3"], index=1)))
# affichage.ShowError("Ceci est un message d'erreur.")
# affichage.DisplayVue(lambda:
#                      affichage.console.print(affichage.create_multiples_info_boxes(
#                         "Titre", [
#                              {
#                                  "title": "Info 1",
#                                  "content": "Contenu 1"
#                              }, {
#                                  "title": "Info 2",
#                                  "content": "Contenu 2"
#                              }
#                          ], box_color="magenta", text_color="yellow")));