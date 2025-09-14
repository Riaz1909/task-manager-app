class TaskController:
    def __init__(self):
        self.tasks = []

    def add_task(self, title, description, deadline, reminder_time):
        task = {
            'title': title,
            'description': description,
            'deadline': deadline,
            'reminder_time': reminder_time
        }
        self.tasks.append(task)

    def remove_task(self, title):
        self.tasks = [task for task in self.tasks if task['title'] != title]

    def update_task(self, title, description=None, deadline=None, reminder_time=None):
        for task in self.tasks:
            if task['title'] == title:
                if description is not None:
                    task['description'] = description
                if deadline is not None:
                    task['deadline'] = deadline
                if reminder_time is not None:
                    task['reminder_time'] = reminder_time
                break

    def get_tasks(self):
        return self.tasks

    def get_task(self, title):
        for task in self.tasks:
            if task['title'] == title:
                return task
        return None