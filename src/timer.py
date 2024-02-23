import flet as ft
import pywintypes
import win32api
import win32con
import win32security
from flet_core import UserControl, MainAxisAlignment, CrossAxisAlignment, ControlEvent, \
    TextAlign, InputFilter, TextStyle
from screen_brightness_control import set_brightness


class Timer(UserControl):
    hours = None
    minutes = None

    def build(self):
        label_style = TextStyle(size=13)
        self.hours = ft.TextField(
            label="hours",
            value="",
            label_style=label_style,
            text_align=TextAlign.CENTER,
            width=77,
            input_filter=InputFilter("^[0-9]{0,2}"),
        )
        self.minutes = ft.TextField(
            label="minutes",
            value="",
            label_style=label_style,
            text_align=TextAlign.CENTER,
            width=77,
            input_filter=InputFilter("^[0-9]{0,2}"),

        )
        separator = ft.Text(value=":", size=30)
        window = ft.Column(
            [
                ft.Row(
                    [self.hours, separator, self.minutes],
                    alignment=MainAxisAlignment.CENTER,
                    vertical_alignment=CrossAxisAlignment.CENTER
                ),
                ft.ElevatedButton("Shutdown", on_click=self.shutdown, width=190),
                ft.ElevatedButton("Reboot", on_click=self.reboot, width=190),
                ft.ElevatedButton("Canceling a timer", on_click=self.cancel, width=190)
            ],
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER
        )
        return window

    @staticmethod
    def init():
        shutdown_privilege = win32security.LookupPrivilegeValue(None, win32con.SE_SHUTDOWN_NAME)
        shutdown_token = win32security.OpenProcessToken(win32api.GetCurrentProcess(),
                                                        win32con.TOKEN_ADJUST_PRIVILEGES | win32con.TOKEN_QUERY)
        win32security.AdjustTokenPrivileges(shutdown_token, 0, [(shutdown_privilege, win32con.SE_PRIVILEGE_ENABLED)])

    def reboot(self, event: ControlEvent):
        second = (int(self.hours.value or 0) * 60 + int(self.minutes.value or 0)) * 60
        win32api.InitiateSystemShutdown(None, None, second, True, True)
        self.hours.value, self.minutes.value = "", ""
        self.update()

    def shutdown(self, event: ControlEvent):
        second = (int(self.hours.value or 0) * 60 + int(self.minutes.value or 0)) * 60
        win32api.InitiateSystemShutdown(None, None, second, True, False)
        self.hours.value, self.minutes.value = "", ""
        self.update()
        if self.page.client_storage.get("timer_data").get("dimming_brightness"):
            set_brightness(0)

    def cancel(self, event: ControlEvent):
        try:
            win32api.AbortSystemShutdown(None)
        except pywintypes.error:
            pass
        self.hours.value, self.minutes.value = "", ""
        self.update()
        set_brightness(100)
