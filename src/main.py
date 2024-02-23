import flet as ft
from flet_core import Page, MainAxisAlignment, CrossAxisAlignment, ControlEvent, ThemeMode

from src.app_bar import AppBar
from src.theme_icon import ThemeIcon
from src.timer import Timer


def main(page: Page):
    def save_state_page(event: ControlEvent):
        if event.data == "close":
            timer_data: dict = page.client_storage.get("timer_data") or {}
            timer_data.update({"theme_mode": page.theme_mode})
            page.client_storage.set("timer_data", timer_data)
            page.window_destroy()

    def get_theme_mode_save_data():
        if timer_data := page.client_storage.get("timer_data"):
            return ThemeMode(timer_data["theme_mode"])
        return ThemeMode(page.platform_brightness)

    page.window_center()
    page.title = "Timer"
    page.window_width = 250
    page.window_height = 330
    page.window_resizable = False
    page.window_full_screen = False
    page.window_maximizable = False
    page.theme_mode = get_theme_mode_save_data()
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.window_prevent_close = True
    page.on_window_event = save_state_page

    theme_icon = ThemeIcon(page)
    page.appbar = AppBar(page, theme_icon).build()

    timer = Timer()
    timer.init()
    page.add(timer)

    page.update()


ft.app(target=main)
