import logging
import os


def setup_logging():
    log_level = os.getenv("LOG_LEVEL", "CRITICAL").upper()
    logging.basicConfig(
        level=getattr(logging, log_level, logging.WARNING),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        # For now only to the console
        handlers=[logging.StreamHandler()],
    )


# Call the setup_logging function to configure logging
setup_logging()
