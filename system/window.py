class Window:

    def __init__(self, wx, wy) -> None:
        self.wxmin = 0
        self.wymin = 0
        self.wxmax = wx
        self.wymax = wy

    def change_offset(self, x, y):
        self.wxmin += x 
        self.wymin += y
        self.wxmax += x
        self.wymax += y

    def change_zoom(self, min, max):
        self.wxmin += min
        self.wymin += min 
        self.wxmax += max
        self.wymax += max