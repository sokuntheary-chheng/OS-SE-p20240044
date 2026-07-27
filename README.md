# OS-SE-p20240044

Operating Systems coursework repository — Chheng Sokuntheary (Student ID: p20240044), Institute of Technology of Cambodia, Year 2 Software Engineering.

This repo contains class activities, lab submissions, and the final exam work for the Operating Systems course.

## Repository Structure

```
OS-SE-p20240044/
├── os-class-activities-p20240044/   # In-class activities (system calls, IPC, threads, semaphores, deadlock)
├── os-lab-p20240044/                # Weekly lab submissions (shell, permissions, threads, security, cron)
├── os-lab-automation/               # Backup/restore automation demo project (cron, tar, logs)
└── os-se-p20240044/final-exam/      # Final exam (real-time graded, server-based)
```

## Class Activities (`os-class-activities-p20240044/`)

| Activity | Topic |
|---|---|
| activity1 | System Calls in Practice (syscalls vs. library calls, `strace`) |
| activity2 | Processes & Inter-Process Communication (fork, shared memory, message queues) |
| activity3 | Socket Communication & Multithreading |
| activity4 | Shared File API (mutex-protected vs. unsynchronized file access, C++/Java) |
| activity5 | Semaphores (producer-consumer, Python) |
| activity6 | Deadlock Simulation (C++, Banker's-style bank account demo) |
| activity7 | Reasoning About Deadlock (Banker's Algorithm) |

## Labs (`os-lab-p20240044/`)

| Lab | Topic |
|---|---|
| lab1 | Introduction to Operating Systems (hands-on) |
| lab2 | File system navigation and organization (`techcorp` directory exercise) |
| lab3 | Wildcards, Links, GRUB & Shared Libraries |
| lab4 | I/O Redirection, Pipelines & Process Management |
| lab5 | Threads, Kernel Workers & Process Signals |
| lab6 | Linux Security, Users, Groups & File Permissions |
| lab7 | Bash Scripting, Permissions & Server Automation |
| lab8 | Race conditions / concurrency exploit exercise (bot swarm, timing attack) |
| lab9 | `flock`-based concurrency & deadlock recovery (timeout, sync scripts) |
| lab10 | Backups, Archiving, Scheduling & `cron` Automation |

## Automation Project (`os-lab-automation/`)

A small demo project (`project/`) used to practice backup/restore workflows, cron-scheduled jobs, and log-based monitoring, including a `restore_demo/` showing recovery from a backup archive.

## Final Exam (`os-se-p20240044/final-exam/`)

Real-time graded practical exam completed on the course server, split into parts:

| Part | Topic |
|---|---|
| Part A | Threads & Signals |
| Part B | Security (setuid) |
| Part C | Shell Scripting |
| Part D | Secure/concurrent resource access (locking) |
| Part E | Automation (backups, cron jobs) |

## Environment

Most C/C++ and shell work targets a Linux server environment (course lab server); a few early activities also include Windows API comparisons. Java activities use plain JDK compilation (`.java`/`.class`).

## Notes

Each subfolder has its own detailed `README.md` with task descriptions, commands used, and screenshots/results for that specific lab or activity.
