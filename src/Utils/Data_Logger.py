import logging

logging.basicConfig(
    level = logging.INFO,
    format  = '%(asctime)s - %(levelname)s - %(message)s',
    handlers =[
        # logging.FileHandler(file_name),
        logging.StreamHandler()
    ],
    force=True
)

def log_info(message):
    logging.info(message)

def log_warning(message):
    logging.warning(message)

def log_error(message):
    logging.error(message)