"""Demo script: builds an owner with pets and tasks, then prints today's schedule."""

from datetime import time

from pawpal_system import Owner, Pet, Task


def main():
    # Create an owner and two pets
    owner = Owner("Jordan")
    buddy = Pet("Buddy", species="Dog")
    whiskers = Pet("Whiskers", species="Cat")
    owner.add_pet(buddy)
    owner.add_pet(whiskers)

    # Add tasks with different times
    buddy.add_task(Task("Morning walk", due_time=time(7, 30), duration=30, priority=3, frequency="daily"))
    whiskers.add_task(Task("Breakfast", due_time=time(8, 0), duration=10, priority=3, frequency="daily"))
    buddy.add_task(Task("Give medication", due_time=time(12, 0), duration=5, priority=2))
    whiskers.add_task(Task("Play session", due_time=time(18, 30), duration=20, priority=1))

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


if __name__ == "__main__":
    main()
