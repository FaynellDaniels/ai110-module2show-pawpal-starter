from datetime import time

import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# The owner lives in session_state so pets and tasks survive Streamlit reruns.
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")
owner = st.session_state.owner

PRIORITY_VALUES = {"low": 1, "medium": 2, "high": 3}

st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name)

st.subheader("Add a Pet")
col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    owner.add_pet(Pet(pet_name, species=species))

if owner.pets:
    st.write("Your pets:")
    st.table([{"name": pet.name, "species": pet.species, "tasks": len(pet.tasks)} for pet in owner.pets])
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Add a Task")

if owner.pets:
    selected_pet_name = st.selectbox("Pet", [pet.name for pet in owner.pets])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col4:
        due_time = st.time_input("Time", value=time(8, 0))

    if st.button("Add task"):
        pet = next(p for p in owner.pets if p.name == selected_pet_name)
        pet.add_task(
            Task(task_title, due_time=due_time, duration=int(duration), priority=PRIORITY_VALUES[priority])
        )
else:
    st.info("Add a pet before adding tasks.")

task_rows = [
    {
        "pet": pet.name,
        "task": task.description,
        "time": task.due_time.strftime("%I:%M %p") if task.due_time else "",
        "duration": task.duration,
        "priority": task.priority,
    }
    for pet in owner.pets
    for task in pet.tasks
]
if task_rows:
    st.write("Current tasks:")
    st.table(task_rows)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
available_minutes = st.number_input("Minutes available today", min_value=1, max_value=1440, value=60)

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    plan = scheduler.generate_plan(int(available_minutes))
    if plan:
        st.success("Here is today's plan:")
    st.text(scheduler.explain_plan(plan))
