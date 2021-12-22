import os

from kivy.lang import Builder

from kivymd.uix.screen import MDScreen


with open(os.path.join(os.getcwd(), "uix", "kv", "settings_screen.kv"), encoding="utf-8") as KV:
    Builder.load_string(KV.read())


class SettingsScreen(MDScreen):
    def save_settings(self):
        """Обработчик кнопки сохранения настроек
        Переход на главный экран offline_room"""
        pass