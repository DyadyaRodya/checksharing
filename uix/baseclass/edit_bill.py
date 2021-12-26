import os

from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.boxlayout import MDBoxLayout

from kivymd.uix.screen import MDScreen

with open(os.path.join(os.getcwd(), "uix", "kv", "edit_bill.kv"), encoding="utf-8") as KV:
    Builder.load_string(KV.read())


class MenuHeader(MDBoxLayout):
    """An instance of the class that will be added to the menu header."""


class EditBillScreen(MDScreen):
    def __init__(self, **kwargs):
        self.__room_controller = kwargs['room_controller']
        del kwargs['room_controller']
        self.current_state = kwargs['current_state']
        del kwargs['current_state']
        super().__init__(**kwargs)
        self.menu = None

    def draw_menu(self):
        cur_room = self.__room_controller.get_room_by_name(name="local")
        mem_list = cur_room.get_mem_list()
        members_num = mem_list.get_member_num()
        menu_items = [
            {
                "text": 'Не выбрано',
                "viewclass": "OneLineListItem",
                "height": dp(56),
                "on_release": lambda x=(None, None): self.menu_callback(*x),
            },
        ]
        for i in range(members_num):
            menu_items.append({
                "text": f'{i+1}. {mem_list.get_member(i).get_name()}',
                "viewclass": "OneLineListItem",
                "height": dp(56),
                "on_release": lambda x=(i, mem_list.get_member(i)): self.menu_callback(*x),
            })
        self.menu = MDDropdownMenu(
            header_cls=MenuHeader(),
            caller=self.ids.mem_name_field,
            items=menu_items,
            width_mult=4,
        )
        self.menu.open()

    def menu_callback(self, i, member):
        self.current_state['member'] = member
        if member is not None:
            self.current_state['member'] = member
            self.ids.mem_name_field.text = f"{i+1}. {member.get_name()}"
        else:
            self.current_state['member'] = None
            self.ids.mem_name_field.text = 'Выбрать участника'
        self.menu.dismiss()
        self.menu = None

    def save_bill(self):
        """Обработчик кнопки сохранения чека
        Переход на экран bill_screen"""
        try:
            rest_name = self.ids.rest_name_field.text
            summ = float(self.ids.summ_field.text)
            member = self.current_state['member']
            if rest_name and member is not None and summ > 0:
                if self.current_state['bill'] is None:
                    self.__room_controller.add_bill_to_room(room_name=self.current_state['room_name'],
                                                            member_global_id=member.get_global_id(),
                                                            rest_name=rest_name,
                                                            summ=summ)
                    self.__room_controller.reset_winners_in_the_room(room_name=self.current_state['room_name'])
                elif self.current_state['bill'].get_name() != rest_name \
                        or self.current_state['bill'].get_summ() != summ \
                        or self.current_state['bill'].get_member() != member:
                    self.__room_controller.edit_bill_room(room_name=self.current_state['room_name'],
                                                          bill_id=self.current_state['bill'].get_id(),
                                                          member_global_id=member.get_global_id(),
                                                          rest_name=rest_name,
                                                          summ=summ)
                    self.__room_controller.reset_winners_in_the_room(room_name=self.current_state['room_name'])
                self.ids.rest_name_field.text = ''
                self.ids.summ_field.text = ''
                self.ids.mem_name_field.text = 'Выбрать участника'
                self.manager.current = "bill_screen"
                self.current_state['member'] = None
                self.current_state['bill'] = None
        except Exception as e:
            print(e)
            return

    def on_enter(self, *args):
        if self.current_state['bill'] is not None:
            self.ids.rest_name_field.text = self.current_state['bill'].get_name()
            self.ids.summ_field.text = f"{self.current_state['bill'].get_summ()}"
            self.ids.mem_name_field.text = self.current_state['bill'].get_member().get_name()
            self.current_state['member'] = self.current_state['bill'].get_member()
        else:
            self.ids.rest_name_field.text = ''
            self.ids.summ_field.text = '0.00'
            self.ids.mem_name_field.text = 'Выбрать участника'
