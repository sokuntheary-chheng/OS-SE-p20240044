"""
Task 2B  –  Print HELLO  WITH  Semaphores  (always correct)
============================================================
Semaphore names match the worksheet (Problem 2B):  a, b, c

Worksheet solution:
    a = 1   (lets Process 1 start immediately)
    b = 0   (released by P1 after HE; gates P2's first L)
    c = 0   (released by P2 after LL; gates P3's O)

Process 1              Process 2              Process 3
--------               --------               --------
wait(a)                wait(b)                wait(c)
print("H")             print("L")             print("O")
print("E")             print("L")
signal(b)              signal(c)

This guarantees the order:  H → E → L → L → O  =  HELLO
"""

import threading

# ── Semaphores  (names and values from worksheet) ─────────────────────────
a = threading.Semaphore(1)   # Process 1 may start immediately
b = threading.Semaphore(0)   # released after HE printed
c = threading.Semaphore(0)   # released after LL printed


def process1():
    a.acquire()          # wait(a)
    print("H", end="", flush=True)
    print("E", end="", flush=True)
    b.release()          # signal(b)  →  allow Process 2 to print L


def process2():
    b.acquire()          # wait(b)  →  wait until HE is done
    print("L", end="", flush=True)
    print("L", end="", flush=True)
    c.release()          # signal(c)  →  allow Process 3 to print O


def process3():
    c.acquire()          # wait(c)  →  wait until LL is done
    print("O", end="", flush=True)


def run_once():
    """Spawn all three processes and wait for them to finish."""
    t1 = threading.Thread(target=process1)
    t2 = threading.Thread(target=process2)
    t3 = threading.Thread(target=process3)

    # Start in reverse order to prove the semaphores – not start order – control output
    t3.start()
    t2.start()
    t1.start()

    t1.join(); t2.join(); t3.join()
    print()   # newline after HELLO


def main():
    global a, b, c

    print("=" * 50)
    print(" Task 2B  –  HELLO  WITH  Semaphores")
    print(" Semaphores: a=1  b=0  c=0  (matches worksheet)")
    print("=" * 50)

    # ── Basic requirement: print HELLO once ──────────────────────────────
    print("Single run: ", end="", flush=True)
    run_once()

    # ── Optional extension: print HELLO three times ──────────────────────
    print("\nOptional extension (HELLO × 3):")
    for i in range(1, 4):
        # Reset semaphores for each round
        a = threading.Semaphore(1)
        b = threading.Semaphore(0)
        c = threading.Semaphore(0)

        print(f"  Round {i}: ", end="", flush=True)
        run_once()

    print("\nDone – output is always HELLO regardless of thread start order.")


if __name__ == "__main__":
    main()
