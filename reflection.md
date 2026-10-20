# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**
- The design focuses on separating pet and owner information from care tasks and the scheduling logic.The main relationships in the initial UML design are that an Owner has a Pet, the Pet has multiple Tasks, and the Scheduler uses the available Tasks and Constraints to create a Schedule.

- Owner – Stores the pet owner's basic information and preferences, such as their name and available time for pet care. The Owner is also responsible for managing the pet associated with them.

- Pet – Stores information about the pet, such as its name, type, age, and care needs. The Pet is associated with the care tasks that need to be completed for it.

- Task – Represents an individual pet-care activity, such as feeding, walking, medication, grooming, or enrichment. It stores information such as the task name, duration, priority, and any relevant constraints.

- Schedule – Represents the daily care plan created for the pet. It is responsible for organizing selected tasks into a schedule based on the owner's available time and the priorities of the tasks.

- Scheduler – Handles the main scheduling logic. It evaluates the available tasks and constraints, determines which tasks should be included in the daily plan, and assigns them to the schedule. It also provides the reasoning behind why certain tasks were selected.

- Constraint – Represents limitations that the scheduler needs to consider, such as the amount of time the owner has available, task priorities, owner preferences, or other scheduling requirements.


**b. Design changes**

- Yes, the design changed during implementation. After reviewing the initial UML design and receiving AI feedback, I identified several areas where the original design was too vague for the scheduling logic to work reliably.

- One major change was how available time was represented. Originally, the Owner class used a single available_time value. During implementation, I realized that a single time does not clearly represent how much time the owner actually has available for pet care. I changed the design to treat availability as a duration in minutes, which makes it easier for the Scheduler to compare the total duration of tasks against the owner's available time.

- Another change was adding clearer return values to methods. Methods such as get_duration(), get_priority(), get_tasks(), and get_remaining_time() originally did not have clearly defined return values. I clarified these contracts so each method returns the information its name suggests. This makes the classes easier to use and test.

- Finally, I clarified the relationship between the Pet, Task, Scheduler, and Schedule classes. Instead of having the scheduler maintain a separate copy of the pet's tasks, the Pet's task list is treated as the source of truth. The Scheduler uses those tasks and the owner's constraints to generate a new Schedule. This reduces the possibility of the same task being stored in multiple places and becoming out of sync.



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
