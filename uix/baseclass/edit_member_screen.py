import os

from kivy.lang import Builder

from kivymd.uix.screen import MDScreen


with open(os.path.join(os.getcwd(), "uix", "kv", "edit_member_screen.kv"), encoding="utf-8") as KV:
    Builder.load_string(KV.read())


class MemberScreen(MDScreen):
    def save_member(self):
        """Кнопка сохранения редактора участника
        Вернуться на главный экран"""
        pass
