import pyttsx3 as tts

class TTS:
    def __init__(self):
        self.engine = tts.init()
        self.set_speed()
        self.set_voice()
        self.set_volume()

    def set_speed(self, speed: int = 130):
        self.engine.setProperty('rate', speed)

    def set_voice(self, voice_id: bool = 1):
        # 0 for male voice, 1 for female voice
        self.engine.setProperty('voice', self.engine.getProperty('voices')[voice_id].id)

    def set_volume(self, volume: float = 1.0):
        self.engine.setProperty('volume', volume)

    def speak(self, text: str):
        self.engine.say(text)
        self.engine.runAndWait()

    def stop(self):
        self.engine.stop()

if __name__ == '__main__':
    tts = TTS()
    tts.speak('Take a look at my machine jack')
    tts.stop()