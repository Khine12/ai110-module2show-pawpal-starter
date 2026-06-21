"""Basic tests for PawPal+ core behaviors."""

from pawpal_system import Pet, Task


def test_mark_complete_changes_status():
    """Calling mark_complete() should set completed to True."""
    task = Task("Walk", "08:00", 30, "high")
    assert task.completed is False     # starts incomplete
    task.mark_complete()
    assert task.completed is True      # now complete


def test_add_task_increases_count():
    """Adding a task to a Pet should increase its task count by 1."""
    pet = Pet(name="Biscuit", species="Dog")
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task("Feeding", "09:00", 10, "high"))
    assert len(pet.get_tasks()) == 1