import os

from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineListItem, IconLeftWidget, IconRightWidget, TwoLineIconListItem, \
    TwoLineAvatarIconListItem

from kivymd.uix.screen import MDScreen

from controllers.controller import RoomController

with open(os.path.join(os.getcwd(), "uix", "kv", "offline_room.kv"), encoding="utf-8") as KV:
    Builder.load_string(KV.read())


class OfflineRoom(MDScreen):
    dialog = None
    __room_controller : RoomController

    def __init__(self, **kwargs):
        self.__room_controller = kwargs['room_controller']
        del kwargs['room_controller']
        self.current_state = kwargs['current_state']
        del kwargs['current_state']
        super().__init__(**kwargs)

    def draw_members_and_summ(self):
        cur_room = self.__room_controller.get_room_by_name(name="local")
        self.ids.summ.text = f"{float(cur_room.get_total_summ())}"
        mem_list = cur_room.get_mem_list()
        members_num = mem_list.get_member_num()
        self.ids.member_container.clear_widgets()
        for i in range(members_num):
            cur_member = mem_list.get_member(i)
            if cur_member.get_status() == []:
                status = ""
            elif cur_member.IsPayed():
                status = "Оплатил"
            else:
                status = f"К оплате: {cur_member.get_status()[0]}"
            list_item = TwoLineAvatarIconListItem(text=f'{i+1}. {cur_member.get_name()}', secondary_text=status)
            list_item.bind(on_release=self.on_release_list_item(i))

            right_widget = IconRightWidget(icon='delete-circle-outline')
            right_widget.bind(on_release=self.on_release_delete_widget(i))

            list_item.add_widget(right_widget)
            self.ids.member_container.add_widget(list_item)

    def on_enter(self, *args):
        """Инициализация экрана
        Заполнение списка участников"""
        self.current_state['member'] = None
        self.current_state['bill'] = None
        self.draw_members_and_summ()

    def on_tap_button_start(self):
        """Обработчик кнопки розыгрыша
        Появляется всплывающее окно с именами плательщиков
        Меняется статус участников в списке"""
        res = self.__room_controller.set_winners_in_the_room(room_name=self.current_state['room_name'])
        if res is not None:
            self.pop_up1()
        else:
            self.pop_up2()
        self.draw_members_and_summ()

    def pop_up1(self):
        '''Displays a pop_up'''
        if not self.dialog:
            winners_list_text = ''
            cur_room = self.__room_controller.get_room_by_name(name="local")
            mem_list = cur_room.get_mem_list()
            members_num = mem_list.get_member_num()
            for winner in self.__room_controller.get_winners_in_the_room(room_name=self.current_state['room_name']):
                for i in range(members_num):
                    if mem_list.get_member(i) == winner:
                        winners_list_text += f'{i+1}. '
                        break
                winners_list_text += winner.get_name()
                winners_list_text += ', '
            if winners_list_text:
                winners_list_text = winners_list_text[:-2]
            self.dialog = MDDialog(
                size_hint=(.45, None),
                auto_dismiss=True,
                title="В этот раз заплатят:",
                text=winners_list_text,
                on_dismiss=self.dismiss_dialog
            )
            self.dialog.open()

    def pop_up2(self):
        '''Displays a pop_up'''
        if not self.dialog:
            self.dialog = MDDialog(
                size_hint=(.45, None),
                auto_dismiss=True,
                title="Нельзя провести розыгрыш:",
                text='Измените настройки или добавьте участников!',
                on_dismiss=self.dismiss_dialog
            )
            self.dialog.open()

    def dismiss_dialog(self, instance):
        self.dialog = None

    def on_release_list_item(self, member_num):
        def on_edit_member(instance):
            """Обработчик нажатия на участника из списка
            Переход на экран редактирования, изменение участника"""
            cur_room = self.__room_controller.get_room_by_name(name="local")
            mem_list = cur_room.get_mem_list()
            self.current_state['member'] = mem_list.get_member(member_num)
            self.manager.current = "edit_member"  # переход на экран редактирования, но нужна связь с изменяемым участником
        return on_edit_member

    def on_release_delete_widget(self, member_num):
        """Обработчик нажатия на иконку удаления участника из списка
        Удалить участника из списка"""
        def on_delete_member(instance):
            """Обработчик нажатия на участника из списка
            Переход на экран редактирования, изменение участника"""
            cur_room = self.__room_controller.get_room_by_name(name="local")
            mem_list = cur_room.get_mem_list()
            member = mem_list.get_member(member_num)
            self.__room_controller.del_member(room_name=self.current_state['room_name'], global_id=member.get_global_id())
            self.__room_controller.reset_winners_in_the_room(room_name=self.current_state['room_name'])
            self.draw_members_and_summ()
        return on_delete_member
