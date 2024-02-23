import flet as ft
from flet_core import UserControl, Page, ControlEvent

from src.theme_icon import ThemeIcon


class AppBar(UserControl):
    def __init__(self, page: Page, theme_icon: ThemeIcon):
        super().__init__()
        self.page = page
        self.theme_icon = theme_icon

    def build(self):
        timer_data = self.page.client_storage.get("timer_data") or {}
        return ft.AppBar(
            toolbar_height=40,
            center_title=False,
            actions=[
                self.theme_icon,

                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(text="Dimming brightness", checked=timer_data.get("dimming_brightness", False),
                                         on_click=self.dimming_brightness),
                    ]
                ),
            ],
        )

    def dimming_brightness(self, event: ControlEvent):
        event.control.checked = not event.control.checked
        page_data = self.page.client_storage.get("timer_data")
        page_data["dimming_brightness"] = event.control.checked
        self.page.client_storage.set("timer_data", page_data)
        self.page.update()
