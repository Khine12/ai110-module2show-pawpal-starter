"""PawPal+ logic layer: core classes for pet care scheduling."""

from dataclasses import dataclass, field
from datetime import date


# Priority ranking for sorting (lower number = higher priority)
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


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
        pass


@dataclass
class Pet:
    """A pet owned by an Owner, holding its own list of tasks."""
    name: str
    species: str
    tasks: list = field(default_factory=list)

    def add_task(self, task):
        """Add a task to this pet's task list."""
        pass

    def get_tasks(self):
        """Return all tasks for this pet."""
        pass


class Owner:
    """A pet owner who manages multiple pets and a daily time budget."""

    def __init__(self, name, available_minutes):
        self.name = name
        self.available_minutes = available_minutes
        self.pets = []

    def add_pet(self, pet):
        """Add a pet to this owner."""
        pass

    def get_all_tasks(self):
        """Return every task across all of this owner's pets."""
        pass


class Scheduler:
    """The 'brain': sorts tasks, builds the daily plan, detects conflicts."""

    def __init__(self, owner):
        self.owner = owner

    def sort_tasks(self):
        """Return tasks sorted by priority, then time."""
        pass

    def generate_plan(self, available_minutes):
        """Build a daily plan within the time budget; return plan + skipped reasons."""
        pass

    def detect_conflicts(self):
        """Find tasks whose time slots overlap."""
        pass

    def mark_task_complete(self, task):
        """Mark a task complete and spawn the next occurrence if recurring."""
        pass