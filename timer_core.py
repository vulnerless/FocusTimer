"""Core logic for FocusTimer: a Pomodoro timer and a simple task list."""

WORK = "work"
SHORT_BREAK = "short_break"
LONG_BREAK = "long_break"

MIN_MINUTES = 1
MAX_MINUTES = 60
MAX_TITLE_LENGTH = 100


class Timer:
    """Pomodoro timer. Time moves forward only when tick() is called."""

    def __init__(self, work_minutes=25, break_minutes=5,
                 long_break_minutes=15, rounds_before_long=4):
        self.work_minutes = work_minutes
        self.break_minutes = break_minutes
        self.long_break_minutes = long_break_minutes
        self.rounds_before_long = rounds_before_long
        self.reset()

    def reset(self):
        self.mode = WORK
        self.remaining = self.work_minutes * 60
        self.running = False
        self.completed = 0

    def start(self):
        self.running = True

    def pause(self):
        self.running = False

    def tick(self, seconds=1):
        if not isinstance(seconds, int) or seconds < 0:
            raise ValueError("Seconds must be a non-negative whole number")
        if not self.running:
            return
        self.remaining -= seconds
        if self.remaining <= 0:
            self._finish_phase()

    def _finish_phase(self):
        if self.mode == WORK:
            self.completed += 1
            if self.completed % self.rounds_before_long == 0:
                self.mode = LONG_BREAK
                self.remaining = self.long_break_minutes * 60
            else:
                self.mode = SHORT_BREAK
                self.remaining = self.break_minutes * 60
        else:
            self.mode = WORK
            self.remaining = self.work_minutes * 60

    def set_durations(self, work_minutes, break_minutes):
        for value in (work_minutes, break_minutes):
            if not isinstance(value, int) or isinstance(value, bool):
                raise ValueError("Durations must be whole numbers")
            if value < MIN_MINUTES or value > MAX_MINUTES:
                raise ValueError("Durations must be between 1 and 60 minutes")
        self.work_minutes = work_minutes
        self.break_minutes = break_minutes
        self.reset()

    def to_dict(self):
        return {
            "mode": self.mode,
            "remaining": self.remaining,
            "running": self.running,
            "completed": self.completed,
            "work_minutes": self.work_minutes,
            "break_minutes": self.break_minutes,
        }


class TaskList:
    """In-memory list of tasks."""

    def __init__(self):
        self.tasks = {}
        self.next_id = 1

    def add(self, title):
        title = (title or "").strip()
        if not title:
            raise ValueError("Title cannot be empty")
        if len(title) > MAX_TITLE_LENGTH:
            raise ValueError("Title is too long")
        task = {"id": self.next_id, "title": title, "done": False}
        self.tasks[self.next_id] = task
        self.next_id += 1
        return task

    def complete(self, task_id):
        if task_id not in self.tasks:
            raise KeyError(task_id)
        self.tasks[task_id]["done"] = True
        return self.tasks[task_id]

    def delete(self, task_id):
        if task_id not in self.tasks:
            raise KeyError(task_id)
        del self.tasks[task_id]

    def all(self):
        return list(self.tasks.values())
