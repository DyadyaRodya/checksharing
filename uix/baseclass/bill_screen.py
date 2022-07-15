import os

from kivy.lang import Builder
from kivymd.uix.list import ThreeLineAvatarIconListItem, IconRightWidget

from kivymd.uix.screen import MDScreen

with open(os.path.join(os.getcwd(), "uix", "kv", "bill_screen.kv"), encoding="utf-8") as KV:
    Builder.load_string(KV.read())


class BillScreen(MDScreen):
    def __init__(self, **kwargs):
        self.__room_controller = kwargs['room_controller']
        del kwargs['room_controller']
        self.current_state = kwargs['current_state']
        del kwargs['current_state']
        super().__init__(**kwargs)

    def draw_bills(self):
        cur_room = self.__room_controller.get_room_by_name(name="local")
        bill_list = cur_room.get_bill_list()
        bills_num = bill_list.get_bill_count()
        self.ids.bill_container.clear_widgets()
        for i in range(bills_num):
            cur_bill = bill_list.get_bill(i)
            added_by = cur_bill.get_member()
            mem_list = cur_room.get_mem_list()
            members_num = mem_list.get_member_num()
            for j in range(members_num):
                if added_by == mem_list.get_member(j):
                    added_by = f"{j+1}. {added_by.get_name()}"
                    break
            owner = f"Добавлено: {added_by}"
            status = f"К оплате: {cur_bill.get_summ()}"
            list_item = ThreeLineAvatarIconListItem(text=cur_bill.get_name(), secondary_text=f"{owner}",
                                                    tertiary_text=f"{status}")
            list_item.bind(on_release=self.on_release_list_item(i))

            right_widget = IconRightWidget(icon='delete-circle-outline')
            right_widget.bind(on_release=self.on_release_delete_widget(i))

            list_item.add_widget(right_widget)
            self.ids.bill_container.add_widget(list_item)

    def on_enter(self, *args):
        """Инициализация экрана
        Выполняется заполнение списка чеков"""
        self.current_state['member'] = None
        self.current_state['bill'] = None
        self.draw_bills()

    def on_release_list_item(self, bill_num):
        def on_edit_member(instance):
            """Обработчик нажатия на участника из списка
            Переход на экран редактирования, изменение участника"""
            cur_room = self.__room_controller.get_room_by_name(name="local")
            bill_list = cur_room.get_bill_list()
            self.current_state['bill'] = bill_list.get_bill(bill_num)
            self.manager.current = "edit_bill"  # переход на экран редактирования, но нужна связь с изменяемым участником
        return on_edit_member

    def on_release_delete_widget(self, bill_num):
        """Обработчик нажатия на иконку удаления участника из списка
        Удалить участника из списка"""
        def on_delete_member(instance):
            """Обработчик нажатия на участника из списка
            Переход на экран редактирования, изменение участника"""
            cur_room = self.__room_controller.get_room_by_name(name="local")
            bill_list = cur_room.get_bill_list()
            cur_bill = bill_list.get_bill(bill_num)
            self.__room_controller.del_bill_from_room(room_name=self.current_state['room_name'], bill_id=cur_bill.get_id())
            self.__room_controller.reset_winners_in_the_room(room_name=self.current_state['room_name'])
            self.draw_bills()
        return on_delete_member
