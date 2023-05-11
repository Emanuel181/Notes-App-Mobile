from pushbullet import Pushbullet
from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.boxlayout import MDBoxLayout
from datetime import datetime
from database import Database
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.app import App
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.pickers import MDDatePicker
import matplotlib.pyplot as plt

Database_notes = Database()


class TaskScreen(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.date_text.text = str(datetime.now().strftime('%A %d %B %Y'))

    def pick_date(self):
        date = MDDatePicker()
        date.bind(on_save=self.save)
        date.open()

    def save(self, instance, value, date_range):
        date = value.strftime('%A %d %B %Y')
        self.ids.date_text.text = str(date)


class ShowTasks(TwoLineAvatarIconListItem):
    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        self.pk = pk

    def mark_task(self, state, tasks_list):
        if state.active == True:
            tasks_list.text = '[s]' + tasks_list.text + '[/s]'
            Database_notes.mark_task_as_completed(tasks_list.pk)
        else:
            tasks_list.text = str(Database_notes.mark_task_as_incompleted(tasks_list.pk))

    def delete_task(self, tasks_list):
        self.parent.remove_widget(tasks_list)
        Database_notes.delete_task(tasks_list.pk)


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    ''' '''


values_xaxis = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
_, incompleted_tasks = Database_notes.get_tasks()

cM, cT, cW, cTh, cF, cSa, cSu = 0, 0, 0, 0, 0, 0, 0

for task in incompleted_tasks:
    if task[2].split()[0] == 'Monday':
        cM += 1
    elif task[2].split()[0] == 'Tuesday':
        cT += 1
    elif task[2].split()[0] == 'Wednesday':
        cW += 1
    elif task[2].split()[0] == 'Thursday':
        cTh += 1
    elif task[2].split()[0] == 'Friday':
        cF += 1
    elif task[2].split()[0] == 'Saturday':
        cSa += 1
    elif task[2].split()[0] == 'Sunday':
        cSu += 1
values_yaxis = [cM, cT, cW, cTh, cF, cSa, cSu]

fix, ax = plt.subplots()
ax.bar(values_xaxis, values_yaxis)
plt.ylabel('Number of tasks per day')


class GraphCreationClass(App):
    def build(self):
        box = BoxLayout()
        box.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        return box


class MainApp(MDApp):
    task_list_dialog = None

    def dark(self):
        self.theme_cls.theme_style = "Dark"

    def light(self):
        self.theme_cls.theme_style = "Light"

    def build(self):
        self.theme_cls.primary_palette = "DeepOrange"

    def show_task_dialog(self):
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(
                title="Create task",
                type="custom",
                content_cls=TaskScreen(),
            )

        self.task_list_dialog.open()

    def on_start(self):
        completed_tasks, incompleted_tasks = Database_notes.get_tasks()

        if incompleted_tasks:
            for task in incompleted_tasks:
                add_task = ShowTasks(pk=task[0], text=str(task[1]), secondary_text=task[2])
                self.root.ids.container.add_widget(add_task)

        if completed_tasks:
            for task in completed_tasks:
                add_task = ShowTasks(pk=task[0], text='[s]' + str(task[1]) + '[/s]', secondary_text=task[2])
                add_task.ids.check.active = True
                self.root.ids.container.add_widget(add_task)

    def close_dialog(self, *args):
        self.task_list_dialog.dismiss()

    def add_task(self, task_to_be_added, task_date):
        added_task = Database_notes.create_task(task_to_be_added.text, task_date)

        self.root.ids['container'].add_widget(
            ShowTasks(pk=added_task[0], text='[b]' + added_task[1] + '[/b]', secondary_text=added_task[2]))

        pb = Pushbullet('o.4fQxfQlYbZ1IyVfgPGhWcWf12rLbpsfG')

        device_to_connect = pb.devices[0]
        phone_number = '+40751974985'
        pb.push_sms(device_to_connect, phone_number,
                    f"Salut Emanuel, ai setat activitatea \"{task_to_be_added.text}\" pentru \"{task_date}\"."
                    f" Poti sa adaugi activitatea in aplicatia de calendar a telefonului dand click pe textul "
                    f"subliniat."
                    f" Sa ai o zi productiva!")


if __name__ == '__main__':
    GraphCreationClass().run()
    MainApp().run()
