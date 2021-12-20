import os

from kivy.lang import Builder
from kivymd.uix.list import TwoLineListItem

from kivymd.uix.screen import MDScreen


with open(os.path.join(os.getcwd(), "uix", "kv", "offline_room.kv"), encoding="utf-8") as KV:
    Builder.load_string(KV.read())


class OfflineRoom(MDScreen):
    def on_enter(self, *args):
        status = "status"
        members_num = 10
        for i in range(members_num):
            self.ids.member_container.add_widget(
                TwoLineListItem(text=f"Name {i}", secondary_text=f"{status}")
            )

    def on_press_add_member(self):
        pass
