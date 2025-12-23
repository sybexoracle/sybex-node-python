import logging
from rich.logging import RichHandler
from rich.console import Console

console = Console()
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        RichHandler(
            console=console,
            rich_tracebacks=True,
            show_time=True,
            show_level=True,
            show_path=True,
        )
    ],
)

AppLogger = logging.getLogger("SybexNodeLogger")