from screenshot import screenshot
import time

def main():
    interval = 0.5  # in seconds
    while True:
        print("Timer is running...")
        time.sleep(interval)
        screenshot()

main()