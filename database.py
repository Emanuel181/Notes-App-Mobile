import sqlite3

class NotesDatabase:
    def __init__(self):
        self.con = sqlite3.connect('notes.db')
        self.cursor = self.con.cursor()
        self.create_table()

    def mark_task_as_incompleted(self, taskid):
        self.cursor.execute("UPDATE tasks SET completed=0 WHERE id=?", (taskid,))
        self.con.commit()

        text_of_task = self.cursor.execute("SELECT task FROM tasks WHERE id=?", (taskid,)).fetchall()
        return text_of_task[0][0]

    def delete_task(self, taskid):
        self.cursor.execute("DELETE FROM tasks WHERE id=?", (taskid,))
        self.con.commit()

    def create_table(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS tasks(id integer PRIMARY KEY AUTOINCREMENT, task varcahr(75) NOT NULL, due_date varchar(75), completed BOOLEAN NOT NULL CHECK (completed IN (0, 1)))")

    def create_task(self, task, due_date=None):
        self.cursor.execute("INSERT INTO tasks(task, due_date, completed) VALUES(?, ?, ?)", (task, due_date, 0))
        self.con.commit()

        created_task = self.cursor.execute("SELECT id, task, due_date FROM tasks WHERE task = ? and completed = 0",
                                           (task,)).fetchall()
        return created_task[-1]

    def get_tasks(self):
        completed_tasks = self.cursor.execute("SELECT id, task, due_date FROM tasks WHERE completed = 1").fetchall()
        incompleted_tasks = self.cursor.execute("SELECT id, task, due_date FROM tasks WHERE completed = 0").fetchall()

        return completed_tasks, incompleted_tasks

    def mark_task_as_completed(self, taskid):
        self.cursor.execute("UPDATE tasks SET completed=1 WHERE id=?", (taskid,))
        self.con.commit()


    def close_db_connection(self):
        self.con.close()
