# https://www.youtube.com/watch?v=a1_O9AnuGB0
import neopixel
from machine import Pin
from neopixel_animate import NeopixelAnimate, mix, wave, random_color
import uasyncio as asyncio
import utime

import random

strip_len = 25

strip = neopixel.NeoPixel(Pin(25), strip_len)

GREEN = (0, 128, 0)
RED = (128, 0, 0)
BLUE = (0, 0, 128)
BLACK = (0, 0, 0)

direction = 1


class SoftMixAnimation(NeopixelAnimate):
    def __init__(self, strip_len, duration_ms=0, **params):
        super().__init__(strip_len, duration_ms=duration_ms, **params)

        self.params['bg_color'] = random_color()
        self.params['active_color'] = random_color()
        self.params['direction'] = 1

    def new_color(self):
        self.params['bg_color'] = self.params['active_color']
        self.params['active_color'] = random_color()
        self.params['direction'] = 1 - self.params['direction']

    def frame(self, offset):
        edge_px = 8
        bg_color = self.params['bg_color']
        active_color = self.params['active_color']

        active_px = self.len * offset
        offset = active_px % 1
        filled_px = int(active_px) - edge_px

        result = [0] * self.len

        for i in range(self.len):
            if i < filled_px:
                result[i] = active_color

            elif i <= active_px:
                j = i - filled_px
                blur_offset = max((offset - 1 - j) /
                                  edge_px + 1, 0)  # magic formula
                result[i] = mix(active_color, bg_color, blur_offset)

            else:
                result[i] = bg_color

            # result = result[init_px:] + result[:init_px]
        if self.params['direction'] == 1:
            result.reverse()

        for i in range(self.len):
            self.leds[i] = result[i]


def new_color():
    print("new_soft_mix callback")
    soft_mix.new_color()


soft_mix = SoftMixAnimation(strip_len, 5000, callback=new_color)


async def process_animation():
    frame = False
    soft_mix.start()
    while True:
        frame = soft_mix.get_frame()

        if frame:
            # print("frame:", frame)
            for i in range(strip_len):
                strip[i] = frame[i][:]
            strip.write()

        await asyncio.sleep_ms(50)


loop = asyncio.get_event_loop()

loop.create_task(process_animation())

loop.run_forever()
