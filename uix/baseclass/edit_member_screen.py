import os

from kivy.lang import Builder

from kivymd.uix.screen import MDScreen


with open(os.path.join(os.getcwd(), "uix", "kv", "edit_member_screen.kv"), encoding="utf-8") as KV:
    Builder.load_string(KV.read())


class MemberScreen(MDScreen):
    def __init__(self, **kwargs):
        self.__room_controller = kwargs['room_controller']
        del kwargs['room_controller']
        self.current_state = kwargs['current_state']
        del kwargs['current_state']
        super().__init__(**kwargs)

    def save_member(self):
        """Кнопка сохранения редактора участника
        Вернуться на главный экран"""
        name = self.ids.name_field.text
        if name == '':
            return
        if self.current_state['member'] is None:
            self.__room_controller.add_member(name=name, room_name=self.current_state['room_name'])
            self.__room_controller.reset_winners_in_the_room(room_name=self.current_state['room_name'])
        elif self.current_state['member'].get_name() != name:
            self.current_state['member'].set_name(name)
            self.__room_controller.reset_winners_in_the_room(room_name=self.current_state['room_name'])
        self.ids.name_field.text = ''
        self.manager.current = "room"
        self.current_state['member'] = None

    def on_enter(self, *args):
        if self.current_state['member'] is not None:
            self.ids.name_field.text = self.current_state['member'].get_name()
        else:
            self.ids.name_field.text = ''
