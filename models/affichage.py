from typing import Callable, List
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.console import Console
import readchar


SPECIAL_KEYS = {
    readchar.key.UP: "UP",
    readchar.key.DOWN: "DOWN",
    readchar.key.LEFT: "LEFT",
    readchar.key.RIGHT: "RIGHT",
    readchar.key.ENTER: "ENTER",
    readchar.key.BACKSPACE: "BACKSPACE",
    readchar.key.TAB: "TAB",
    readchar.key.ESC: "ESC",
    readchar.key.SPACE: "SPACE",
    readchar.key.DELETE: "DELETE",
}


def format_key(k: str) -> str:
    if k in SPECIAL_KEYS:
        return SPECIAL_KEYS[k]
    if k.isprintable():
        return k
    # Fallback for unmapped control keys (e.g., Ctrl+C -> '\x03')
    return repr(k)


CANCEL_KEYS = (readchar.key.CTRL_C, readchar.key.ESC,
               "\x1b", "\x1b\x1b", "\x03", "\x1b\x03")


class Affichage:

	console = Console()

	@classmethod
	def display_vue(cls, vue: Callable, max_index=1):
		if max_index <= 0:
			max_index = 1
		index_actuel = 0
		with Live(vue(index_actuel), console=cls.console, refresh_per_second=20, transient=True) as live:
			while True:
				touche = readchar.readkey()
				if touche == readchar.key.UP:
					index_actuel = (index_actuel - 1) % max_index
					live.update(vue(index_actuel))
				elif touche == readchar.key.DOWN:
					index_actuel = (index_actuel + 1) % max_index
					live.update(vue(index_actuel))
				elif touche == readchar.key.ENTER:
					return index_actuel
				elif touche in CANCEL_KEYS:
					return None

	@classmethod
	def demander_input(cls, prompt: str) -> str:
		return cls.console.input(prompt)

	BOX_HEIGHT = 20

	@classmethod
	def show_error(cls, error: str):
		texte = Text(error, style="bold red")
		return Panel(
			texte,
			title="[bold]Erreur[/bold]",
			border_style="red",
			height=cls.BOX_HEIGHT,
			expand=True,
			padding=(1, 2),
		)

	@classmethod
	def create_info_box(cls, titre: str, info: str, box_color: str, text_color: str) -> Panel:
		texte = Text(info, justify="center", style=text_color)
		return Panel(
			texte,
			title=f"[bold {box_color}]✦ {titre} ✦[/]",
			title_align="center",
			border_style=box_color,
			height=cls.BOX_HEIGHT,
			expand=True,
			padding=(1, 2),
		)

	@classmethod
	def create_select_box(cls, titre: str, items: List, index: int, box_color: str, text_color: str, hover_color: str) -> Panel:
		texte = Text(justify="center")
		dernier = len(items) - 1
		for i, item in enumerate(items):
			fin = "\n" if i < dernier else ""
			if i == index:
				texte.append(f" ❯ {item} ❮ ", style=f"bold {hover_color} reverse")
			else:
				texte.append(f"   {item}   ", style=text_color)
			texte.append(fin)

		return Panel(
			texte,
			title=f"[bold {box_color}]✦ {titre} ✦[/]",
			title_align="center",
			subtitle="[dim]↑/↓ naviguer • ⏎ valider[/dim]",
			subtitle_align="center",
			border_style=box_color,
			height=cls.BOX_HEIGHT,
			expand=True,
			padding=(1, 2),
		)