#!/usr/bin/python2
import math

from swcpy import Manager

border_width = 4
border_color_normal = 0xff888888
border_color_active = 0xff333388


class WManager(Manager):
    def __init__(self):
        super(WManager, self).__init__()
        self.focused = None

    def arrange(self):
        screen = self.screens.values()[0]
        screen_geometry = screen.usable_geometry

        windows = self.windows.values()

        num_windows = len(windows)
        if num_windows == 0:
            return

        num_columns = int(math.ceil(math.sqrt(num_windows)))
        num_rows = int(num_windows / num_columns + 1)

        for nc in range(num_columns):
            if not windows:
                break

            geometry = {"x": 0, "y": 0, "width": 0, "height": 0}
            geometry["x"] = screen_geometry.x + border_width + \
                screen_geometry.width * nc / num_columns
            geometry["width"] = screen_geometry.width / num_columns \
                - 2 * border_width

            if (nc == num_windows % num_columns):
                num_rows -= 1

            for nr in range(num_rows):
                window = windows.pop()
                geometry["y"] = screen_geometry.y + border_width + \
                    screen_geometry.height * nr / num_rows
                geometry["height"] = screen_geometry.height / num_rows - 2 * \
                    border_width
                window.set_geometry(**geometry)
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
