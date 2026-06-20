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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
