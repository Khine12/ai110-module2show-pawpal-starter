"""Test suite for PawPal+ core behaviors and scheduling logic."""

from datetime import timedelta
from pawpal_system import Owner, Pet, Task, Scheduler


def make_owner():
    """Helper: an owner with two pets for tests to use."""
    owner = Owner(name="Tester", available_minutes=60)
    owner.add_pet(Pet(name="Biscuit", species="dog"))
    owner.add_pet(Pet(name="Miso", species="cat"))
    return owner


# --- Core object behavior ---

def test_mark_complete_changes_status():
    """mark_complete() sets a task's completed flag to True."""
    task = Task("Walk", "08:00", 30, "high")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_count():
    """Adding a task to a Pet increases its task count by 1."""
    pet = Pet(name="Biscuit", species="dog")
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task("Feeding", "09:00", 10, "high"))
    assert len(pet.get_tasks()) == 1


# --- Scheduling logic ---

def test_sort_tasks_chronological():
    """sort_tasks() returns tasks in chronological order."""
    owner = make_owner()
    biscuit = owner.pets[0]
    biscuit.add_task(Task("Evening", "18:00", 30, "high"))
    biscuit.add_task(Task("Morning", "08:00", 30, "high"))
    biscuit.add_task(Task("Noon", "12:00", 20, "low"))
    scheduler = Scheduler(owner)
    times = [t.time for t in scheduler.sort_tasks()]
    assert times == ["08:00", "12:00", "18:00"]


def test_recurrence_creates_next_occurrence():
    """Completing a daily task adds a new occurrence for the next day."""
    owner = make_owner()
    biscuit = owner.pets[0]
    daily = Task("Morning walk", "08:00", 30, "high", frequency="daily")
    biscuit.add_task(daily)
    scheduler = Scheduler(owner)

    assert len(biscuit.get_tasks()) == 1
    scheduler.mark_task_complete(daily)
    assert len(biscuit.get_tasks()) == 2
    new_task = biscuit.get_tasks()[1]
    assert new_task.completed is False
    assert new_task.due_date == daily.due_date + timedelta(days=1)


def test_conflict_detection_flags_overlap():
    """detect_conflicts() flags two tasks whose times overlap."""
    owner = make_owner()
    biscuit = owner.pets[0]
    biscuit.add_task(Task("Walk", "08:00", 30, "high"))   # 08:00–08:30
    biscuit.add_task(Task("Feed", "08:15", 10, "high"))   # 08:15–08:25
    scheduler = Scheduler(owner)
    assert len(scheduler.detect_conflicts()) == 1


def test_no_conflict_when_times_dont_overlap():
    """detect_conflicts() returns nothing when tasks don't overlap."""
    owner = make_owner()
    biscuit = owner.pets[0]
    biscuit.add_task(Task("Walk", "08:00", 30, "high"))   # ends 08:30
    biscuit.add_task(Task("Feed", "09:00", 10, "high"))   # starts 09:00
    scheduler = Scheduler(owner)
    assert scheduler.detect_conflicts() == []


def test_empty_pet_has_no_tasks():
    """A pet with no tasks contributes nothing (edge case)."""
    owner = make_owner()
    scheduler = Scheduler(owner)
    assert scheduler.sort_tasks() == []
    assert scheduler.detect_conflicts() == []


def test_generate_plan_respects_budget():
    """generate_plan() skips tasks that exceed the remaining budget."""
    owner = make_owner()
    owner.available_minutes = 30
    biscuit = owner.pets[0]
    biscuit.add_task(Task("Walk", "08:00", 30, "high"))   # fits exactly
    biscuit.add_task(Task("Play", "09:00", 20, "low"))    # no budget left
    scheduler = Scheduler(owner)
    planned, skipped = scheduler.generate_plan()
    assert len(planned) == 1
    assert len(skipped) == 1