"""
Usage:
python3 pwm.py --dir cw/acw --frequency 1-1000 --duty 1-100
"""
import Jetson.GPIO as GPIO
import time
import argparse
import logging

DIR = 18
STEP = 32
ENABLE = 15
MS2 = 12
MS1 = 11

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

def args_get():
    """
    Create an argument parser
    """
    parser = argparse.ArgumentParser(description="""
    Control the Stepper motor direction, frequency and duty cycle.\n
    Keep the duty cycle at 50 for accurate control.
    """)
    parser.add_argument(
        "--dir", help="--dir cw/acw", required=True)
    parser.add_argument("--frequency", help="--frequency <hz>", required=True)
    parser.add_argument(
        "--duty", help="--duty <dutycycle>", required=True)
    args = parser.parse_args()
    dir = args.dir.lower()
    if dir == "cw":
        dir = 0
    elif dir == "acw":
        dir = 1
    else:
        logging.error("dir can only be 'cw' or 'acw'")
        exit(EXIT_FAILURE)

    try:
        frequency : int = int(args.frequency)
        duty : int = int(args.duty)
    except:
        logging.error("Pass a valid frequency and duty")
        exit(EXIT_FAILURE)

    if frequency > 1000 or frequency < 1:
        logging.error("Valid frequency range is between 1 - 1000hz")
        exit(EXIT_FAILURE)

    if duty > 100 or duty < 1:
        logging.error("Valid duty is between 1 - 100")
        exit(EXIT_FAILURE)
    
    return dir, frequency, duty



def setup():
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)
    GPIO.setup(ENABLE, GPIO.OUT)
    GPIO.setup(MS1, GPIO.OUT)
    GPIO.setup(MS2, GPIO.OUT)
    reset_pins()
    # Open Serial connection for debugging
    print("Begin motor control")


def reset_pins():
    GPIO.output(DIR, GPIO.LOW)
    GPIO.output(STEP, GPIO.LOW)
    GPIO.output(MS2, GPIO.LOW)
    GPIO.output(MS1, GPIO.LOW)
    GPIO.output(ENABLE, GPIO.HIGH)


def cleanup():
    GPIO.cleanup()


def pwm(frequency, dutycycle):
    one_cycle = 1/frequency
    on_time = (dutycycle * one_cycle) / 100 
    off_time = one_cycle - on_time
    GPIO.output(STEP, GPIO.HIGH)
    time.sleep(on_time)
    GPIO.output(STEP, GPIO.LOW)
    time.sleep(off_time)

def main(dir, frequency, duty):
    setup()
    GPIO.output(DIR, dir)
    while 1:
        try:
            pwm(frequency, duty)
        except KeyboardInterrupt:
            break
    print("Cleaning up")
    reset_pins()
    cleanup()


# Run the main here
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    GPIO.setmode(GPIO.BOARD)

    dir, frequency, duty = args_get()
    logging.debug(f"dir: {dir}, frequency: {frequency} duty: {duty}")
    main(dir, frequency, duty)
