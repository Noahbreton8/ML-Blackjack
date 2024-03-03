from nicegui import ui
from gameStrategy import cardCounting
from gameStrategy import tts
import cv2
import time
from nicegui.events import KeyEventArguments
import os
import atexit
from modelApi import extractModelData

url = "http://machinejack.tech"

deckNumber = 2
currentCount = 3
hand = ["2h", "3h", "4h"]
displayMode = "Pick your display Mode"
isDarkMode = False
standard_text_ccs = """
                font-family: "Source Code Pro";

"""


tts = tts.TTS()

capture = cv2.VideoCapture(0)
iframe = 0
piframe = 0

@ui.refreshable
def build_home_page():
    keyboard = ui.keyboard(on_key=handle_key)
    start_css()
    ui.label("Machine Jack").style("""
                                    font-size: 48px;
                                    margin: auto;
                                    width: 50%;
                                    font-family: Anta;
                                    text-align: center;
                                   """)
    display_switch = ui.switch(displayMode, on_change= lambda: change_mode(display_switch))
    display_switch.bind_text_from(globals(), "displayMode")

    with ui.expansion("Control Center") as control_center:
        control_center.style('''
                                width: 400px;
                             '''+standard_text_ccs)

        ui.label(f"Card counting score: {currentCount}")

        voice_select = ui.select({0: "male", 1: "female"}, value=1, on_change=lambda: tts.set_voice(voice_select.value))

        volume_slider = ui.slider(min=0, max=100, value=100, on_change=lambda: tts.set_volume(volume_slider.value / 100))
        ui.label().bind_text_from(volume_slider,'value')

        speed_slider = ui.slider(min=50, max=250, value=130, on_change=lambda: tts.set_speed(speed_slider.value))
        ui.label().bind_text_from(speed_slider,'value')

        ui.button("Speak", on_click=lambda: tts.speak("The quick brown fox jumps over the small white dog"))

def start_css():
    ui.add_head_html('''
    <link href='https://fonts.googleapis.com/css?family=Source Code Pro' rel='stylesheet'>
    <link href='https://fonts.googleapis.com/css?family=Anta' rel='stylesheet'>
    ''')
    # <style>
    # @font-face {
    #     font-family: 'metalica';
    #     src: url('fonts/Metallica-Font/Pastor of Muppets.ttf');
    # }
    # </style>
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


def change_mode(switch: ui.switch):
    global isDarkMode
    global displayMode
    isDarkMode = not isDarkMode
    if isDarkMode:
        displayMode = "Dark"
        switch.style("color: rgb(126,75,104);")
    else:
        switch.style("color: rgb(195,182,50);")
        displayMode = "Light"
    ui.dark_mode(isDarkMode)


def main():
    build_home_page()
    ui.run()

if __name__ in {"__main__", "__mp_main__"}:
    main()