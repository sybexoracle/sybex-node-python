import time
from src.app import App
from src.logger import AppLogger

if __name__ == "__main__":
    app = App()

    try:
        app.initialize()
        app.polling_service()

        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        app.stop_service()
    except Exception as e:
        AppLogger.error(f"An error occurred: {str(e)}")
        app.stop_service()
