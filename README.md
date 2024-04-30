# Passenger Service System
PSS is a tool that will assist the user to schedule his/her activities. It will take various "tasks" as input
and schedule them according to the user's needs. Typical tasks would be attending class, studying,
working on assignment, and so on. Typical outputs will be daily, weekly, or monthly schedules. PSS
also has commands for storing the list of tasks to a data file, or to read those tasks from a data file.
The user will interact with PSS to enter a new task to the system. There are different types of tasks
(see below), but each task will have a start time and a duration. The times and durations should be
rounded to the nearest 15 minutes. If the user attempts to create a task that overlaps an existing task,
PSS will report the overlap and will not create the new task.
Some of the tasks are recurring tasks. These tasks occur on a repeating basis, from a particular start
date to a given end date. For example, one task might be for one hour and 15 minutes, every Tuesday
evening at 7:00 p.m., from January 28th to May 5th.
Another type of task is a transient task, which only occurs one time.
A third type of task is an anti-task, which cancels out one particular occurence of a recurring task. For
example, an anti-task might be set for February 25th, for an hour and 15 minutes starting at 7:00 p.m.
This task would need to refer to the recurring task. Note that if an anti-task removes one instance of a
recurring task, then a transient task could be scheduled at that same time.
Recurring tasks can be further subdivided into Course, Study, Sleep, Exercise, Work, and Meal. Your
group can suggest other types of recurring tasks.
Transient tasks can be further subdivided into Visit, Shopping, and Appointment. You may also add
other types of recurring tasks.

#Implementation
PSS using Model-View-Controller (MVC) design
