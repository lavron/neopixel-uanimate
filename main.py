import neopixel
from machine import Pin
from neopixel_animate import NeopixelAnimate, PulseAnimation, RainbowAnimation, RotateAnimation
import uasyncio as asyncio

strip_len = 250

strip = neopixel.NeoPixel(Pin(22), strip_len)

GREEN = (0, 128, 0)
RED = (128, 0, 0)
BLUE = (0, 0, 128)
BLACK = (0, 0, 0)

breath = PulseAnimation(strip_len, 800, color=BLUE)
offline = PulseAnimation(strip_len, 2000, color=RED)
rainbow = RainbowAnimation(strip_len, 2000)
rotate = RotateAnimation(strip_len, 2000, color=BLUE, color_bg=BLACK, dir='cw')


# adding user's animation
# offset is float 0.0 ~ 1.0
class FillAnimation(NeopixelAnimate):
    def frame(self, offset):
        color = self.params.get("color_passed_to_fill")
        active_px = int(self.len * offset)
        for i in range(self.len):
            if i <= active_px:
                self.leds[i] = color
            else:
                self.leds[i] = BLACK

#callback example
def fill_animation_callback():
    print("Fill animation completed")


fill = FillAnimation(strip_len, 3000, color_passed_to_fill=GREEN,
                     loop=False, callback=fill_animation_callback)

animations = [breath, offline, rainbow, fill, rotate]

active_animation = breath
pointer = 0


async def toggle_animation():
    global pointer, active_animation
    while True:
        await asyncio.sleep_ms(5000)
        print("Toggling animation")
        pointer = pointer + 1
        if pointer >= len(animations):
            pointer = 0
        active_animation = animations[pointer]
        active_animation.start()


async def process_animation():
    while True:
        frame = active_animation.get_frame()
        if frame:
            for i in range(strip_len):
                strip[i] = frame[i]
            strip.write()
        await asyncio.sleep_ms(50)
        

loop = asyncio.get_event_loop()

loop.create_task(process_animation())
loop.create_task(toggle_animation())

loop.run_forever()