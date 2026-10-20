"""PawPal: a simple pet-care scheduling system.

How the pieces fit together:
    Owner     -> has many Pets
    Pet       -> has many Tasks
    Scheduler -> asks the Owner for all tasks, then sorts and plans them
"""

from dataclasses import dataclass, field, replace
from datetime import date, time, timedelta


@dataclass
class Task:
    """One pet-care activity, like a walk or a feeding."""

    description: str
    due_time: time | None = None  # when it should happen, e.g. time(8, 30)
    duration: int = 0             # minutes
    priority: int = 1             # higher number = more important
    frequency: str = "once"       # "once", "daily", "weekly", ...
    due_date: date | None = None  # which day it is due
    completed: bool = False

    def mark_complete(self):
        """Mark this task as done."""
        self.completed = True

    def next_occurrence(self) -> "Task | None":
        """Return a new copy of this task for its next occurrence.

        A "daily" task is due today + 1 day and a "weekly" task today + 7 days,
        calculated with timedelta. The copy starts out not completed. Tasks with
        any other frequency (like "once") don't repeat, so None is returned.
        """
        days_until_next = {"daily": 1, "weekly": 7}.get(self.frequency)
        if days_until_next is None:
            return None
        next_date = date.today() + timedelta(days=days_until_next)
        return replace(self, due_date=next_date, completed=False)


@dataclass
class Pet:
    """A pet and the list of tasks it needs."""

    name: str
    species: str = ""
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task: Task):
        """Remove a task from this pet."""
        self.tasks.remove(task)


@dataclass
class Owner:
    """A person who takes care of one or more pets."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return every task from every pet in one list."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


class Scheduler:
    """Builds a daily plan from all of an owner's tasks."""

    def __init__(self, owner: Owner):
        """Create a scheduler that plans tasks for the given owner."""
        self.owner = owner

    def get_pending_tasks(self) -> list[Task]:
        """Get all tasks (across all pets) that are not done yet."""
        return [task for task in self.owner.get_all_tasks() if not task.completed]

    def mark_task_complete(self, pet: Pet, task: Task) -> Task | None:
        """Mark a task done and, if it repeats, schedule its next occurrence.

        Args:
            pet: The pet that owns the task (the new task is added to this pet).
            task: The task that was just finished.

        Returns:
            The newly created task for daily/weekly tasks, otherwise None.
        """
        task.mark_complete()
        next_task = task.next_occurrence()
        if next_task is not None:
            pet.add_task(next_task)
        return next_task

    def find_conflicts(self) -> list[str]:
        """Find pending tasks that are scheduled at the same time.

        Lightweight check: tasks conflict if they share the same date and start
        time, whether they belong to the same pet or different pets. Completed
        tasks and tasks without a time are ignored. Overlapping durations are
        not checked.

        Returns:
            One warning message per conflicting time slot (an empty list if
            there are none). Nothing is raised, so the program never crashes.
        """
        slots: dict[tuple, list[str]] = {}
        for pet in self.owner.pets:
            for task in pet.tasks:
                if task.completed or task.due_time is None:
                    continue
                slots.setdefault((task.due_date, task.due_time), []).append(
                    f"{task.description} ({pet.name})"
                )

        warnings = []
        for (_, due_time), names in slots.items():
            if len(names) > 1:
                warnings.append(f"Warning: {due_time:%I:%M %p} conflict - " + " and ".join(names))
        return warnings

    def sort_by_time(self, tasks: list[Task] | None = None) -> list[Task]:
        """Sort tasks by time of day, earliest first.

        Args:
            tasks: The tasks to sort. If left out, all of the owner's tasks
                (across every pet) are used.

        Returns:
            A new sorted list. Tasks with no time are placed at the end.
        """
        if tasks is None:
            tasks = self.owner.get_all_tasks()
        # The lambda tells sorted() what to compare. time objects compare
        # correctly on their own; zero-padded "HH:MM" strings would too.
        return sorted(tasks, key=lambda task: task.due_time or time.max)

    def filter_tasks(self, completed: bool | None = None, pet_name: str | None = None) -> list[Task]:
        """Get tasks filtered by completion status and/or pet name.

        Args:
            completed: True for finished tasks, False for pending ones, or
                None (the default) for both.
            pet_name: Only include this pet's tasks, or None for every pet.

        Returns:
            The matching tasks. Both filters can be combined.
        """
        matches = []
        for pet in self.owner.pets:
            if pet_name is not None and pet.name != pet_name:
                continue
            for task in pet.tasks:
                if completed is None or task.completed == completed:
                    matches.append(task)
        return matches

    def prioritize_tasks(self) -> list[Task]:
        """Sort pending tasks by priority (highest first), then by earliest time."""
        return sorted(
            self.get_pending_tasks(),
            key=lambda task: (-task.priority, task.due_time or time.max),
        )

    def generate_plan(self, available_minutes: int) -> list[Task]:
        """Build a plan by adding tasks in priority order while they still fit.

        A task that is too long for the time left is skipped, and smaller
        tasks after it can still be added.

        Args:
            available_minutes: How many minutes the owner has for pet care.

        Returns:
            The chosen tasks, in priority order.
        """
        plan = []
        minutes_used = 0
        for task in self.prioritize_tasks():
            if minutes_used + task.duration <= available_minutes:
                plan.append(task)
                minutes_used += task.duration
        return plan

    def explain_plan(self, plan: list[Task]) -> str:
        """Describe the plan in plain text."""
        if not plan:
            return "No tasks could be scheduled."
        lines = [f"{i}. {task.description} ({task.duration} min)" for i, task in enumerate(plan, 1)]
        lines.append(f"Total: {sum(task.duration for task in plan)} min")
        return "\n".join(lines)
