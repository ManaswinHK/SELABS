import array
import math
import pygame

SAMPLE_RATE = 22050


def _tone(freqs, duration, volume=0.4):
    """Build a Sound from a sequence of (frequency, fraction-of-duration) steps."""
    n = int(SAMPLE_RATE * duration)
    buf = array.array("h")
    for i in range(n):
        t = i / SAMPLE_RATE
        freq = freqs[min(len(freqs) - 1, int(i / n * len(freqs)))]
        envelope = 1 - i / n  # linear fade-out avoids clicks
        buf.append(int(32767 * volume * envelope * math.sin(2 * math.pi * freq * t)))
    return pygame.mixer.Sound(buffer=buf.tobytes())


class SoundManager:
    """Generates simple sound effects at runtime; silently disabled if no audio device."""

    def __init__(self):
        self.enabled = False
        self.sounds = {}
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=1)
            self.sounds = {
                "bounce": _tone([220], 0.08),
                "win": _tone([523, 659, 784, 1047], 0.6),
                "timeout": _tone([392, 330, 262, 196], 0.7),
            }
            self.enabled = True
        except pygame.error:
            pass

    def play(self, name):
        if self.enabled:
            self.sounds[name].play()
