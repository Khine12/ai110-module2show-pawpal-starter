import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.markdown("A pet care planning assistant — add your pets, give them tasks, and build a daily schedule.")

with st.expander("Scenario", expanded=False):
    st.markdown(
        """
**PawPal+** helps a pet owner plan care tasks for their pet(s) based on constraints
like time, priority, and preferences.
"""
    )

# --- Create the Owner ONCE and keep it across reruns ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Owner", available_minutes=120)
owner = st.session_state.owner

st.divider()

# --- Owner + Pets ---
st.subheader("Owner & Pets")
owner.name = st.text_input("Owner name", value=owner.name)

col_a, col_b = st.columns(2)
with col_a:
    pet_name = st.text_input("Pet name", value="Mochi")
with col_b:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add Pet"):
    owner.add_pet(Pet(name=pet_name, species=species))
    st.success(f"Added {pet_name} the {species}!")

if owner.pets:
    st.write("**Your pets:** " + ", ".join(p.name for p in owner.pets))
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Add a Task ---
st.subheader("Add a Task")
if owner.pets:
    pet_choice = st.selectbox("Which pet?", [p.name for p in owner.pets])

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        task_time = st.text_input("Time (HH:MM)", value="08:00")
    with col3:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    if st.button("Add task"):
        pet = next(p for p in owner.pets if p.name == pet_choice)
        pet.add_task(Task(task_title, task_time, int(duration), priority))
        st.success(f"Added '{task_title}' to {pet_choice}.")
else:
    st.info("Add a pet first, then you can give it tasks.")

# Show all current tasks
all_tasks = owner.get_all_tasks()
if all_tasks:
    st.write("Current tasks:")
    st.table([
        {"Time": t.time, "Task": t.description,
         "Duration (min)": t.duration, "Priority": t.priority}
        for t in all_tasks
    ])

st.divider()

# --- Generate Schedule ---
st.subheader("Today's Schedule")
budget = st.number_input("Time available today (minutes)",
                         min_value=10, max_value=1440,
                         value=owner.available_minutes)
owner.available_minutes = int(budget)

if st.button("Generate schedule"):
    if not owner.get_all_tasks():
        st.warning("No tasks yet — add some above first.")
    else:
        scheduler = Scheduler(owner)

        # Conflicts shown as warnings the owner can act on
        for w in scheduler.detect_conflicts():
            st.warning(w)

        # The priority-fit plan
        planned, skipped = scheduler.generate_plan()
        if planned:
            st.success("Planned for today:")
            st.table([
                {"Time": t.time, "Task": t.description,
                 "Duration (min)": t.duration, "Priority": t.priority}
                for t in sorted(planned, key=lambda t: t.time)
            ])
        # What didn't fit, and why
        for t, reason in skipped:
            st.caption(f"Skipped '{t.description}' — {reason}")