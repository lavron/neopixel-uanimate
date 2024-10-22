import utime
import math
import random


class NeopixelAnimate:
    def __init__(self, strip_len, duration_ms=0, **params):
        self.len = strip_len
        self.params = params
    

        self.duration_ms = duration_ms
        self.start_ms = 0
        self.now_ms = utime.ticks_ms()
        self.status = False  # passive

        self.loop = params.get("loop") if 'loop' in params else True

        self.leds = [0] * self.len

        self.frame_count = 0

    def start(self):
        self.start_ms = utime.ticks_ms()
        self.status = True  # active

    def stop(self):
        if 'callback' in self.params:
            callback = self.params.get("callback")
            callback()
        self.status = False
        self.frame_count = 0

    def frame(self, offset):
        return self.leds

    def fill(self, color):
        for i in range(self.len):
            self.leds[i] = color

    def get_frame(self):
        if self.status == False:
            # bail, no active animation
            return False
        self.frame_count += 1

        self.now_ms = utime.ticks_ms()
        passed_ms = utime.ticks_diff(self.now_ms, self.start_ms)

        if passed_ms >= self.duration_ms:
            # animation time is over
            self.stop()
            if not self.loop:
                return False
            self.start()

        offset = (passed_ms % self.duration_ms)/self.duration_ms

        self.frame(offset)

        return self.leds


class RainbowAnimation(NeopixelAnimate):
    def frame(self, offset):
        sat = 1.0
        bri = 0.2
        for i in range(self.len):
            hue = (360*(offset + i/self.len)) % 360
            color = hsv2rgb(hue, sat, bri)
            self.leds[i] = color


class PulseAnimation(NeopixelAnimate):
    def frame(self, offset):
        color = self.params.get("color")
        color = rgb2hsv(color)
        val = color[2] * wave(offset)
        color = hsv2rgb(color[0], color[1], val)
        self.fill(color)


class RotateAnimation (NeopixelAnimate):
    def frame(self, offset):
        color = self.params.get("color")
        color_bg = self.params.get("color_bg")
        direction = self.params.get("dir") if 'dir' in self.params else 'cw'

        width_px = self.len // 2

        active_px = int(offset * self.len)

        result = [0] * self.len
        for i in range(self.len):
            result[i] = color if i < width_px else color_bg

        # shift result forward for active_px
        result = result[active_px:] + result[:active_px]

        if direction == "ccw":
            result.reverse()
        self.leds = result
        # print("self.leds:", self.leds)


def hsv2rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0:
        r, g, b = v, t, p
    elif hi == 1:
        r, g, b = q, v, p
    elif hi == 2:
        r, g, b = p, v, t
    elif hi == 3:
        r, g, b = p, q, v
    elif hi == 4:
        r, g, b = t, p, v
    elif hi == 5:
        r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b


def rgb2hsv(rgb):
    r, g, b = rgb
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return h, s, v


def wave(offset):
    if offset > 0.5:
        offset = 1 - offset
    return offset * 2


def lerp(a,  b,  f):
    return a + f * (b - a)


def mix(a, b, t):
    r1, g1, b1 = a
    r2, g2, b2 = b
    r = int(math.sqrt((1 - t) * r2 ** 2 + t * r1 ** 2))
    g = int(math.sqrt((1 - t) * g2 ** 2 + t * g1 ** 2))
    b = int(math.sqrt((1 - t) * b2 ** 2 + t * b1 ** 2))
    return (r, g, b)


count = 0
def random_color():
    global count
    color = [0,0,0]
    color[count] = random.randrange(256)
    a0 = random.randrange(1)
    
    a1 = ((1-a0)+count+1) % 3
    
    a0 = (count+a0+1) % 3
    color[a0] = 255-color[count]
    color[a1] = 0
    count += random.randrange(15)
    count %= 3
    print(color[0], color[1], color[2])
    return ( color[0], color[1], color[2])
     
