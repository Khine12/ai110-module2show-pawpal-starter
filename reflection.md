# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial UML has four classes with clear, one-directional relationships: an Owner has many Pets, each Pet has many Tasks, and a Scheduler reads from the Owner to act on all of its tasks. I deliberately separated data from behavior — Owner, Pet, and Task just hold information, while the Scheduler holds the logic.

Classes and responsibilities:

Task — one care activity. Stores its description, start time, duration, priority, frequency, completion status, and due date; can mark itself complete.
Pet — a single animal. Stores its name, species, and its own list of tasks; can add and return those tasks.
Owner — the user. Stores their name, available daily time, and list of pets; can add pets and aggregate every task across all of them.
Scheduler — the system's "brain." Holds no data of its own; it reads from the Owner and is responsible for sorting tasks, generating the daily plan within the time budget, detecting conflicts, and managing recurring tasks.

**b. Design changes**

Yes. While designing, I refined the Task model after re-reading the scenario. I originally treated duration and priority as optional, but the scheduler's core job is fitting tasks into a limited time budget and ordering them by importance — without those two fields it has nothing to reason about — so I made both required. I also added a due_date field early, before implementing recurring tasks, so I won't have to restructure the data model later when a daily task needs to roll over to the next day.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My scheduler considers two constraints: the owner's available time (a daily minute budget) and each task's priority. The planner sorts incomplete tasks by priority first (high → medium → low), then by time, and adds each only if it fits the remaining budget. I treated priority as most important because pet care has non-negotiable tasks like medication and feeding that should never be dropped for optional ones like extra play time, so the planner schedules high-priority tasks first. Time is the hard limit — once the budget is exhausted, remaining tasks are skipped with an explanation.

**b. Tradeoffs**

My planner is greedy: it walks tasks in priority order and takes each if it fits, without reconsidering earlier picks. The tradeoff is that a high-priority task that doesn't fit can be passed over while a smaller, lower-priority task that does fit gets scheduled instead — a smarter algorithm might rearrange to fit the important one. A second tradeoff is in conflict detection: I flag any overlap of two tasks' time windows as a warning rather than auto-resolving it. Both are reasonable here because this is a personal pet-care helper, not a hospital scheduler — predictable, readable behavior and letting the human make the final call matter more than a mathematically optimal plan.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI across the whole build: brainstorming the class design and UML, scaffolding then implementing the methods, drafting the demo script and test suite, and wiring the logic into Streamlit. The most useful prompts were narrow ones tied to a specific method or error — like how the Scheduler should pull tasks from the Owner's pets, or how to use timedelta for the recurring due date — rather than "build the whole app" asks.

**b. Judgment and verification**

One suggestion I modified: a more "Pythonic" conflict-detection using itertools.combinations. It was shorter, but the explicit double loop is easier to read and explain, so I kept the readable version. I verified the logic by running main.py with deliberately overlapping tasks and by writing tests asserting exactly one conflict for overlapping times and zero for non-overlapping ones.

---

## 4. Testing and Verification

**a. What you tested**

I tested task completion and adding tasks, plus the scheduling logic: sorting, recurrence, and conflict detection, with edge cases for an empty pet and a task that exceeds the time budget. 

**b. Confidence**

Confidence: 4/5 — solid on the tested paths; next I'd test weekly recurrence over month boundaries and cross-pet conflicts.

---

## 5. Reflection

**a. What went well**

Went well: the CLI-first workflow — building and verifying the logic in main.py before the UI meant the brain already worked when I reached Streamlit, so I only had to handle st.session_state.  

**b. What you would improve**

Improve: make the planner smarter than greedy so a high-priority task isn't passed over for a smaller low-priority one, and persist data between runs.

**c. Key takeaway**

Key takeaway: staying the lead architect matters even when AI writes code fast — the real decisions (separating data from behavior, putting recurrence on the Scheduler, keeping readable code over clever code) were mine, and AI was most useful when I drove the design and asked narrow questions.