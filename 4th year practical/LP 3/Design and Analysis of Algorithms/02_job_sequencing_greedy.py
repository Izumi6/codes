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


def print_job_table(jobs, title="INPUT JOBS"):
    """Display a formatted table of jobs."""
    print(f"\n  {title}")
    print(f"  {'─' * 45}")
    print(f"  {'Job ID':<12} {'Deadline':>10} {'Profit':>12}")
    print(f"  {'─' * 45}")
    for job in jobs:
        print(f"  {job.job_id:<12} {job.deadline:>10} {job.profit:>12}")
    print(f"  {'─' * 45}")


def main():
    print("=" * 60)
    print("   JOB SEQUENCING WITH DEADLINES — GREEDY METHOD")
    print("=" * 60)

    try:
        user_input = input("\n  Enter the number of jobs (press Enter for default 5 jobs): ").strip()
    except EOFError:
        user_input = ""
    if not user_input:
        print("  Using default sample jobs: J1(d=2, p=100), J2(d=1, p=19), J3(d=2, p=27), J4(d=1, p=25), J5(d=3, p=15)")
        jobs = [
            Job(job_id="J1", deadline=2, profit=100),
            Job(job_id="J2", deadline=1, profit=19),
            Job(job_id="J3", deadline=2, profit=27),
            Job(job_id="J4", deadline=1, profit=25),
            Job(job_id="J5", deadline=3, profit=15)
        ]
    else:
        n = int(user_input)
        jobs = []
        print("\n  Enter job details (deadline and profit for each job):")
        print(f"  {'─' * 45}")

        for i in range(1, n + 1):
            deadline = int(input(f"    Job J{i} — Deadline : "))
            profit = int(input(f"    Job J{i} — Profit   : "))
            jobs.append(Job(job_id=f"J{i}", deadline=deadline, profit=profit))
            print()

    # Display the input jobs
    print_job_table(jobs)

    # Execute greedy job sequencing
    scheduled, total_profit = job_sequencing(jobs)

    # ── Display Results ──────────────────────────────────────────────────
    print(f"\n{'═' * 60}")
    print("  OPTIMAL JOB SCHEDULE (Greedy by Profit)")
    print(f"{'═' * 60}")
    print(f"  {'Time Slot':<12} {'Job ID':<12} {'Profit':>12}")
    print(f"  {'─' * 45}")

    for slot_num, job in scheduled:
        print(f"  {slot_num:<12} {job.job_id:<12} {job.profit:>12}")

    print(f"  {'─' * 45}")
    print(f"  {'TOTAL PROFIT':<24} {total_profit:>12}")
    print(f"  {'Jobs Scheduled':<24} {len(scheduled):>12} / {len(jobs)}")
    print(f"{'═' * 60}\n")


if __name__ == "__main__":
    main()

"""
============================== SAMPLE OUTPUT ==============================

  Enter the number of jobs: 4
    Job J1 — Deadline: 2, Profit: 100
    Job J2 — Deadline: 1, Profit: 19
    Job J3 — Deadline: 3, Profit: 27
    Job J4 — Deadline: 4, Profit: 25

  OPTIMAL JOB SCHEDULE (Greedy by Profit)
    Time Slot    Job ID         Profit
    1            J2                 19
    2            J1                100
    3            J3                 27
    4            J4                 25
    TOTAL PROFIT                  171
    Jobs Scheduled                  4 / 4

========================================================================
"""
