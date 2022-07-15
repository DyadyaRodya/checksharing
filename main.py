from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp

from uix.baseclass.bill_screen import BillScreen
from uix.baseclass.edit_bill import EditBillScreen
from uix.baseclass.edit_member_screen import MemberScreen
from uix.baseclass.offline_room import OfflineRoom
from uix.baseclass.settings_screen import SettingsScreen

from controllers.controller import RoomController


class OfflineRoomApp(MDApp):
    def __init__(self, **kwargs):
        self.__room_controller = kwargs['room_controller']
        del kwargs['room_controller']
        super(OfflineRoomApp, self).__init__(**kwargs)
        self.previous_screen = "room"
        self.sm = ScreenManager()
        self.current_state = {'member': None, 'bill': None, 'room_name': 'local'}

    def build(self):
        self.sm.add_widget(OfflineRoom(room_controller=self.__room_controller, current_state=self.current_state))
        self.sm.add_widget(SettingsScreen(room_controller=self.__room_controller, current_state=self.current_state))
        self.sm.add_widget(MemberScreen(room_controller=self.__room_controller, current_state=self.current_state))
        self.sm.add_widget(BillScreen(room_controller=self.__room_controller, current_state=self.current_state))
        self.sm.add_widget(EditBillScreen(room_controller=self.__room_controller, current_state=self.current_state))

        return self.sm

    def set_screen(self, screen_name):
        self.root.current = screen_name


if __name__ == '__main__':
    app = OfflineRoomApp(room_controller=RoomController())
    app.run()
