import pyautogui as pyag
#from gameStrategy.cardCounting import updateCount
import time


def take_screenshot():
    im1 = pyag.screenshot()
    im1.save('my_screenshot.png')

def main():
    interval = 0.5  # in seconds
    while True:
        print("Timer is running...")
        time.sleep(interval)
        take_screenshot()

main()