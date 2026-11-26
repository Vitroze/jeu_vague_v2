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

    def DisplayVue(self, vue: callable):
        """
        Affiche la vue passée en paramètre.
        """
        self.console.clear()
        vue()

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
affichage = Affichage()
affichage.DisplayVue(lambda: affichage.console.print(affichage.create_info_box("Titre", "Ceci est une info box")))
affichage.DisplayVue(lambda: affichage.console.print(affichage.create_select_box("Titre", ["Option 1", "Option 2", "Option 3"], index=1)))
affichage.ShowError("Ceci est un message d'erreur.")