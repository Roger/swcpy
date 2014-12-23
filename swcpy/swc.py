from cffi import FFI

ffi = FFI()

# Wayland
ffi.cdef("""
struct wl_display *wl_display_create(void);
int wl_display_add_socket(struct wl_display *display, const char *name);
struct wl_event_loop *wl_display_get_event_loop(struct wl_display *display);
void wl_display_run(struct wl_display *display);
""")

# Internal
ffi.cdef("""
struct screen
{
    long screen_id;
};

struct window
{
    long window_id;
};
""")

# SWC
ffi.cdef("""
struct swc_rectangle
{
    int32_t x, y;
    uint32_t width, height;
};

struct swc_screen
{
    struct swc_rectangle geometry;
    struct swc_rectangle usable_geometry;
};

struct swc_window
{
    char * title;
    char * class;

    struct swc_window * parent;
};


struct swc_manager
{
    void (* new_screen)(struct swc_screen * screen);
    void (* new_window)(struct swc_window * window);
};

bool swc_initialize(struct wl_display * display,
                    struct wl_event_loop * event_loop,
                    const struct swc_manager * manager);



struct swc_screen_handler
{
    void (* destroy)(void * data);
    void (* geometry_changed)(void * data);
    void (* usable_geometry_changed)(void * data);
    void (* entered)(void * data);
};

struct swc_window_handler
{
    void (* destroy)(void * data);
    void (* title_changed)(void * data);
    void (* class_changed)(void * data);
    void (* parent_changed)(void * data);
    void (* entered)(void * data);
    void (* move)(void * data);
    void (* resize)(void * data);
};

void swc_screen_set_handler(struct swc_screen * screen,
                            const struct swc_screen_handler * handler,
                            void * data);

void swc_window_set_tiled(struct swc_window * window);
void swc_window_set_stacked(struct swc_window * window);

void swc_window_set_handler(struct swc_window * window,
                            const struct swc_window_handler * handler,
                            void * data);
void swc_window_show(struct swc_window * window);
void swc_window_hide(struct swc_window * window);
void swc_window_focus(struct swc_window * window);
void swc_window_set_border(struct swc_window * window,
                           uint32_t color, uint32_t width);
void swc_window_set_geometry(struct swc_window * window,
                             const struct swc_rectangle * geometry);
""")

lib = ffi.verify(
    """
    #include <wayland-server.h>
    #include <swc.h>

    struct screen
    {
        long screen_id;
    };

    struct window
    {
        long window_id;
    };
    """,
    libraries=["wayland-server", "swc"]
)
