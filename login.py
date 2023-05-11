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
from helpclasses import WelcomeUserScreen, EnterUserUsername, StoreUserClass, MainScreen

sm = ScreenManager()
sm.add_widget(WelcomeUserScreen(name='welcomescreen'))
sm.add_widget(EnterUserUsername(name='usernamescreen'))
sm.add_widget(StoreUserClass(name='storeuserclass'))
sm.add_widget(MainScreen(name='main_screen'))


class LoginAppKivy(MDApp):
    def build(self):
        self.strng = Builder.load_string(helpingstring)
        self.theme_cls.primary_palette = "DeepOrange"
        return self.strng

    def save_user_name(self):
        self.store.put('UserName', name=self.username)
        self.change_username_dynamically_on_screen()

    def change_username_dynamically_on_screen(self):
        user_name = self.store.get('UserName')['name']
        self.strng.get_screen('mainscreen').ids.profile_name.text = f"Welcome {user_name}"

    def on_start(self):
        self.store = JsonStore("user_name.json")
        try:
            if self.store.get('UserName')['name'] != "":
                self.change_username_dynamically_on_screen()
                self.strng.get_screen('mainscreen').manager.current = 'mainscreen'

        except:
            self.strng.get_screen('welcomescreen').manager.current = 'welcomescreen'

    def close_username_dialogue(self, obj):
        self.dialog.dismiss()

    def check_for_valid_username(self):
        self.username = self.strng.get_screen('usernamescreen').ids.username_text_fied.text
        username_is_correct = True
        try:
            int(self.username)
        except:
            username_is_correct = False

        if username_is_correct or self.username.split() == []:
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialogue)
            self.dialog = MDDialog(title='Try another username',
                                   text="Retype username using letters and numbers(except "
                                        "first position)",
                                   size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()

        else:
            self.strng.get_screen('usernamescreen').ids.disabled_button.disabled = False

    def turn_on_button(self):
        self.strng.get_screen('storeuserclass').ids.second_disabled.disabled = False

    def turn_off_finalize_button(self):
        self.strng.get_screen('storeuserclass').ids.name_picker.disabled = True

    def turn_off_add_user_button(self):
        self.strng.get_screen('usernamescreen').ids.add_user_button.disabled = True

    def turn_off_go_back(self):
        self.strng.get_screen('storeuserclass').ids.back_button.disabled = True


if __name__ == "__main__":
    LoginAppKivy().run()
    GraphCreationClass().run()
    MainApp().run()
