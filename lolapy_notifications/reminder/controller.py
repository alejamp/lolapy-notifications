import threading
import time

import schedule


def run_in_background(interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


class Reminder():
    id: str
    seconds: int
    target: str
    created_at: int
    job: schedule.Job
    metadata: dict



class ReminderController:

    def __init__(self):
        self.jobs = {}
        self.stop_run_continuously = None
        

    def background_job():
        print('Hello from the background thread')


    def add_reminder(self, user_id: str, seconds: int, target: str, reminder_id: str, metadata: dict = {}):
        reminder = Reminder()
        reminder.id = reminder_id
        reminder.seconds = seconds
        reminder.target = target
        reminder.created_at = int(time.time())
        reminder.metadata = metadata
        reminder.job = schedule.every(seconds).seconds.do(self.run_reminder, reminder)
        if user_id not in self.jobs:
            self.jobs[user_id] = {}

        self.jobs[user_id][reminder_id] = reminder

    def remove_reminder(self, user_id: str, id: str):
        if user_id in self.jobs and id in self.jobs[user_id]:
            reminder = self.jobs[user_id][id]
            schedule.cancel_job(reminder.job)
            del self.jobs[user_id][id]

    def get_reminders(self, user_id: str):
        if user_id in self.jobs:
            return self.jobs[user_id]
        return {}

    def stop_reminders(self, user_id: str):
        if user_id in self.jobs:
            for id, reminder in self.jobs[user_id].items():
                schedule.cancel_job(reminder.job)
            del self.jobs[user_id]


    def run_reminder(self, reminder: Reminder):
        print("Running reminder..." + reminder.target)
    
    def start(self):
        # Start the background thread
        self.stop_run_continuously = run_in_background()

    def stop(self):
        # Stop the background thread
        self.stop_run_continuously.set()


if __name__ == '__main__':
    controller = ReminderController()
    controller.add_reminder('user1', 1, 'target1', 'id1')
    controller.add_reminder('user2', 2, 'target2', 'id2')
    controller.start()
    time.sleep(5)
    # controller.remove_reminder('user1', 'id1')
    controller.stop_reminders('user2')
    time.sleep(5)
    controller.stop()

