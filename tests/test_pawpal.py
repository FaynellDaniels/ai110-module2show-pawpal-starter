from datetime import date, time, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_changes_status():
    task = Task("Morning walk")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet("Buddy")
    assert len(pet.tasks) == 0

    pet.add_task(Task("Morning walk"))

    assert len(pet.tasks) == 1


def test_completing_daily_task_creates_next_day_task():
    pet = Pet("Buddy")
    walk = Task("Morning walk", frequency="daily")
    pet.add_task(walk)
    scheduler = Scheduler(Owner("Jordan", pets=[pet]))

    next_task = scheduler.mark_task_complete(pet, walk)

    assert walk.completed is True
    assert len(pet.tasks) == 2
    assert next_task.due_date == date.today() + timedelta(days=1)
    assert next_task.completed is False


def test_completing_weekly_task_creates_task_a_week_later():
    pet = Pet("Buddy")
    bath = Task("Bath", frequency="weekly")
    pet.add_task(bath)
    scheduler = Scheduler(Owner("Jordan", pets=[pet]))

    next_task = scheduler.mark_task_complete(pet, bath)

    assert next_task.due_date == date.today() + timedelta(days=7)


def test_completing_one_time_task_creates_no_new_task():
    pet = Pet("Buddy")
    vet = Task("Vet visit")
    pet.add_task(vet)
    scheduler = Scheduler(Owner("Jordan", pets=[pet]))

    next_task = scheduler.mark_task_complete(pet, vet)

    assert next_task is None
    assert len(pet.tasks) == 1


def test_find_conflicts_warns_about_same_time_tasks():
    buddy, whiskers = Pet("Buddy"), Pet("Whiskers")
    buddy.add_task(Task("Walk", due_time=time(8, 0)))
    whiskers.add_task(Task("Breakfast", due_time=time(8, 0)))
    scheduler = Scheduler(Owner("Jordan", pets=[buddy, whiskers]))

    warnings = scheduler.find_conflicts()

    assert len(warnings) == 1
    assert "Walk (Buddy)" in warnings[0] and "Breakfast (Whiskers)" in warnings[0]


def test_find_conflicts_returns_nothing_when_times_differ():
    pet = Pet("Buddy")
    pet.add_task(Task("Walk", due_time=time(8, 0)))
    pet.add_task(Task("Feed", due_time=time(9, 0)))

    assert Scheduler(Owner("Jordan", pets=[pet])).find_conflicts() == []


def test_sort_by_time_returns_tasks_in_chronological_order():
    buddy, whiskers = Pet("Buddy"), Pet("Whiskers")
    buddy.add_task(Task("Evening walk", due_time=time(18, 30)))
    whiskers.add_task(Task("Breakfast", due_time=time(8, 0)))
    buddy.add_task(Task("Medication", due_time=time(12, 0)))
    scheduler = Scheduler(Owner("Jordan", pets=[buddy, whiskers]))

    sorted_tasks = scheduler.sort_by_time()

    assert [task.description for task in sorted_tasks] == ["Breakfast", "Medication", "Evening walk"]


def test_sort_by_time_puts_tasks_without_a_time_last():
    pet = Pet("Buddy")
    pet.add_task(Task("Anytime play"))
    pet.add_task(Task("Breakfast", due_time=time(8, 0)))

    sorted_tasks = Scheduler(Owner("Jordan", pets=[pet])).sort_by_time()

    assert [task.description for task in sorted_tasks] == ["Breakfast", "Anytime play"]


def test_sort_by_time_with_no_tasks_returns_empty_list():
    assert Scheduler(Owner("Jordan", pets=[Pet("Buddy")])).sort_by_time() == []
