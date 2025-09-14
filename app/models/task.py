class Task:
    def __init__(self, title, description, deadline, reminder_time=None):
        self.title = title
        self.description = description
        self.deadline = deadline
        self.reminder_time = reminder_time

    def set_title(self, title):
        self.title = title

    def get_title(self):
        return self.title

    def set_description(self, description):
        self.description = description

    def get_description(self):
        return self.description

    def set_deadline(self, deadline):
        self.deadline = deadline

    def get_deadline(self):
        return self.deadline

    def set_reminder_time(self, reminder_time):
        self.reminder_time = reminder_time

    def get_reminder_time(self):
        return self.reminder_time

    def __str__(self):
        return f"Task(title={self.title}, description={self.description}, deadline={self.deadline}, reminder_time={self.reminder_time})"