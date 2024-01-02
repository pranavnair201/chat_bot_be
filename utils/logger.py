import logging
import os


def get_logger(session_id):
    log_folder = "./session_logs"
    os.makedirs(log_folder, exist_ok=True)

    log_file_path = os.path.join(log_folder, f"{session_id}.log")

    logger = logging.getLogger(session_id)

    if not logger.handlers:  # Check if the logger already has handlers
        formatter = logging.Formatter('%(asctime)s %(message)s')

        file_handler = logging.FileHandler(log_file_path, mode="a")
        file_handler.setFormatter(formatter)

        logger.setLevel(logging.INFO)
        logger.addHandler(file_handler)

    return logger