#!/usr/bin/python2
import math

from swcpy import Manager

border_width = 4
border_color_normal = 0xff888888
border_color_active = 0xff333388


class WManager(Manager):
    """
    Super simple wm example, assuming that there's only one screen
    """

    def __init__(self):
        super(WManager, self).__init__()
        self.focused = None

    def arrange(self):
        screen = self.screens.values()[0]
        geometry = screen.usable_geometry

        windows = self.windows.values()

        num_windows = len(windows)
        if num_windows == 0:
            return

        columns = int(math.ceil(math.sqrt(num_windows)))
        rows = int(num_windows / columns + 1)

        for nc in range(columns):
            if not windows:
                break

            x = y = width = height = 0
            x = geometry.x + border_width + geometry.width * nc / columns
            width = geometry.width / columns - 2 * border_width

            if (nc == num_windows % columns):
                rows -= 1

            for nr in range(rows):
                window = windows.pop()
                y = geometry.y + border_width + geometry.height * nr / rows
                height = geometry.height / rows - 2 * border_width
                window.set_geometry(x, y, width, height)

                if not windows:
                    break

    def on_new_screen(self, sid):
        pass

    def on_new_window(self, wid):
        window = self.windows[wid]
        window.tiled = True
        self.focus(window)
        window.show()
        self.arrange()

    def on_window_entered(self, wid):
        window = self.windows.get(wid, None)
        self.focus(window)

    def focus(self, window):
        if self.focused:
            self.focused.set_border(border_color_normal, border_width)
        self.focused = window
        window.set_border(border_color_active, border_width)
        window.focus()

    def on_window_destroy(self, wid):
        self.arrange()


if __name__ == "__main__":
    wmanager = WManager()
    wmanager.initialize()
