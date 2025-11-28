import logging

logger = logging.getLogger("giants_to_i3dio")
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Usage:  logger.info("This is an info message")
