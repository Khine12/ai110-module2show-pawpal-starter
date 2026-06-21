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
    """The 'brain': retrieves and organizes tasks across all pets."""

    def __init__(self, owner):
        self.owner = owner

    def sort_tasks(self):
        """Return all of the owner's tasks sorted by start time."""
        tasks = self.owner.get_all_tasks()
        return sorted(tasks, key=lambda t: t.time)

    # --- Implemented in Phase 4 (algorithmic layer) ---
    def generate_plan(self, available_minutes):
        """Build a daily plan within the time budget (Phase 4)."""
        pass

    def detect_conflicts(self):
        """Find tasks whose time slots overlap (Phase 4)."""
        pass

    def mark_task_complete(self, task):
        """Mark a task complete and handle recurrence (Phase 4)."""
        pass