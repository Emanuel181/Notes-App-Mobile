import os
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.storage.jsonstore import JsonStore
from main import MainApp
from main import GraphCreationClass
from helpstring import helpingstring
from helpclasses import WelcomeScreen, EnterUsername, StoreUserClass, MainScreen


sm = ScreenManager()
sm.add_widget(WelcomeScreen(name='welcomescreen'))
sm.add_widget(EnterUsername(name='usernamescreen'))
sm.add_widget(StoreUserClass(name='storeuserclass'))
sm.add_widget(MainScreen(name='main_screen'))


class LoginAppKivy(MDApp):
    def build(self):
        self.strng = Builder.load_string(helpingstring)
        self.theme_cls.primary_palette = "DeepOrange"
        return self.strng

    def close_username_dialogue(self, obj):
        self.dialog.dismiss()

    def show_date_picker(self):
        pass

    def save_user_name(self):
        self.store.put('UserInfo', name=self.username)
        self.change_username_dynamically_on_screen()

    def change_username_dynamically_on_screen(self):
        self.strng.get_screen('mainscreen').ids.profile_name.text = f"Welcome {self.store.get('UserInfo')['name']}"

    def on_start(self):
        self.store = JsonStore("user_name.json")
        try:
            if self.store.get('UserInfo')['name'] != "":
                self.change_username_dynamically_on_screen()
                self.strng.get_screen('mainscreen').manager.current = 'mainscreen'

        except KeyError:
            self.strng.get_screen('welcomescreen').manager.current = 'welcomescreen'

    def check_for_valid_username(self):
        self.username = self.strng.get_screen('usernamescreen').ids.username_text_fied.text
        username_is_correct = True
        try:
            int(self.username)
        except:
            username_is_correct = False
        if username_is_correct or self.username.split() == []:
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialogue)
            self.dialog = MDDialog(title='Invalid Username', text="Retype username using letters and numbers(except "
                                                                  "first position)",
                                   size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()

        else:
            self.strng.get_screen('usernamescreen').ids.disabled_button.disabled = False

    def turn_off_button(self):
        self.strng.get_screen('storeuserclass').ids.second_disabled.disabled = False


if __name__ == "__main__":
    LoginAppKivy().run()
    GraphCreationClass().run()
    MainApp().run()
