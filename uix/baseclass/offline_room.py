import os

from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineListItem, IconLeftWidget, IconRightWidget, TwoLineIconListItem, \
    TwoLineAvatarIconListItem

from kivymd.uix.screen import MDScreen

with open(os.path.join(os.getcwd(), "uix", "kv", "offline_room.kv"), encoding="utf-8") as KV:
    Builder.load_string(KV.read())


class OfflineRoom(MDScreen):
    dialog = None

    def on_enter(self, *args):
        """Инициализация экрана
        Заполнение списка участников"""
        status = "status"
        members_num = 10
        for i in range(members_num):
            list_item = TwoLineAvatarIconListItem(text=f"Name {i}", secondary_text=f"{status}")
            list_item.bind(on_release=self.on_release_list_item)

            right_widget = IconRightWidget(icon='delete-circle-outline')
            right_widget.bind(on_release=self.on_release_delete_widget)

            list_item.add_widget(right_widget)
            self.ids.member_container.add_widget(list_item)

    def on_tap_button_start(self):
        """Обработчик кнопки розыгрыша
        Появляется всплывающее окно с именами плательщиков
        Меняется статус участников в списке"""
        self.pop_up1()

    def pop_up1(self):
        '''Displays a pop_up'''
        if not self.dialog:
            self.dialog = MDDialog(
                size_hint=(.45, None),
                auto_dismiss=True,
                title="В этот раз заплатят:",
                text="Rodion",
                on_dismiss=self.dismiss_dialog
            )
            self.dialog.open()

    def dismiss_dialog(self, instance):
        self.dialog = None

    def on_release_list_item(self, instance):
        """Обработчик нажатия на участника из списка
        Переход на экран редактирования, изменение участника"""
        print("Click!")
        # self.manager.current = "edit_member" # переход на экран редактирования, но нужна связь с изменяемым участником

    def on_release_delete_widget(self, instance):
        """Обработчик нажатия на иконку удаления участника из списка
        Удалить участника из списка"""
        print("Delete!")
