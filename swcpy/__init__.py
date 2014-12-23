from swc import ffi, lib


class Screen(object):
    def __init__(self, swc_screen, screen_handler):
        self.swc_screen = swc_screen
        self._id = id(swc_screen)

        # struct with the id of the screen
        screen_data = ffi.new("struct screen *")
        screen_data.screen_id = self._id
        self._screen_data = screen_data

        # lib.swc_screen_set_handler(swc_screen, screen_handler, screen_data)

    @property
    def usable_geometry(self):
        return self.swc_screen.usable_geometry


class Window(object):
    def __init__(self, swc_window, window_handler):
        self._tiled = False
        self._id = id(swc_window)
        self.swc_window = swc_window

        # struct with the id of the window
        window_data = ffi.new("struct window *")
        window_data.window_id = self._id
        self._window_data = window_data

        lib.swc_window_set_handler(
            swc_window,
            window_handler,
            window_data
            )

    @property
    def title(self):
        title = getattr(self.swc_window, "title", None)
        if not title:
            return ""
        return ffi.string(title)

    @property
    def wm_class(self):
        wm_class = getattr(self.swc_window, "class", None)
        if not wm_class:
            return ""
        return ffi.string(wm_class)

    def focus(self):
        lib.swc_window_focus(self.swc_window)

    def set_border(self, color, width=1):
        lib.swc_window_set_border(self.swc_window, color, width)

    def hide(self):
        lib.swc_window_hide(self.swc_window)

    def show(self):
        lib.swc_window_show(self.swc_window)

    def set_geometry(self, x, y, width, height):
        geometry = ffi.new("struct swc_rectangle *")
        geometry.x = x
        geometry.y = y
        geometry.width = width
        geometry.height = height

        lib.swc_window_set_geometry(self.swc_window, geometry)

    @property
    def tiled(self):
        return self._tiled

    @tiled.setter
    def tiled(self, is_tiled):
        self._tiled = is_tiled
        if is_tiled:
            lib.swc_window_set_tiled(self.swc_window)
        else:
            lib.swc_window_set_stacked(self.swc_window)


class Manager(object):
    def __init__(self):
        self.screens = {}
        self.windows = {}

        self.screen_handler = ffi.new("struct swc_screen_handler *")
        self.setup_window_handler()
        self.setup_swc_manager()

        # TODO
        # self.screen_handler.entered = self._on_screen_entered
        # self.screen_handler.destroy = self._on_screen_destroy
        # self.screen_handler.geometry_changed = self.on_geometry_change
        # self.screen_handler.usable_geometry_changed = self.on_geometry_change

        self.wl_display = lib.wl_display_create()
        lib.wl_display_add_socket(self.wl_display, ffi.NULL)
        self.event_loop = lib.wl_display_get_event_loop(self.wl_display)

    def setup_swc_manager(self):
        self.swc_manager = ffi.new("struct swc_manager *")

        @ffi.callback("void (* new_screen)(struct swc_screen * screen)")
        def on_new_screen(swc_screen):
            screen = Screen(swc_screen, self.screen_handler)
            self.screens[screen._id] = screen
            self.on_new_screen(screen._id)
        self._on_new_screen = on_new_screen

        @ffi.callback("void (* new_window)(struct swc_window * window)")
        def on_new_window(swc_window):
            window = Window(swc_window, self.window_handler)
            self.windows[window._id] = window
            self.on_new_window(window._id)
        self._on_new_window = on_new_window

        self.swc_manager.new_window = self._on_new_window
        self.swc_manager.new_screen = self._on_new_screen

    def setup_window_handler(self):
        self.window_handler = ffi.new("struct swc_window_handler *")

        @ffi.callback("void (* entered)(void * data)")
        def on_window_entered(data):
            window_data = ffi.cast("struct window *", data)
            wid = window_data.window_id
            self.on_window_entered(wid)
        self._on_window_entered = on_window_entered

        @ffi.callback("void (* destroy)(void * data)")
        def on_window_destroy(data):
            window_data = ffi.cast("struct window *", data)
            wid = window_data.window_id

            window = self.windows[wid]
            window.hide()
            del self.windows[wid]
            self.on_window_destroy(wid)
        self._on_window_destroy = on_window_destroy

        self.window_handler.entered = self._on_window_entered
        self.window_handler.destroy = self._on_window_destroy

    def initialize(self):
        lib.swc_initialize(self.wl_display, self.event_loop, self.swc_manager)
        lib.wl_display_run(self.wl_display)
        # lib.wl_display_destroy(wl_display)

    def on_new_screen(self, sid):
        pass

    def on_new_window(self, wid):
        pass

    def on_window_entered(self, wid):
        pass

    def on_window_destroy(self, wid):
        pass
