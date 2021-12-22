import os

from kivy.lang import Builder
from kivymd.uix.list import TwoLineListItem

from kivymd.uix.screen import MDScreen

with open(os.path.join(os.getcwd(), "uix", "kv", "edit_bill.kv"), encoding="utf-8") as KV:
    Builder.load_string(KV.read())


class EditBillScreen(MDScreen):
    def save_bill(self):
        """Обработчик кнопки сохранения чека
        Переход на экран bill_screen"""
        pass
