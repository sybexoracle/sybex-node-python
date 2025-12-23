import time
from threading import Thread
from threading import Event as ThreadEvent
from src.logger import AppLogger, console


class App:
    def __init__(self) -> None:
        self.event = ThreadEvent()

        self.threads = []

    def initialize(self):
        AppLogger.info("Initializing Sybex Oracle Node...")

    def start_service(self):
        while not self.event.is_set():
            try:
                AppLogger.info("Polling for new questions to resolve...")

                time.sleep(10)

                AppLogger.info("No new questions found. Continuing to poll...")
            except KeyboardInterrupt:
                AppLogger.info("Shutting down polling service...")
                self.stop_service()
            except Exception as e:
                AppLogger.error(f"Error in polling service: {e}")

    def spinner_service(self):
        with console.status("Oracle Node is running...", spinner="dots"):
            self.event.wait()

    def polling_service(self):
        AppLogger.info("Starting polling service...")

        polling_thread = Thread(target=self.start_service)
        polling_thread.start()

        spinner_thread = Thread(target=self.spinner_service)
        spinner_thread.start()

        self.threads.extend([polling_thread, spinner_thread])

    def stop_service(self):
        AppLogger.info("Stopping Sybex Oracle Node...")

        self.event.set()
        for thread in self.threads:
            thread.join()
