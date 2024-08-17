import logging

def setup_logging():
    logging.basicConfig(
        filename='app.log',
        level=logging.DEBUG,
        format='%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
