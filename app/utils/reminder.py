def set_reminder(task_title, reminder_time):
    import time
    import threading

    def notify():
        time.sleep(reminder_time)
        print(f"Reminder: It's time to complete your task: '{task_title}'!")

    reminder_thread = threading.Thread(target=notify)
    reminder_thread.start()