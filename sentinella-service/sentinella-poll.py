import time
from datetime import datetime

from config.config import PASSED, FAILED
from travis_polling.travis_polling import TravisSub
from pi_control.led.led_control import turn_on_led
from pi_control.led.led_control import LED_GREEN, LED_RED, LED_YELLOW

from pi_control.buzz.buzz_control import buzz

from config.config import read_sentinella_config

subscribe = True
buzz_on = True

PASSED_BUZZ = 0
ERROR_BUZZ = 1
FAILED_BUZZ = 2

DEFAULT_SLEEP_SEC = 600  # 10 minutes
MIN_SLEEP_SEC = 120  # 2 minutes


def __buzz(buzz_type):
    global buzz_on
    if buzz_on:
        buzz(buzz_type)


def start_subscribe():
    global subscribe, buzz_on
    subscribe = True

    while subscribe:

        buzz_on, start_time_str, end_time_str = read_sentinella_config()

        start_time = datetime.strptime(start_time_str, "%I:%M%p").time()
        end_time = datetime.strptime(end_time_str, "%I:%M%p").time()
        time_now = datetime.now().time()

        if start_time < time_now < end_time:

            subs = TravisSub()
            status = subs.generate_report()

            if status == PASSED:
                turn_on_led(LED_GREEN)
                __buzz(PASSED_BUZZ)
            elif status == FAILED:
                turn_on_led(LED_RED)
                __buzz(FAILED_BUZZ)
            else:
                turn_on_led(LED_YELLOW)
                __buzz(ERROR_BUZZ)

            print "Last update time: {}".format(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        time.sleep(DEFAULT_SLEEP_SEC)


def stop_subscribe():
    global subscribe
    subscribe = False


if __name__ == "__main__":
    start_subscribe()
