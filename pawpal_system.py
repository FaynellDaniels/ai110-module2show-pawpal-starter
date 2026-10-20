"""Data model skeleton for the PawPal pet-care scheduling system."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, time


@dataclass
class Owner:
    """Stores an owner's information and care preferences."""

    name: str = ""
    available_time: time | None = None
    preferences: list[str] = field(default_factory=list)

    def add_preference(self, preference: str) -> None:
        pass

    def update_availability(self, available_time: time) -> None:
        pass

    def get_preferences(self) -> None:
        pass


@dataclass
class Task:
    """Represents one pet-care activity."""

    name: str = ""
    task_type: str = ""
    duration: int = 0
    priority: int = 0
    preferred_time: time | None = None
    completed: bool = False

    def mark_complete(self) -> None:
        pass

    def update_task(self) -> None:
        pass

    def get_duration(self) -> None:
        pass

    def get_priority(self) -> None:
        pass


@dataclass
class Pet:
    """Stores a pet's information and care tasks."""

    name: str = ""
    species: str = ""
    age: int = 0
    breed: str = ""
    care_needs: str = ""
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def get_tasks(self) -> None:
        pass

    def update_care_needs(self, care_needs: str) -> None:
        pass


@dataclass
class Constraint:
    """Stores rules that determine whether tasks fit a care plan."""

    available_time: time | None = None
    max_task_duration: int = 0
    preferred_times: list[time] = field(default_factory=list)
    owner_preferences: list[str] = field(default_factory=list)

    def check_task(self, task: Task) -> None:
        pass

    def is_satisfied(self) -> None:
        pass

    def update_constraint(self) -> None:
        pass


@dataclass
class Schedule:
    """Represents the tasks planned for a particular date."""

    date: date | None = None
    tasks: list[Task] = field(default_factory=list)
    total_duration: int = 0
    remaining_time: int = 0

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def calculate_duration(self) -> None:
        pass

    def get_remaining_time(self) -> None:
        pass


@dataclass
class Scheduler:
    """Coordinates tasks, constraints, and schedule generation."""

    tasks: list[Task] = field(default_factory=list)
    constraints: list[Constraint] = field(default_factory=list)
    owner: Owner | None = None
    pet: Pet | None = None

    def generate_plan(self) -> None:
        pass

    def prioritize_tasks(self) -> None:
        pass

    def check_constraints(self) -> None:
        pass

    def explain_plan(self) -> None:
        pass