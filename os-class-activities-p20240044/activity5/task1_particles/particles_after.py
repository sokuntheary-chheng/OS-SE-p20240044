"""
Task 1B  –  Particle Pair Buffer  WITH  Semaphores  (correct, runs forever)
============================================================================
Semaphore names and initial values match the filled-in worksheet answer:

    s     = 0     counting semaphore – number of complete pairs ready to fetch
    space = 50    counting semaphore – number of free pair-slots in the buffer
    lock  = 1     binary  semaphore  – mutual exclusion on the shared buffer

Producer pseudocode (from worksheet):
    wait(space)
    Produce P1, P2
    wait(lock)
        Place P1 in buffer
        Place P2 in buffer
    signal(s)
    signal(lock)
    Go to PLoop

Consumer pseudocode (from worksheet):
    wait(s)   wait(lock)
        Fetch P1 from buffer
        Fetch P2 from buffer
    signal(space)   signal(lock)
    Package and ship
    Go to CLoop
"""

import threading
import time
import random

# ── Buffer & counters ──────────────────────────────────────────────────────
BUFFER_CAPACITY = 100          # 100 particles = 50 pairs
NUM_PRODUCERS   = 4            # multiple producer machines

buffer         = []
produced_pairs = 0
packaged_pairs = 0
running        = True
error_flag     = threading.Event()

# ── Semaphores  (names match worksheet) ───────────────────────────────────
s     = threading.Semaphore(0)    # full pairs available to consumer
space = threading.Semaphore(50)   # free pair-slots available to producers
lock  = threading.Semaphore(1)    # mutex – protects buffer list


# ── Producer ──────────────────────────────────────────────────────────────
def producer(machine_id: int):
    global produced_pairs, running
    pair_id = 0

    while running and not error_flag.is_set():
        pair_id += 1
        p1 = f"M{machine_id}-{pair_id}-P1"
        p2 = f"M{machine_id}-{pair_id}-P2"

        # ── wait(space) ── block until a pair slot is free
        space.acquire()

        # Produce (outside the lock – no shared state needed yet)
        time.sleep(random.uniform(0.005, 0.02))   # simulate production time

        # ── wait(lock) ── enter critical section
        lock.acquire()
        try:
            # Safety guard (should never fire with correct semaphores)
            if len(buffer) + 2 > BUFFER_CAPACITY:
                print("The producing machine is broken")
                error_flag.set()
                running = False
                return

            buffer.append(p1)
            buffer.append(p2)
            produced_pairs += 1
        finally:
            # ── signal(s) + signal(lock) ──
            s.release()       # one more pair is ready for the consumer
            lock.release()    # leave critical section


# ── Consumer ──────────────────────────────────────────────────────────────
def consumer():
    global packaged_pairs, running

    while running and not error_flag.is_set():

        # ── wait(s) ── block until at least one pair is ready
        s.acquire()

        # ── wait(lock) ── enter critical section
        lock.acquire()
        try:
            # Safety guard (should never fire with correct semaphores)
            if len(buffer) < 2:
                print("The packaging machine is broken")
                error_flag.set()
                running = False
                return

            p1 = buffer.pop(0)
            p2 = buffer.pop(0)
        finally:
            # ── signal(space) + signal(lock) ──
            space.release()   # one pair-slot is free again
            lock.release()    # leave critical section

        # ── Pair integrity check (outside the lock) ───────────────────────
        p1_base = p1.rsplit("-", 1)[0]   # "M2-17"
        p2_base = p2.rsplit("-", 1)[0]   # must also be "M2-17"

        if p1_base != p2_base:
            print("Pairs are incorrect")
            print(f"  Got: {p1} + {p2}")
            error_flag.set()
            running = False
            return

        # ── Package and ship ──────────────────────────────────────────────
        packaged_pairs += 1
        print(
            f"Produced pairs: {produced_pairs:4d} | "
            f"Packaged pairs: {packaged_pairs:4d} | "
            f"Buffer particles: {len(buffer):3d} | "
            f"Shipped: {p1} + {p2}"
        )

        time.sleep(random.uniform(0.01, 0.03))   # simulate packaging time


# ── Main ──────────────────────────────────────────────────────────────────
def main():
    global running

    print("=" * 70)
    print(" Task 1B  –  Particle Pair Buffer  WITH  Semaphores")
    print(f" Buffer capacity : {BUFFER_CAPACITY} particles ({BUFFER_CAPACITY // 2} pairs)")
    print(f" Producer machines: {NUM_PRODUCERS}")
    print(" Semaphores: s=0  space=50  lock=1   (matches worksheet)")
    print(" Press Ctrl+C to stop.")
    print("=" * 70)

    threads = []

    for i in range(1, NUM_PRODUCERS + 1):
        t = threading.Thread(target=producer, args=(i,), daemon=True)
        threads.append(t)
        t.start()

    c = threading.Thread(target=consumer, daemon=True)
    c.start()
    threads.append(c)

    try:
        while running and not error_flag.is_set():
            time.sleep(0.1)
    except KeyboardInterrupt:
        running = False
        print("\nStopped by user (Ctrl+C).")

    time.sleep(0.2)
    print("\n" + "=" * 70)
    print(f" Total produced : {produced_pairs} pairs")
    print(f" Total packaged : {packaged_pairs} pairs")
    print(f" Buffer remaining: {len(buffer)} particles")
    print("=" * 70)


if __name__ == "__main__":
    main()
