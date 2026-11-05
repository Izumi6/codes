"""
================================================================================
  Program 2: Job Sequencing with Deadlines — Greedy Method
  Course: Design and Analysis of Algorithms (410241)

  Description:
    Given a set of jobs where each job has a deadline and a profit, schedule
    jobs on a single machine to maximize total profit. Each job takes exactly
    one unit of time and only one job can be scheduled at a time.

  Greedy Strategy:
    1. Sort all jobs in decreasing order of profit.
    2. For each job, assign it to the latest available time slot
       before its deadline.

  Time Complexity : O(n²) — for each job, we scan for a free slot.
  Space Complexity: O(n)  — for the schedule and slot-tracking arrays.

  No external libraries required. Uses only Python standard library.
================================================================================
"""


class Job:
    """Represents a job with an identifier, deadline, and profit."""

    def __init__(self, job_id, deadline, profit):
        self.job_id = job_id
        self.deadline = deadline
        self.profit = profit

    def __repr__(self):
        return f"Job({self.job_id}, d={self.deadline}, p={self.profit})"


def job_sequencing(jobs):
    """
    Schedule jobs to maximize profit using the greedy approach.

    Parameters:
        jobs (list[Job]): List of Job objects.

    Returns:
        tuple: (scheduled_jobs, total_profit)
            - scheduled_jobs: list of (slot, Job) tuples in time order.
            - total_profit: sum of profits of scheduled jobs.
    """
    # Step 1: Sort jobs by profit in descending order
    jobs_sorted = sorted(jobs, key=lambda j: j.profit, reverse=True)

    # Determine the maximum deadline to define the scheduling window
    max_deadline = max(j.deadline for j in jobs_sorted)

    # Slot array: index 0 is unused; slots 1..max_deadline are time slots
    # None indicates the slot is free
    slot = [None] * (max_deadline + 1)

    scheduled_jobs = []
    total_profit = 0

    # Step 2: Greedily assign each job to the latest free slot ≤ its deadline
    for job in jobs_sorted:
        # Search from the job's deadline down to slot 1
        for t in range(job.deadline, 0, -1):
            if slot[t] is None:
                slot[t] = job
                scheduled_jobs.append((t, job))
                total_profit += job.profit
                break

    # Sort the result by time slot for clear presentation
    scheduled_jobs.sort(key=lambda x: x[0])

    return scheduled_jobs, total_profit


def main():
    print("--- Job Sequencing with Deadlines (Greedy Strategy) ---")
    n = int(input("Enter number of jobs: "))
    jobs = []
    for i in range(1, n + 1):
        deadline = int(input(f"Job {i} Deadline: "))
        profit = int(input(f"Job {i} Profit  : "))
        jobs.append(Job(job_id=f"J{i}", deadline=deadline, profit=profit))

    print("\nInput Jobs:")
    for job in jobs:
        print(f"  {job.job_id}: Deadline = {job.deadline}, Profit = {job.profit}")

    scheduled, total_profit = job_sequencing(jobs)

    print("\nOptimal Scheduled Jobs:")
    for slot_num, job in scheduled:
        print(f"  Slot {slot_num}: {job.job_id} (Profit = {job.profit})")

    print(f"\nTotal Profit: {total_profit}")
    print(f"Jobs Scheduled: {len(scheduled)} out of {len(jobs)}")


if __name__ == "__main__":
    main()

"""
SAMPLE OUTPUT:
----------------------------------------------
--- Job Sequencing with Deadlines (Greedy Strategy) ---
Enter number of jobs: 5
Job 1 Deadline: 2
Job 1 Profit  : 100
Job 2 Deadline: 1
Job 2 Profit  : 19
Job 3 Deadline: 2
Job 3 Profit  : 27
Job 4 Deadline: 1
Job 4 Profit  : 25
Job 5 Deadline: 3
Job 5 Profit  : 15

Input Jobs:
  J1: Deadline = 2, Profit = 100
  J2: Deadline = 1, Profit = 19
  J3: Deadline = 2, Profit = 27
  J4: Deadline = 1, Profit = 25
  J5: Deadline = 3, Profit = 15

Optimal Scheduled Jobs:
  Slot 1: J3 (Profit = 27)
  Slot 2: J1 (Profit = 100)
  Slot 3: J5 (Profit = 15)

Total Profit: 142
Jobs Scheduled: 3 out of 5
----------------------------------------------
"""
