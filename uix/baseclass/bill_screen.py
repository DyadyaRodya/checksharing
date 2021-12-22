import os

from kivy.lang import Builder
from kivymd.uix.list import TwoLineListItem

from kivymd.uix.screen import MDScreen

with open(os.path.join(os.getcwd(), "uix", "kv", "bill_screen.kv"), encoding="utf-8") as KV:
    Builder.load_string(KV.read())


class BillScreen(MDScreen):
    def on_enter(self, *args):
        """Инициализация экрана
        Выполняется заполнение списка чеков"""
        status = "description"
        bills_num = 10
        for i in range(bills_num):
            list_item = TwoLineListItem(text=f"Bill {i}", secondary_text=f"{status}")
            list_item.bind(on_release=self.on_release_list_item)
            self.ids.bill_container.add_widget(list_item)

    def on_release_list_item(self, instance):
        """Обработчик нажатия на чек из списка
        Переход на экран редактирования, изменение чека"""
        print("Click!")
        # self.manager.current = "edit_bill"
