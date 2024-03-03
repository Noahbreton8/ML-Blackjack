from nicegui import ui
from gameStrategy import cardCounting
from gameStrategy import tts
import cv2
import time
from nicegui.events import KeyEventArguments
import os
import atexit

url = "http://machinejack.tech"
deck = {
    '2h': 2, '3h': 3, '4h': 4, '5h': 5, '6h': 6, '7h': 7, '8h': 8, '9h': 9, '10h': 10, 'jh': 10, 'qh': 10, 'kh': 10, 'ah': 11,
    '2d': 2, '3d': 3, '4d': 4, '5d': 5, '6d': 6, '7d': 7, '8d': 8, '9d': 9, '10d': 10, 'jd': 10, 'qd': 10, 'kd': 10, 'ad': 11,
    '2c': 2, '3c': 3, '4c': 4, '5c': 5, '6c': 6, '7c': 7, '8c': 8, '9c': 9, '10c': 10, 'jc': 10, 'qc': 10, 'kc': 10, 'ac': 11,
    '2s': 2, '3s': 3, '4s': 4, '5s': 5, '6s': 6, '7s': 7, '8s': 8, '9s': 9, '10s': 10, 'js': 10, 'qs': 10, 'ks': 10, 'as': 11,
}
deckNumber = 2
currentCount = 3
hand = ["2h", "3h", "4h"]

tts = tts.TTS()

capture = cv2.VideoCapture(0)
iframe = 0
piframe = 0

@ui.refreshable
def build_home_page():
    keyboard = ui.keyboard(on_key=handle_key)

    ui.label("Machine Jack").style("""
                                   font-size: 48px;
                                    margin: auto;
                                    width: 50%;
                                   """)
    ui.label(currentCount)

    voice_select = ui.select({0: "male", 1: "female"}, value=1, on_change=lambda: tts.set_voice(voice_select.value))

    volume_slider = ui.slider(min=0, max=100, value=100, on_change=lambda: tts.set_volume(volume_slider.value / 100))
    ui.label().bind_text_from(volume_slider,'value')

    speed_slider = ui.slider(min=50, max=150, value=130, on_change=lambda: tts.set_speed(speed_slider.value))
    ui.label().bind_text_from(speed_slider,'value')

    ui.button("Speak", on_click=lambda: tts.speak("Take a look at my machine jack"))

def update_count():
    global currentCount
    newcc = cardCounting.update_count(hand[-1], deck, deckNumber)
    if newcc != currentCount:
        currentCount += newcc
        build_home_page.refresh()

def handle_key(e: KeyEventArguments):
    global iframe
    global piframe
    if e.key == 's' and not e.action.repeat:
        if e.action.keydown:
            iframe = time.time()
            if not os.path.exists('images'):
                os.makedirs('images')
            if piframe != 0:
                os.remove(f'images/cam-{piframe}.png')
            ret, frame = capture.read()
            cv2.imwrite(f'images/cam-{iframe}.png', frame)
            build_home_page.refresh()
        elif e.action.keyup:
            ui.image(f'images/cam-{iframe}.png')
            piframe = iframe

def main():
    build_home_page()
    ui.run()

if __name__ in {"__main__", "__mp_main__"}:
    main()