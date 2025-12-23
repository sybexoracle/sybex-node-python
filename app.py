import time
from src.app import App

if __name__ == "__main__":
    app = App()
    app.initialize()

    try:
        app.polling_service()

        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        app.stop_service()
