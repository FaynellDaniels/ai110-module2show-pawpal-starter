"""Demo script: builds an owner with pets and tasks, then prints today's schedule."""

from datetime import time

from pawpal_system import Owner, Pet, Scheduler, Task


def main():
    # Create an owner and two pets
    owner = Owner("Jordan")
    buddy = Pet("Buddy", species="Dog")
    whiskers = Pet("Whiskers", species="Cat")
    owner.add_pet(buddy)
    owner.add_pet(whiskers)

    # Add tasks deliberately out of time order
    whiskers.add_task(Task("Play session", due_time=time(18, 30), duration=20, priority=1))
    buddy.add_task(Task("Give medication", due_time=time(12, 0), duration=5, priority=2))
    whiskers.add_task(Task("Breakfast", due_time=time(8, 0), duration=10, priority=3, frequency="daily"))
    buddy.add_task(Task("Morning walk", due_time=time(7, 30), duration=30, priority=3, frequency="daily"))

    # Mark one task done so we can try filtering
    buddy.tasks[1].mark_complete()

    # Pair each task with its pet's name, then sort by time of day
    todays_tasks = [(pet.name, task) for pet in owner.pets for task in pet.tasks]
    todays_tasks.sort(key=lambda pair: pair[1].due_time)

    print("=" * 46)
    print(f"  Today's Schedule - {owner.name}")
    print("=" * 46)
    print(f"  {'TIME':<9} {'TASK':<17} {'PET':<10} {'LENGTH':>6}")
    print("-" * 46)
    for pet_name, task in todays_tasks:
        time_text = task.due_time.strftime("%I:%M %p").lstrip("0")
        print(f"  {time_text:>8}  {task.description:<17} {pet_name:<10} {task.duration:>3} min")
    print("-" * 46)
    total_minutes = sum(task.duration for _, task in todays_tasks)
    print(f"  {len(todays_tasks)} tasks, {total_minutes} min total")

    # Sorting and filtering with the Scheduler
    scheduler = Scheduler(owner)

    print("\nTasks as added (out of order):")
    for task in owner.get_all_tasks():
        print(f"  {task.due_time:%H:%M}  {task.description}")

    print("\nSorted by time:")
    for task in scheduler.sort_by_time():
        print(f"  {task.due_time:%H:%M}  {task.description}")

    print("\nPending tasks only:")
    for task in scheduler.filter_tasks(completed=False):
        print(f"  {task.description}")

    print("\nBuddy's tasks only:")
    for task in scheduler.filter_tasks(pet_name="Buddy"):
        print(f"  {task.description}")

    # Conflict detection: two tasks at the same time (different pets, then same pet)
    print("\nChecking for conflicts:")
    buddy.add_task(Task("Grooming", due_time=time(8, 0), duration=30, priority=1))
    whiskers.add_task(Task("Brush fur", due_time=time(18, 30), duration=10, priority=1))
    for warning in scheduler.find_conflicts():
        print(f"  {warning}")

    # Recurring tasks: completing a daily/weekly task creates the next one
    print("\nCompleting Breakfast (daily):")
    breakfast = whiskers.tasks[1]
    next_breakfast = scheduler.mark_task_complete(whiskers, breakfast)
    print(f"  Next Breakfast is due {next_breakfast.due_date}")
    print(f"  Whiskers now has {len(whiskers.tasks)} tasks")


if __name__ == "__main__":
    main()
