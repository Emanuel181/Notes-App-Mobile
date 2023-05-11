helpingstring = '''

ScreenManager:
    WelcomeUserScreen:
    EnterUserUsername:
    StoreUserClass:
    MainScreen:

<WelcomeUserScreen>:
    name: 'welcomescreen'
    MDLabel:
        text:'Primul tău pas spre o viață mai organizată!'
        font_style: 'H2'
        halign: 'center'
        pos_hint: {'center_y':0.65}

    MDFloatingActionButton:
        icon:'account-plus-outline'
        md_bg_color:app.theme_cls.primary_color
        user_font_size : '60sp'
        pos_hint: {'center_x':0.5,'center_y':0.32}
        on_press:
            root.manager.current = 'usernamescreen'
            root.manager.transition.direction = 'left'

    MDProgressBar:
        value:30
        pos_hint:{'center_y' : 0.02}

<EnterUserUsername>
    name:'usernamescreen'
    MDFloatingActionButton:
        icon: 'arrow-left'
        md_bg_color:app.theme_cls.primary_color
        pos_hint: {'center_x':0.1,'center_y':0.1}
        user_font_size : '45sp'
        on_press:
            root.manager.current = 'welcomescreen'
            root.manager.transition.direction = 'right'

    MDFloatingActionButton:
        id:disabled_button
        disabled: True
        icon: 'arrow-right'
        md_bg_color:app.theme_cls.primary_color
        pos_hint: {'center_x':0.9,'center_y':0.1}
        user_font_size : '45sp'
        on_press:
            root.manager.current = 'storeuserclass'
            root.manager.transition.direction = 'left'

    MDProgressBar:
        value:60
        pos_hint: {'center_y':0.02}

    MDLabel:
        text:'Username'
        font_style: 'H2'
        halign: 'center'
        pos_hint : {'center_y':0.85}

    MDTextField:
        id:username_text_fied
        pos_hint: {'center_x':0.5,'center_y':0.6}
        size_hint: (0.7,0.1)
        hint_text : 'Username'
        helper_text: 'Required'
        helper_text_mode: 'on_error'
        icon_right: 'account'
        icon_right_color: app.theme_cls.primary_color
        required : True

    MDFloatingActionButton:
        id: add_user_button
        icon:'account-plus'
        md_bg_color:app.theme_cls.primary_color
        pos_hint: {'center_x':0.5,'center_y':0.35}
        user_font_size: '50sp'
        on_press: 
            app.check_for_valid_username()
            app.turn_off_add_user_button()

<StoreUserClass>:
    name:'storeuserclass'
    MDLabel:
        text:'Ești la un pas de a folosi aplicația!'
        font_style: 'H2'
        halign: 'center'
        pos_hint: {'center_y':0.75} 

    MDRaisedButton:
        id:name_picker
        text:'Apasă pentru a finaliza'
        user_font_size : '70sp'
        pos_hint : {'center_x':0.5,'center_y':0.4}
        on_press: 
            app.turn_on_button()
            app.save_user_name()
            app.turn_off_finalize_button()
            app.turn_off_go_back()

    MDFloatingActionButton:
        id: back_button
        icon:'arrow-left'
        md_bg_color:app.theme_cls.primary_color
        pos_hint: {'center_x':0.1,'center_y':0.1}
        user_font_size: '45sp'
        on_press: root.manager.current = 'usernamescreen'

    MDFloatingActionButton:
        id: second_disabled
        disabled: True
        icon:'arrow-right'
        md_bg_color:app.theme_cls.primary_color
        pos_hint: {'center_x':0.9,'center_y':0.1}
        user_font_size: '45sp'
        on_press: root.manager.current = 'mainscreen'

<MainScreen>:
    name : 'mainscreen'
    MDLabel:
        id:profile_name
        text:'main screen'
        font_style : 'H2'
        halign : 'center'
        pos_hint : {'center_y':0.7}

    MDFloatingActionButton:
        id: second_disabled
        disabled: False
        icon:'arrow-right'
        md_bg_color:app.theme_cls.primary_color
        pos_hint: {'center_x':0.9,'center_y':0.1}
        user_font_size: '45sp'
        on_press: app.stop()
'''