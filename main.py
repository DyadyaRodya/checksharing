from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp

from uix.baseclass.offline_room import OfflineRoom
from uix.baseclass.settings_screen import SettingsScreen


class OfflineRoomApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(OfflineRoom())
        sm.add_widget(SettingsScreen())

        return sm

    def set_screen(self, screen_name):
        self.root.current = screen_name


if __name__ == '__main__':
    OfflineRoomApp().run()
