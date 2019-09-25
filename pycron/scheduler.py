import collections
import datetime
import subprocess
import threading
import time
from queue import PriorityQueue

from croniter import croniter
from pytz import timezone

from .rules import CronRule, RuleParser

NextExecution = collections.namedtuple('NextExecution', 'timestamp cron_rule')
tz = timezone(time.tzname[0])


def tz_now():
    return tz.localize(datetime.datetime.now())


def timestamp_to_dt(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, tz=tz)


def get_time_to_sleep(execute_time):
    sleep_seconds = execute_time - tz_now().timestamp()
    return sleep_seconds if sleep_seconds > 0 else 0


class Scheduler(threading.Thread):
    def __init__(self, filename: str, reload_event: threading.Event, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.filename = filename
        self.reload_event = reload_event

        self.cron_rules = []
        self.queue = PriorityQueue()
        self.restart = threading.Event()

    def run(self):
        print("Scheduler start")
        self.load_data()

        while not self.restart.is_set() and not self.queue.empty():
            if self.reload_event.is_set():
                self.load_data()

            entry = self.queue.get()[1]
            print("First entry in queue is", entry)
            sleep_seconds = get_time_to_sleep(entry.timestamp)
            print("Going to sleep {0} seconds until it is time".format(sleep_seconds))
            self.reload_event.wait(sleep_seconds)
            print("Finished sleeping...")
            if not self.reload_event.is_set():  # If there has been a change we don't want to execute the code
                self.execute(entry.cron_rule.command)
                next_rule_execution = self.get_next_execution(entry.cron_rule, timestamp_to_dt(entry.timestamp))
                self.add_to_queue(next_rule_execution)

    def load_data(self):
        print("Loading data from {0}".format(self.filename))
        self.cron_rules = self.read_file()
        self.build_queue()

        self.reload_event.clear()  # File has been loaded so we clear the Event for continuing monitoring it

    def read_file(self):
        parser = RuleParser(self.filename)
        return parser.parse()

    def build_queue(self) -> None:
        self.queue = PriorityQueue()

        start_dt = tz_now().replace(second=0, microsecond=0)

        for rule in self.cron_rules:
            cron_exec = self.get_next_execution(rule, start_dt)
            self.add_to_queue(cron_exec)

    def add_to_queue(self, next_execution: NextExecution) -> None:
        self.queue.put((next_execution.timestamp, next_execution))

    @staticmethod
    def get_next_execution(cron_rule: CronRule, start_dt: datetime.datetime) -> NextExecution:
        scheduler = croniter(cron_rule.schedule, start_dt)
        next_execution = scheduler.get_next()
        return NextExecution(next_execution, cron_rule)

    @staticmethod
    def execute(command: str):
        print("Execute: ", command)

        p = subprocess.Popen(
            command.split(" "),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True
        )
        return p.pid
