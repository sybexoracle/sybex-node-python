import logging
from rich.logging import RichHandler
from rich.console import Console

console = Console()

# disbale all other loggers

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

blocked_loggers = [
    "graphql",
    "urllib3",
    "asyncio",
    "gql.transport.aiohttp",
    "gql.transport.websockets",
    "gql.transport.requests",
    "web3.providers.HTTPProvider"
]
for logger_name in blocked_loggers:
    logging.getLogger(logger_name).setLevel(logging.WARNING)

for name in logging.root.manager.loggerDict:
    logging.getLogger(name).setLevel(logging.CRITICAL + 1)

AppLogger = logging.getLogger("SybexNodeLogger")
AppLogger.setLevel(logging.DEBUG)
AppLogger.propagate = True