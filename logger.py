import logging
import os
from datetime import datetime


# Create logs folder
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)


# Create today's log file
log_file = os.path.join(
    LOG_DIR,
    f"app_{datetime.now().strftime('%Y-%m-%d')}.log"
)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()
    ]
)


logger = logging.getLogger("Document-QA-Bot")


def log_question(question):
    """Log the question asked by the user."""
    logger.info("Question received: %s", question)


def log_success(question, sources):
    """Log successful answer generation."""
    logger.info(
        "Answer generated successfully | Question: %s | Sources: %s",
        question,
        sources
    )


def log_error(error):
    """Log an application error."""
    logger.error("Application error: %s", error)