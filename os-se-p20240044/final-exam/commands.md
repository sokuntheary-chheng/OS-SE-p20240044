# commands.md — exact commands I ran, per part

> Paste the **real** commands you ran, in order, in the fenced blocks below. Graded for
> command competency and is your defence if any output is questioned. One block per part.
> Delete the hint comments and replace with your actual commands.

## Part A — Threads, Mapping & Signals

```bash
# compile the threaded program (mind the threading flag), run it
# capture the 1:1 user→kernel (LWP) mapping into thread_map.txt while it runs
# compile/run signal_demo and demonstrate catching the interactive interrupt
gcc -pthread partA_threads/thread_demo.c -o partA_threads/thread_demo
./partA_threads/thread_demo

cp partA_threads/thread_demo.c /tmp/thread_demo_evidence.c
# edited /tmp copy only: added sleep(3) inside worker() before computing result
gcc -pthread /tmp/thread_demo_evidence.c -o /tmp/thread_demo_evidence
/tmp/thread_demo_evidence &
PID=$!
ls /proc/$PID/task
ps -eLf | grep $PID
cat /proc/$PID/status | grep -i threads
gcc partA_threads/signal_demo.c -o partA_threads/signal_demo
./partA_threads/signal_demo
# ran, let it loop, sent SIGINT via Ctrl+C, observed cleanup + exit
```

## Part B — Permissions, Special Bits & ACLs

```bash
# build the tree (shared dir + private file); set octal + symbolic modes
# demonstrate setgid + sticky on a dir you own; build/set the setuid binary
# add and read back an ACL entry; save reports
mkdir -p partB_security/shared_dir
touch partB_security/private_file.txt
echo "confidential OrbitWorks data" > partB_security/private_file.txt
chmod 600 partB_security/private_file.txt
chmod u=rw,go= partB_security/private_file.txt
chmod 711 partB_security/shared_dir
chmod u=rwx,g=x,o=x partB_security/shared_dir
ls -l partB_security/private_file.txt
ls -ld partB_security/shared_dir
stat partB_security/private_file.txt
stat partB_security/shared_dir
# saved into partB_security/perm_report.txt
mkdir partB_security/setgid_dir
chmod g+s partB_security/setgid_dir
ls -ld partB_security/setgid_dir

mkdir partB_security/sticky_dir
chmod +t partB_security/sticky_dir
ls -ld partB_security/sticky_dir

gcc partB_security/setuid_demo.c -o partB_security/setuid_demo
chmod u+s partB_security/setuid_demo
ls -l partB_security/setuid_demo
./partB_security/setuid_demo
# saved combined evidence + explanation into partB_security/perm_report.txt
# screenshot: b1_special_bits.png
```

## Part C — Bash Scripting, PATH & Safe Scanning

```bash
# make greeter runnable by name via PATH; record PATH + resolved location
# run collector over your dirs; show it skips unreadable/missing files safely
mkdir -p partC_scripting/scripts partC_scripting/images
cd partC_scripting/scripts
# created greeter (variable + array + command substitution)
chmod +x greeter
cp greeter ~/bin/greeter
hash -r
greeter
# saved PATH + which/type output into partC_scripting/path_report.txt
mkdir -p ~/collector_test/dir1 ~/collector_test/dir2
echo "Report A: Beacon stock check OK" > ~/collector_test/dir1/file1.txt
echo "Report B: backup completed" > ~/collector_test/dir2/file2.txt
echo "secret data" > ~/collector_test/dir1/locked.txt
chmod 000 ~/collector_test/dir1/locked.txt
# created collector script (loops candidates, checks -e and -r before touching, skips safely)
chmod +x collector
./collector
cat collected_report.txt
# screenshot: c1_collector_run.png
```

## Part D — Race Condition & flock

```bash
# init stock; run swarm several times unpatched and record final stock each time
# add the exclusive advisory lock around the read-modify-write; re-run swarm
# D1: buy_beacon created (validates qty, reads/decrements stock, logs with student_id)
chmod +x partD_secure/scripts/buy_beacon
echo "150" > partD_secure/stock.txt
./partD_secure/scripts/buy_beacon Alice 5
cat partD_secure/stock.txt
cat partD_secure/sales.log

# D2: swarm created (60 concurrent background purchases)
chmod +x partD_secure/scripts/swarm
echo "150" > partD_secure/stock.txt
./partD_secure/scripts/swarm
cat partD_secure/stock.txt   # run 1: -1
echo "150" > partD_secure/stock.txt
./partD_secure/scripts/swarm
cat partD_secure/stock.txt   # run 2: -1
echo "150" > partD_secure/stock.txt
./partD_secure/scripts/swarm
cat partD_secure/stock.txt   # run 3: 140
# results saved into partD_secure/observations.txt

# D3: patched buy_beacon — wrapped read-modify-write in ( flock -x 200; ... ) 200>"$LOCK_FILE"
chmod +x partD_secure/scripts/buy_beacon
echo "150" > partD_secure/stock.txt
./partD_secure/scripts/swarm
cat partD_secure/stock.txt   # 90
echo "150" > partD_secure/stock.txt
./partD_secure/scripts/swarm
cat partD_secure/stock.txt   # 90
echo "150" > partD_secure/stock.txt
./partD_secure/scripts/swarm
cat partD_secure/stock.txt   # 90
# screenshot: d2_patched.png
```

## Part E — Backups & cron

```bash
# E1: run backup_project enough times that pruning happens (keep newest RETAIN_N)
# E2: per-user crontab, two entries (absolute paths):
#     recurring (CRON_INTERVAL) -> partE_automation/logs/cron_recurring.log
#     one-shot at TIMED        -> partE_automation/logs/cron_oneshot.log
# E3: backup_exam -> tar the final-exam folder to ~/exam-backups/final-exam-<ts>.tar.gz
#     crontab: run backup_exam on a short interval AND once at exactly 16:00 today
#     then: ls ~/exam-backups
# capture crontab -l + both logs + the ~/exam-backups listing into cron_report.txt
# E1: backup_project
mkdir -p ~/sample_project/src ~/sample_project/docs
echo "print('hello orbitworks')" > ~/sample_project/src/main.py
echo "Project notes" > ~/sample_project/docs/notes.txt
chmod +x partE_automation/scripts/backup_project
./partE_automation/scripts/backup_project   # run 1
sleep 2
./partE_automation/scripts/backup_project   # run 2
sleep 2
./partE_automation/scripts/backup_project   # run 3 - pruning starts
sleep 2
./partE_automation/scripts/backup_project   # run 4 - pruning continues, 2 archives remain
# log saved into partE_automation/backup_log.txt
# screenshot: e1_backup_retention.png
# E2: timed_job + crontab (recurring every 1 min, one-shot at 14:35)
chmod +x partE_automation/scripts/timed_job
crontab -e
# added:
# * * * * * .../timed_job .../logs/cron_recurring.log
# 35 14 * * * .../timed_job .../logs/cron_oneshot.log
crontab -l

# E3: backup_exam (tar final-exam/ to ~/exam-backups/) + crontab (every 5 min + 16:00 one-shot)
chmod +x partE_automation/scripts/backup_exam
mkdir -p ~/exam-backups
./partE_automation/scripts/backup_exam
ls -la ~/exam-backups
crontab -e
# added:
# */5 * * * * .../backup_exam >> .../logs/backup_exam_cron.log 2>&1
# 0 16 * * * .../backup_exam >> .../logs/backup_exam_cron.log 2>&1
crontab -l
```
