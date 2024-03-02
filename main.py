from screenshot import screenshot
#from gameStrategy.cardCounting import updateCount
import time

deck = {
    '2h': 2, '3h': 3, '4h': 4, '5h': 5, '6h': 6, '7h': 7, '8h': 8, '9h': 9, '10h': 10, 'jh': 10, 'qh': 10, 'kh': 10, 'ah': 11,
    '2d': 2, '3d': 3, '4d': 4, '5d': 5, '6d': 6, '7d': 7, '8d': 8, '9d': 9, '10d': 10, 'jd': 10, 'qd': 10, 'kd': 10, 'ad': 11,
    '2c': 2, '3c': 3, '4c': 4, '5c': 5, '6c': 6, '7c': 7, '8c': 8, '9c': 9, '10c': 10, 'jc': 10, 'qc': 10, 'kc': 10, 'ac': 11,
    '2s': 2, '3s': 3, '4s': 4, '5s': 5, '6s': 6, '7s': 7, '8s': 8, '9s': 9, '10s': 10, 'js': 10, 'qs': 10, 'ks': 10, 'as': 11,
}

currentCount = 0

def main():
    interval = 0.5  # in seconds
    while True:
        print("Timer is running...")
        time.sleep(interval)
        screenshot()
    
main()