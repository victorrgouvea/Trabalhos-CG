class Window:

    def __init__(self, wx, wy) -> None:
        self.wxmin = 0
        self.wymin = 0
        self.wxmax = wx
        self.wymax = wy
        self.sizex = wx
        self.sizey = wy
        self.scale = [2, 2]
        self.center = [0, 0]
        self.angle_offset = 0

    def change_offset(self, x, y):
        self.wxmin += x
        self.wymin += y
        self.wxmax += x
        self.wymax += y
        self.update_center()

    def change_zoom(self, min, max):
        self.wxmin += min
        self.wymin += min
        self.wxmax += max
        self.wymax += max
        self.update_center()

    def update_center(self):
        self.update_sizes()
        self.center = [round((self.wxmin + self.wxmax) / 2, 2), round((self.wymin + self.wymax) / 2, 2)]

    def update_sizes(self):
        self.sizex = self.wxmax - self.wxmin
        self.sizey = self.wymax - self.wymin

    def update_scale(self):
        self.update_center()
        return [round(2/self.sizex, 3), round(2/self.sizey, 3)]

    def rotate(self, angle):
        self.angle_offset += angle
