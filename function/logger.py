class ColorText: # https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
    DEBUG = '\033[94m'
    SUCCESS = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def print_debug( title: str, text: str ):
    """Un texte affiché sous une couleur. Le titre sera en bleu et le reste gardera du blanc"""

    print(ColorText.DEBUG + f"[{title}] " + ColorText.ENDC + text)

def print_error( title: str, text: str ):
    """Un texte affiché sous une couleur. Le titre sera en rouge et le reste gardera du blanc"""

    print(ColorText.FAIL + f"[{title}] " + ColorText.ENDC + text)

def print_success( title: str, text: str ):
    """Un texte affiché sous une couleur. Le titre sera en vert et le reste gardera du blanc"""

    print(ColorText.SUCCESS + f"[{title}] " + ColorText.ENDC + text)