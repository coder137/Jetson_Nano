"""
Usage:
python3 gpp.py --operation [input/output] --pin [pin_number] --state [1/0]
"""
import time
import argparse
import logging

import Jetson.GPIO as GPIO


def args_get():
    """
    Create an argument parser
    """
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "--operation", help="--operation input/output", required=True)
    parser.add_argument("--pin", help="--pin <pin_number>", required=True)
    parser.add_argument(
        "--state", help="--state <1/0>\nNOTE: Only used when operation=output")
    args = parser.parse_args()
    logging.info(f"args: {args}")
    logging.info(f"operation: {args.operation}")
    logging.info(f"pin: {args.pin}")

    operation: str = args.operation.lower()
    try:
        pin: int = int(args.pin)
    except:
        logging.error("Pass a valid pin number")
        exit(EXIT_FAILURE)

    state = args.state
    if operation.lower() == "output":
        if state == None:
            logging.error(
                "When operation is 'output' make sure `state` is supplied")
            exit(EXIT_FAILURE)
        else:
            state = int(args.state)
            logging.info(f"sanitized_state: {state}")
            if state == 1 or state == 0:
                pass
            else:
                logging.error("State can only be 1 or 0")
                exit(EXIT_FAILURE)

    return (operation, pin, state)


def output_operation(pin, state):
    """
    Perform the OUTPUT operation
    """
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, state)
    GPIO.cleanup()


def input_operation(pin):
    """
    Perform the INPUT operation
    """
    GPIO.setup(pin, GPIO.IN)
    print("Ctrl+C to exit")
    while 1:
        try:
            value = GPIO.input(pin)
            print(f"GPIO_READ pin {pin}: {value}")
            time.sleep(1)
        except KeyboardInterrupt:
            break
    GPIO.cleanup()


# CONSTANTS
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

if __name__ == '__main__':
    # Set the default options here
    logging.basicConfig(level=logging.WARNING)
    GPIO.setmode(GPIO.BOARD)

    # Get arguments
    operation, pin, state = args_get()

    # Perform operation
    if operation == "input":
        input_operation(pin)
    elif operation == "output":
        output_operation(pin, state)
    else:
        logging.error(
            "Incorrect operation selected i.e either 'output'/'input' allowed")
