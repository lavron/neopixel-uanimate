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



### Custom animations

You can extend the controler wit hown animations. Be sure to pass strip length and loop duration in ms.

```python
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
```

## Authors

* **Viktor Lavron** - *Initial work* - [https://lavron.info](https://lavron.info)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

<!-- ## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc -->
