import logging

BOARD = 0
BCM = 1
OUT = 1
IN = 0
HIGH = 1
LOW = 0

def setmode(a):
    logging.info(f"Setting mode to {a}.")

def setup(a, b):
    if b == OUT:
        logging.info(f"Setting up GPIO@{a} as Output.")
    else:
        logging.info(f"Setting up GPIO@{a} as Input.")

def output(a, b):
    if b == HIGH:
        logging.info(f"Setting GPIO@{a} to On.")
    else:
        logging.info(f"Setting GPIO@{a} to Off.")

def cleanup():
    logging.info("Cleaning up.")

def setwarnings(flag):
    logging.info(f"Setting warning: {flag}")