"""
Task 1A  –  Particle Pair Buffer  WITHOUT  Semaphores  (intentionally broken)
==============================================================================
Demonstrates the three failure modes the activity requires:
  • "The packaging machine is broken"  (consumer fetches from empty buffer)
  • "The producing machine is broken"  (producer adds to a full buffer)
  • "Pairs are incorrect"              (P1 and P2 from different machines)

There is NO mutex and NO counting semaphore, so race conditions occur quickly.
Run it, let it crash on its own, then take your screenshot.
"""

import threading
import time
import random

# ── shared state ────────────────────────────────────────────────────────────
BUFFER_CAPACITY = 100          # 100 particles = 50 pairs
buffer          = []           # shared particle buffer  (NO protection)
produced_pairs  = 0
packaged_pairs  = 0
running         = True         # set to False to stop all threads


# ── Producer  (NO semaphores – intentionally unsafe) ─────────────────────
def producer(machine_id: int):
    global produced_pairs, running
    pair_id = 0

    while running:
        pair_id += 1
        p1 = f"M{machine_id}-{pair_id}-P1"
        p2 = f"M{machine_id}-{pair_id}-P2"

        # Full-buffer check with NO semaphore – another thread can sneak in
        if len(buffer) + 2 > BUFFER_CAPACITY:
            print("The producing machine is broken")
            running = False
            return

        # Deliberate tiny gap between P1 and P2  →  creates the race window
        buffer.append(p1)
        time.sleep(random.uniform(0, 0.003))   # context-switch simulation
        buffer.append(p2)

        produced_pairs += 1
        time.sleep(random.uniform(0.005, 0.02))


# ── Consumer  (NO semaphores – intentionally unsafe) ─────────────────────
def consumer():
    global packaged_pairs, running

    while running:
        time.sleep(0.015)          # consumer runs slightly slower

        # Empty-buffer check with NO semaphore
        if len(buffer) == 0:
            print("The packaging machine is broken")
            running = False
            return

        if len(buffer) < 2:
            continue               # wait a little then retry

        # Pop two items with NO mutex – another thread may interleave here
        p1 = buffer.pop(0)
        p2 = buffer.pop(0)

        # ── Pair integrity check ──────────────────────────────────────────
        # Format: M<machine>-<pairID>-P1  /  M<machine>-<pairID>-P2
        # Strip the trailing -P1 / -P2 and compare the base strings.
        p1_base = p1.rsplit("-", 1)[0]   # e.g. "M2-17"
        p2_base = p2.rsplit("-", 1)[0]   # e.g. "M3-5"

        if p1_base != p2_base:
            print("Pairs are incorrect")
            print(f"  Got: {p1} + {p2}")
            running = False
            return

        packaged_pairs += 1
        print(
            f"[BEFORE] Produced: {produced_pairs:4d} | "
            f"Packaged: {packaged_pairs:4d} | "
            f"Buffer: {len(buffer):3d} particles"
        )


# ── Main ──────────────────────────────────────────────────────────────────
def main():
    global running

    print("=" * 60)
    print(" Task 1A  –  Particle Buffer  WITHOUT  Semaphores")
    print(" (will break quickly due to race conditions)")
    print("=" * 60)

    NUM_PRODUCERS = 4
    threads = []

    for i in range(1, NUM_PRODUCERS + 1):
        t = threading.Thread(target=producer, args=(i,), daemon=True)
        threads.append(t)
        t.start()

    c = threading.Thread(target=consumer, daemon=True)
    c.start()
    threads.append(c)

    try:
        while running:
            time.sleep(0.05)
    except KeyboardInterrupt:
        running = False
        print("\nStopped by user.")

    time.sleep(0.2)   # let error message print before exit
    print(f"\nFinal – Produced: {produced_pairs} | Packaged: {packaged_pairs}")


if __name__ == "__main__":
    main()
