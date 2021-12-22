from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp

from uix.baseclass.bill_screen import BillScreen
from uix.baseclass.edit_bill import EditBillScreen
from uix.baseclass.edit_member_screen import MemberScreen
from uix.baseclass.offline_room import OfflineRoom
from uix.baseclass.settings_screen import SettingsScreen


class OfflineRoomApp(MDApp):
    def __init__(self, **kwargs):
        super(OfflineRoomApp, self).__init__(**kwargs)
        self.previous_screen = "room"
        self.sm = ScreenManager()

    def build(self):
        self.sm.add_widget(OfflineRoom())
        self.sm.add_widget(SettingsScreen())
        self.sm.add_widget(MemberScreen())
        self.sm.add_widget(BillScreen())
        self.sm.add_widget(EditBillScreen())

        return self.sm

    def set_screen(self, screen_name):
        self.root.current = screen_name


if __name__ == '__main__':
    OfflineRoomApp().run()
