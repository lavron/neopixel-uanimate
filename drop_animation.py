# https://www.youtube.com/watch?v=a1_O9AnuGB0
import neopixel
from machine import Pin
from neopixel_animate import NeopixelAnimate, PulseAnimation, RainbowAnimation, RotateAnimation
import uasyncio as asyncio
import urandom
import utime

strip_len = 25

strip = neopixel.NeoPixel(Pin(22), strip_len)

GREEN = (0, 128, 0)
RED = (128, 0, 0)
BLUE = (0, 0, 128)
BLACK = (0, 0, 0)


class DropAnimation(NeopixelAnimate):
    # def __init__(self, strip_len, duration_ms=0, **params):
    #     super().__init__(strip_len, duration_ms=duration_ms, **params)
        # self.hot_points = [0] * self.len
    def frame(self, offset):
        width_px = randint(5, 7)
        init_px = randint(0, self.len)
        edge_px = randint(1, 3)
        
        print("Generated drop. Width: %s, init:%s, edge: %s", width_px, init_px, edge_px)
        
        active_px = width_px * wave(offset)
        blur = active_px%1
        filled_px = int(active_px) - edge_px

        for i in range(self.len):
            if i <= filled_px:
                result[i] = BLUE
            elif i <= active_px:
                blur_offset = blur - i / edge_px
                result[i] = mix(BLUE, BLACK, blur_offset)
            else:
                result[i] = BLACK

        result = result[init_px:] + result[:init_px]
        
        for i in range(self.len):
            self.leds[i] = result[i]


drop = DropAnimation(strip_len, 2000)


def randint(min, max):
    span = max - min + 1
    div = 0x3fffffff // span
    offset = urandom.getrandbits(30) // div
    val = min + offset
    return val


def wave(offset):
    if offset > 0.5:
        offset = 1 - offset
    return offset * 2


async def process_animation():
    drop.start()
    while True:
        frame = drop.get_frame()
        if frame:
            for i in range(strip_len):
                strip[i] = frame[i][:]
            strip.write()
        await asyncio.sleep_ms(50)


loop = asyncio.get_event_loop()

loop.create_task(process_animation())

loop.run_forever()