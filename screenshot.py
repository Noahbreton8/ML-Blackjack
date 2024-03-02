import pyautogui as pyag

def screenshot():
    im1 = pyag.screenshot()
    im1.save('my_screenshot.png')