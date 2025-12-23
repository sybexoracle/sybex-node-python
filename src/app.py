import time
from threading import Thread
from threading import Event as ThreadEvent
from src.logger import AppLogger, console
from src.resolver import Resolver
from src.helpers import minimize_string, timestamp_to_datetime
from src.relayer.client import RelayerClient
from src.relayer.amm import RelayerAMM


class App:
    def __init__(self) -> None:
        self.event = ThreadEvent()

        self.delay = 5  # seconds

        self.threads = []

        self.relayer = RelayerClient()
        self.resolver = Resolver()
        self.relayer_amm = RelayerAMM(self.relayer)

    def initialize(self):
        AppLogger.info("Initializing Sybex Oracle Node...")
        self.relayer.initialize()

    def start(self):
        questions = self.resolver.query_questions()

        if len(questions) == 0:
            AppLogger.info("No new questions to resolve. Waiting for the next poll...")
            time.sleep(5)
            return

        for question in questions:
            question_id = question.get("id")
            question_real_id = question.get("questionId")

            AppLogger.info(
                f"Checking answers for question ID: {minimize_string(question_real_id)}"
            )
            answers = self.resolver.query_answers(questionId=question_real_id)
            if len(answers) > 0:
                AppLogger.info(
                    f"Question ID: {minimize_string(question_id)} already has answers. Skipping..."
                )
                continue

            # Check deadline
            timeout = question.get("timeout")
            current_time = int(time.time())
            deadline = current_time + int(timeout)

            current_datetime = timestamp_to_datetime(current_time)
            deadline_datetime = timestamp_to_datetime(deadline)

            AppLogger.info(
                f"Current time: {current_datetime}, Deadline: {deadline_datetime}"
            )

            if deadline and current_time < int(deadline):
                AppLogger.info(
                    f"Question ID: {minimize_string(question_id)} deadline not reached. Skipping..."
                )
                continue

            AppLogger.info(f"Resolving question ID: {minimize_string(question_id)}...")
            self.resolver.try_resolve(question=question)

    def start_service(self):
        while not self.event.is_set():
            try:
                AppLogger.info("Polling for new questions to resolve...")
                self.start()
            except KeyboardInterrupt:
                AppLogger.info("Shutting down polling service...")
                self.stop_service()
            except Exception as e:
                console.print_exception()
                AppLogger.error(f"Error in polling service: {e}")
            time.sleep(self.delay)

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
