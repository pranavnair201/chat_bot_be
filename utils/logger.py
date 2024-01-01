import logging

def get_logger(session_id):
    logging.basicConfig(
        level=logging.INFO,
        filename=f"session_logs/session_{session_id}.log",
        filemode="w",
        format="%(asctime)s %(message)s"
    )
    return logging