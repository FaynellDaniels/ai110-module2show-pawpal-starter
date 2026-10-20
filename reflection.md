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

- One tradeoff my scheduler makes is that conflict detection only checks for exact matching start times instead of overlapping durations. For example, if Buddy has a 30-minute walk at 8:00 and Whiskers has a task at 8:15, the scheduler will not warn me, even though the owner cannot do both at once. It only warns when two pending tasks have the same date and the same start time. Completed tasks and tasks without a time are ignored.

- This tradeoff is reasonable for this scenario because it keeps the code simple and easy to understand. The check groups tasks by start time in one pass, and it returns a warning message instead of crashing the program. A pet owner's daily tasks are usually few and spread across the day, so exact matches are the most obvious conflicts to catch. Checking overlaps would mean sorting the tasks and comparing each task's start time plus duration with the next task's start time, which is more complicated. If I had more time, I would add overlap detection to make the warnings more accurate.

---

## 3. AI Collaboration

**a. How you used AI**

- I used AI for implementing code, and simplifying the code. I started with my class skeletons and asked AI to complete the Task, Pet, Owner, and Scheduler classes. I also used AI to simplify the code, create a demo in main.py, make the schedule easier to read, write tests, and add docstrings. When I had errors, I gave AI the exact error message so it could explain what went wrong. The most helpful prompts were specific and included the file name and requirements. For example, asking AI to complete the four main classes in pawpal_system.py worked well because I clearly explained what each class needed to do. I also asked AI to suggest formatting ideas before making changes, which let me choose the version I liked.

**b. Judgment and verification**

-The first version AI created was more complicated than I needed. It included extra classes and fields that were not necessary for my project. I asked AI to simplify the code and make it easier to understand. The final version had the required classes, fewer fields, and simple docstrings for the methods. I checked the AI's work by running the program instead of only looking at the code. I ran main.py, checked the schedule output, and wrote two tests for mark_complete() and adding a task to a pet. I found a bug where a field named time conflicted with the time class and caused the program to crash. I fixed this by renaming the field to due_time. 

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
