
class DropAnimation(NeopixelAnimate):
    def __init__(self, strip_len, duration_ms=0, **params):
        super().__init__(strip_len, duration_ms=duration_ms, **params)
        # self.loop = False
        self.drop = {
            'color1' : random_color(),
            'color2' : random_color(),
            'width_px':  25,
            
        }
        self.generate_drop()

    def generate_drop(self):
        print("self.drop:", self.drop)
        self.drop = {
            'init_px': random.randrange(0, self.len),
            'edge_px': random.randrange(4, 10),
            'color1' : self.drop['color2'],
            'color2' : random_color()
            
        }
        print("new drop:", self.drop)

    def frame(self, offset):

        drop = self.drop
        width_px = drop['width_px']
        init_px = drop['init_px']
        edge_px = drop['edge_px']
        
        color1 = drop['color1']
        color2 = drop['color2']

        active_px = width_px * wave(offset)
        offset = active_px % 1
        filled_px = int(active_px) - edge_px

        result = [0] * self.len

        for i in range(self.len):
            if i < filled_px:
                result[i] = color1

            elif i <= active_px:
                j = i - filled_px
                blur_offset = max((offset - 1 - j) / edge_px + 1, 0) #magic formula
                result[i] = mix(color1, color2, blur_offset)

            else:
                result[i] = color2

            # result = result[init_px:] + result[:init_px]
            
        for i in range(self.len):
            if self.leds[i] != BLACK:
                self.leds[i] = result[i]
            else:
                self.leds[i] = mix(result[i], self.leds[i], 0.5)

