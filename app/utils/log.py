import logging

# Create a custom logger
logger = logging.getLogger("InsightEngineLogger")
logger.setLevel(logging.INFO)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create log format
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
console_handler.setFormatter(formatter)

# Attach handler if not already attached
if not logger.handlers:
    logger.addHandler(console_handler)
