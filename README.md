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

## 🖥️ Sample Output

Today's Schedule for Khine:
----------------------------------------
[ ] 07:30  Litter change   (10 min) [medium]          
[ ] 08:00  Morning walk    (30 min) [high]                  
[ ] 09:00  Feeding         (10 min) [high]             
[ ] 18:00  Play time       (20 min) [low]           

```
## 🧪 Testing PawPal+

Run the suite from the repo root:

    python -m pytest

The tests cover core object behavior (task completion, adding tasks) and the
scheduling logic: chronological sorting, daily-task recurrence, conflict
detection (overlap and non-overlap), an empty-pet edge case, and the planner
respecting the time budget.

**Confidence Level:** ⭐⭐⭐⭐ (4/5) — the tested behaviors are solid; with more
time I'd add tests for weekly recurrence across month boundaries and conflicts
between different pets.

(.venv) PS C:\Users\khine\ai110-module2show-pawpal-starter> python -m pytest
===================== test session starts ======================
platform win32 -- Python 3.12.2, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\khine\ai110-module2show-pawpal-starter
plugins: anyio-4.14.0
collected 8 items                                               

tests\test_pawpal.py ........                             [100%]

====================== 8 passed in 0.12s =======================

```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | Scheduler.sort_tasks() | Sorts all tasks chronologically by HH:MM time |
| Filtering | Scheduler.filter_tasks(pet_name, completed) | Filter by pet and/or completion status |
| Conflict handling | Scheduler.detect_conflicts() | Flags overlapping time slots (start + duration); returns warnings, never crashes |
| Recurring tasks | Scheduler.mark_task_complete() → _create_next_occurrence() | Daily/weekly tasks spawn the next occurrence (+1 / +7 days via timedelta) | Daily plan | Scheduler.generate_plan(available_minutes) | Greedy, priority-first selection within the time budget; returns planned + skipped-with-reasons

## 📸 Demo Walkthrough
1. Enter the owner's name and add one or more pets with the **Add Pet** button.
2. Pick a pet, fill in a task (title, time, duration, priority), and click **Add task**.
3. Repeat to add a few tasks at different times.
4. Set the time available for the day, then click **Generate schedule**.
5. The app flags any time conflicts, shows the priority-fit plan in a table, and
   notes any tasks it skipped because the budget ran out.
