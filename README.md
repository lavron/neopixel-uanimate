# Neopixel uAnimate

Micropython library for the animations on the Neopixels (WS2812 etc)

## Getting Started

Import library and/or animations
```python
import time
from neopixel_animate import NeopixelAnimate, PulseAnimation
```
Initiate animation

```python
strip_len = 24
duration_ms = 1000
breath = PulseAnimation(strip_len, duration_ms, color=BLUE)

breath.start()

while True:
    frame = breath.get_frame()
    if frame:
        for i in range(strip_len):
            strip[i] = frame[i]
        strip.write()

```

### Basic animations

Three basic animations included: 

1. Rainbow
2. Pulse
3. Rotate

![video with example_simple.py running on the WS2812B strip](https://github.com/lavron/neopixel-uanimate/blob/master/img/preview.gif)


Check this video with example_simple.py running on the WS2812B strip:
https://www.youtube.com/watch?v=a1_O9AnuGB0



### Custom animations

You can extend the controler with own animations. 
Defined 'frame()' method should accept 'offset' argument (between 0 and 1), and set color for every self.leds[el].

Be sure to pass strip length and loop duration in ms.

```python
# filling strip with BLUE from bottom to top
class FillAnimation(NeopixelAnimate):
    def frame(self, offset):
        active_px = int(self.len * offset)
        for i in range(self.len):
            self.leds[i] = BLUE if i <= active_px else BLACK

#callback example
def fill_animation_callback():
    print("Fill animation completed")


fill = FillAnimation(strip_len, 3000, loop=False, callback=fill_animation_callback)
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details