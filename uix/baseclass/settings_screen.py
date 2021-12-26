import os

from kivy.lang import Builder

from kivymd.uix.screen import MDScreen


with open(os.path.join(os.getcwd(), "uix", "kv", "settings_screen.kv"), encoding="utf-8") as KV:
    Builder.load_string(KV.read())


class SettingsScreen(MDScreen):
    def __init__(self, **kwargs):
        self.__room_controller = kwargs['room_controller']
        del kwargs['room_controller']
        self.current_state = kwargs['current_state']
        del kwargs['current_state']
        super().__init__(**kwargs)

    def on_enter(self, *args):
        self.ids.name_field.text = f"{self.__room_controller.get_room_info(self.current_state['room_name']).get_win_count()}"

    def save_settings(self):
        """Обработчик кнопки сохранения настроек
        Переход на главный экран offline_room"""
        try:
            win_count = int(self.ids.name_field.text)
            if win_count > 0:
                if win_count != self.__room_controller.get_room_info(self.current_state['room_name']).get_win_count():
                    self.__room_controller.edit_payment_settings(room_name=self.current_state['room_name'],
                                                                 win_count=win_count)
                    self.__room_controller.reset_winners_in_the_room(room_name=self.current_state['room_name'])
                self.ids.name_field.text = ''
                self.manager.current = "room"
            else:
                self.ids.name_field.text = f"{self.__room_controller.get_room_info(self.current_state['room_name']).get_win_count()}"
        except Exception as e:
            print(e)
            return

