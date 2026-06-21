"""Demo script to verify PawPal+ logic in the terminal (CLI-first)."""

from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    # 1. Owner with 120 minutes available today
    owner = Owner(name="Khine", available_minutes=120)

    # 2. Two pets, added to the owner
    biscuit = Pet(name="Biscuit", species="Golden Retriever")
    miso = Pet(name="Miso", species="Cat")
    owner.add_pet(biscuit)
    owner.add_pet(miso)

    # 3. At least three tasks with different times
    biscuit.add_task(Task("Morning walk", "08:00", 30, "high"))
    biscuit.add_task(Task("Feeding", "09:00", 10, "high"))
    miso.add_task(Task("Litter change", "07:30", 10, "medium"))
    miso.add_task(Task("Play time", "18:00", 20, "low"))

    # 4. Build and print today's schedule (sorted by time)
    scheduler = Scheduler(owner)
    todays_tasks = scheduler.sort_tasks()

    print(f"Today's Schedule for {owner.name}:")
    print("-" * 40)
    for task in todays_tasks:
        status = "x" if task.completed else " "
        print(f"[{status}] {task.time}  {task.description:<15} "
              f"({task.duration} min) [{task.priority}]")


if __name__ == "__main__":
    main()