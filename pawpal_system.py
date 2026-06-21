"""PawPal+ logic layer: core classes for pet care scheduling."""

from dataclasses import dataclass, field
from datetime import date, timedelta


# Priority ranking for sorting (lower number = higher priority)
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def _to_minutes(hhmm):
    """Convert an 'HH:MM' string into minutes since midnight."""
    hours, minutes = hhmm.split(":")
    return int(hours) * 60 + int(minutes)


@dataclass
class Task:
    """A single pet care activity (walk, feeding, meds, etc.)."""
    description: str
    time: str                 # "HH:MM" start time
    duration: int             # minutes
    priority: str             # "high" | "medium" | "low"
    frequency: str = "once"   # "once" | "daily" | "weekly"
    completed: bool = False
    due_date: date = field(default_factory=date.today)

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True


@dataclass
class Pet:
    """A pet that holds its own list of care tasks."""
    name: str
    species: str
    tasks: list = field(default_factory=list)

    def add_task(self, task):
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self):
        """Return this pet's list of tasks."""
        return self.tasks


class Owner:
    """A pet owner who manages multiple pets and a daily time budget."""

    def __init__(self, name, available_minutes):
        self.name = name
        self.available_minutes = available_minutes
        self.pets = []

    def add_pet(self, pet):
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self):
        """Return every task across all of this owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    """The 'brain': sorts, filters, plans, detects conflicts, handles recurrence."""

    def __init__(self, owner):
        self.owner = owner

    def sort_tasks(self):
        """Return all of the owner's tasks sorted by start time."""
        return sorted(self.owner.get_all_tasks(), key=lambda t: t.time)

    def filter_tasks(self, pet_name=None, completed=None):
        """Return tasks filtered by pet name and/or completion status."""
        results = []
        for pet in self.owner.pets:
            if pet_name is not None and pet.name != pet_name:
                continue
            for task in pet.get_tasks():
                if completed is not None and task.completed != completed:
                    continue
                results.append(task)
        return results

    def detect_conflicts(self):
        """Return warning strings for tasks whose time slots overlap."""
        tasks = self.sort_tasks()
        warnings = []
        for i in range(len(tasks)):
            for j in range(i + 1, len(tasks)):
                a, b = tasks[i], tasks[j]
                a_start, b_start = _to_minutes(a.time), _to_minutes(b.time)
                a_end, b_end = a_start + a.duration, b_start + b.duration
                if a_start < b_end and b_start < a_end:
                    warnings.append(
                        f"Conflict: '{a.description}' ({a.time}) overlaps "
                        f"'{b.description}' ({b.time})"
                    )
        return warnings

    def mark_task_complete(self, task):
        """Mark a task complete; if it recurs, add its next occurrence."""
        task.mark_complete()
        if task.frequency in ("daily", "weekly"):
            self._create_next_occurrence(task)

    def _create_next_occurrence(self, task):
        """Add the next instance of a recurring task to its pet."""
        days = 1 if task.frequency == "daily" else 7
        next_task = Task(
            description=task.description,
            time=task.time,
            duration=task.duration,
            priority=task.priority,
            frequency=task.frequency,
            completed=False,
            due_date=task.due_date + timedelta(days=days),
        )
        for pet in self.owner.pets:
            if any(t is task for t in pet.get_tasks()):
                pet.add_task(next_task)
                break

    def generate_plan(self, available_minutes=None):
        """Build a daily plan within the time budget, highest priority first.

        Returns (planned, skipped); each skipped item includes a reason.
        """
        if available_minutes is None:
            available_minutes = self.owner.available_minutes
        tasks = [t for t in self.owner.get_all_tasks() if not t.completed]
        tasks.sort(key=lambda t: (PRIORITY_ORDER[t.priority], t.time))

        planned, skipped, remaining = [], [], available_minutes
        for task in tasks:
            if task.duration <= remaining:
                planned.append(task)
                remaining -= task.duration
            else:
                skipped.append((task, f"needs {task.duration} min, only {remaining} left"))
        return planned, skipped