
class ViewPort: 
    
    def __init__(self, vpx, vpy, window) -> None:
        self.vpxmax = vpx
        self.vpymax = vpy
        self.vpxmin = 0
        self.vpymin = 0
        self.window = window

    def transform(self, x, y):
        wcmax = (self.window.wxmax, self.window.wymax)
        wcmin = (self.window.wxmin, self.window.wymin)
        vp_x = (((x - wcmin[0]) / (wcmax[0] - wcmin[0])) * (self.vpxmax - self.vpxmin))
        vp_y = ((1 - ((y - wcmin[1]) / (wcmax[1] - wcmin[1]))) * (self.vpymax - self.vpymin))
        return (vp_x, vp_y)
