"""Demo script to verify PawPal+ logic in the terminal (CLI-first)."""

from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    owner = Owner(name="Khine", available_minutes=60)

    biscuit = Pet(name="Biscuit", species="dog")
    miso = Pet(name="Miso", species="cat")
    owner.add_pet(biscuit)
    owner.add_pet(miso)

    # Added out of order on purpose, to prove sorting works
    biscuit.add_task(Task("Evening walk", "18:00", 30, "high"))
    biscuit.add_task(Task("Morning walk", "08:00", 30, "high", frequency="daily"))
    miso.add_task(Task("Feeding", "08:15", 10, "high"))    # overlaps the morning walk
    miso.add_task(Task("Play time", "12:00", 20, "low"))

    scheduler = Scheduler(owner)

    print("=== Sorted by time ===")
    for t in scheduler.sort_tasks():
        print(f"  {t.time}  {t.description} ({t.duration}m) [{t.priority}]")

    print("\n=== Filter: only Biscuit's tasks ===")
    for t in scheduler.filter_tasks(pet_name="Biscuit"):
        print(f"  {t.time}  {t.description}")

    print("\n=== Conflict detection ===")
    conflicts = scheduler.detect_conflicts()
    for w in conflicts:
        print(f"  [!] {w}")
    if not conflicts:
        print("  No conflicts.")

    print("\n=== Daily plan (60 min budget, priority first) ===")
    planned, skipped = scheduler.generate_plan()
    for t in planned:
        print(f"  PLANNED: {t.time} {t.description} ({t.duration}m, {t.priority})")
    for t, reason in skipped:
        print(f"  SKIPPED: {t.description} -> {reason}")

    print("\n=== Recurring task ===")
    daily_task = next(t for t in owner.get_all_tasks() if t.frequency == "daily")
    print(f"  Biscuit has {len(biscuit.get_tasks())} tasks before completion.")
    scheduler.mark_task_complete(daily_task)
    print(f"  Marked '{daily_task.description}' (daily) complete -> next occurrence created.")
    print(f"  Biscuit now has {len(biscuit.get_tasks())} tasks.")


if __name__ == "__main__":
    main()