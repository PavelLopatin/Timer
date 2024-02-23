import flet as ft
from flet_core import UserControl, Page, ControlEvent, \
    ThemeMode


THEME_MODE = {
    ThemeMode.LIGHT: ThemeMode.DARK,
    ThemeMode.DARK: ThemeMode.LIGHT
}


class ThemeIcon(UserControl):

    def __init__(self, page: Page):
        super().__init__()
        self.page = page

    def build(self):
        if self.page.theme_mode == ThemeMode.DARK:
            return ft.IconButton(
                icon=ft.icons.LIGHT_MODE,
                selected_icon=ft.icons.DARK_MODE,
                on_click=self.change_theme
            )
        return ft.IconButton(
            icon=ft.icons.DARK_MODE,
            selected_icon=ft.icons.LIGHT_MODE,
            on_click=self.change_theme
        )

    def change_theme(self, event: ControlEvent):
        self.page.theme_mode = THEME_MODE[self.page.theme_mode]
        event.control.selected = not event.control.selected
        event.control.update()
        self.page.update()
