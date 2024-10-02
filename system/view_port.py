class ViewPort:

    def __init__(self, vpx, vpy, window) -> None:
        self.vpxmax = vpx
        self.vpymax = vpy
        self.vpxmin = 0
        self.vpymin = 0
        self.window = window

    def transform(self, x, y):
        wcmax =  [1, 1]
        wcmin = [-1, -1]
        x += 0.3
        vp_x = (((x - wcmin[0]) / (wcmax[0] - wcmin[0])) * (self.vpxmax - self.vpxmin))
        vp_y = ((1 - ((y - wcmin[1]) / (wcmax[1] - wcmin[1]))) * (self.vpymax - self.vpymin))
        #vp_x += (self.vpxmax - self.vpxmin)/8
        return [vp_x, vp_y]
