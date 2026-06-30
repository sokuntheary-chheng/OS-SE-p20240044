# Final Exam — Chheng Sokuntheary

Student name: Chheng Sokuntheary
Student ID: p20240044
Server username: se-chheng-sokuntheary
Exam scenario value (COMPANY / PRODUCT): OrbitWorks / Beacon
Date & start time: 2026-06-30, approx 12:40 PM
AI assistant used (name/none): Claude

> Exact commands per part are in `commands.md`. Live-curveball answers are in `live_mods.md`.

---

## Part A — Threads, Kernel Mapping & Signals

**Screenshots**

![A1 — all workers + summary](partA_threads/images/a1_thread_run.png)
![A2 — signal_demo: commands + interaction (signal sent, cleanup msg, clean exit)](partA_threads/images/a2_signal_catch.png)

**Written (one short answer)**

- **Why does a worker thread's joined result reach the main thread, but a forked
  child's value would not?**
  Threads share one address space (joined value read from shared memory); a forked
  child runs in a copied address space, so its changes never reach the parent.

**Anything not completed:** none

---

## Part B — Files, Permissions & Special Bits

**Screenshot**

![B1 — setuid / setgid / sticky bits + id output](partB_security/images/b1_special_bits.png)

**Written (one short answer)**

- **Translate your private file's final octal mode into the 9-char symbolic string**
  octal `600` → `rw-------`

**Anything not completed:** none

---

## Part C — Bash Scripting, PATH & Safe File Scanning

**Screenshot**

![C1 — collector run + consolidated report](partC_scripting/images/c1_collector_run.png)

**Written (one short answer)**

- **Why did `greeter` fail to run by name before you added your `bin` directory to PATH?**
  The shell only searches directories listed in $PATH when resolving a bare command
  name. Before ~/bin was on $PATH, the shell had no way to find greeter unless given
  its exact location (./greeter or full path) — bash doesn't search the current
  directory by default, for security reasons.

**Anything not completed:** none

---

## Part D — Concurrency, a Race Condition & File Locking

**Screenshot**

![D2 — swarm lands at the correct stock after the lock](partD_secure/images/d2_patched.png)

**Written (one short answer)**

- **Why did the unpatched `swarm` sometimes leave more stock than the correct final
  value (with 150 stock and 60 concurrent buyers)?**
  buy_beacon's check-then-act (read stock, validate, then write new stock) is not
  atomic. With 60 concurrent processes, several can read the SAME stale stock value
  before any of them writes back. Concurrent writers can overwrite each other's
  decrements (a lost update), so fewer decrements than expected get applied, leaving
  more stock than correct. In testing, the same underlying race also sometimes drove
  stock below zero, since multiple processes could pass the stock-check against the
  same stale value before any write landed — both are symptoms of the same
  Time-of-Check-to-Time-of-Use race, fixed in D3 with an exclusive flock around the
  read-modify-write critical section.

**Anything not completed:** none — race reproduced as both over-stock and negative-stock
outcomes across unpatched runs; D3's lock produces the correct value (90) on every run.

---

## Part E — Backups, Archiving & cron Automation

**Screenshot**

![E1 — only 2 archives remain + log](partE_automation/images/e1_backup_retention.png)

**Written (one short answer)**

- **Archiving vs compression — which one actually shrank the bytes, and why?**
  tar archives (bundles) many files into one file but does not by itself reduce size;
  the -z flag (gzip) is what actually compresses the bytes by finding and removing
  redundancy in the data. Archiving organizes; compression shrinks.

**Anything not completed:** E1, E2 (recurring + 14:35 one-shot), and E3's recurring
backup_exam entry are all confirmed fired correctly. E3's 16:00 one-shot backup_exam
entry was checked once it fired (see cron_report.txt and partE_automation/logs/ for
final evidence).
