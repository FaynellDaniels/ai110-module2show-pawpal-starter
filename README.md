# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Implementation Summary
The implementation builds the PawPal system using several classes that work together to manage pet owners, pets, preferences, and scheduling. The Owner class stores information about pet owners and their preferences, while the Pet class represents individual pets and their details. The Schedule class manages scheduled activities or appointments for pets, and the Scheduler class helps create and organize these schedules. Together, these classes allow the system to connect owners with their pets, use owner preferences, and manage pet-related schedules in an organized way.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
==============================================
  Today's Schedule - Jordan
==============================================
  TIME      TASK              PET        LENGTH
----------------------------------------------
   7:30 AM  Morning walk      Buddy       30 min
   8:00 AM  Breakfast         Whiskers    10 min
  12:00 PM  Give medication   Buddy        5 min
   6:30 PM  Play session      Whiskers    20 min
----------------------------------------------
  4 tasks, 65 min total

```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
=============================================================== test session starts ================================================================
platform darwin -- Python 3.13.15, pytest-9.1.1, pluggy-1.7.0
rootdir: /Users/nellie/Documents/ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 10 items                                                                                                                                 

tests/test_pawpal.py ..........                                                                                                              [100%]

================================================================ 10 passed in 0.03s ================================================================
```


- The 10 tests cover four areas:

- Basic behavior: mark_complete() changes a task's status, and adding a task to a pet increases its task count.

- Sorting: sort_by_time() returns tasks from all pets in chronological order. It puts tasks with no time last, and returns an empty list when there are no tasks.

- Recurring tasks: completing a daily task creates a new one due tomorrow. A weekly task creates one due in 7 days, and a one-time task creates nothing.

- Conflict detection: two tasks at the same time produce a warning naming both. Tasks at different times produce none.


## 📐 Smarter Scheduling



| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | Scheduler.sort_by_time(), Scheduler.prioritize_tasks() | Sorts by time of day (earliest first, tasks with no time last), or by priority (highest first, then earliest time) |
| Filtering | Scheduler.filter_tasks() | Filters by completion status (completed=True/False), by pet (pet_name="Buddy"), or both |
| Conflict handling | Scheduler.find_conflicts() | Returns a warning when two pending tasks share the same date and start time (same pet or different pets); overlapping durations are not checked |
| Recurring tasks | Scheduler.mark_task_complete(), Task.next_occurrence() | Completing a "daily" task adds a copy due tomorrow; a "weekly" task adds one due in 7 days |


## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
