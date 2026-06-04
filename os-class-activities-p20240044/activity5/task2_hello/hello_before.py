"""
Task 2A  –  Print HELLO  WITHOUT  Semaphores  (wrong / unpredictable order)
============================================================================
Three threads start at the same time with no ordering constraints.
The OS scheduler decides who runs first, so the letters come out scrambled.

"""

import threading
import time
import random


def process1():
    """Prints H then E"""
    time.sleep(random.uniform(0, 0.08))
    print("H", end="", flush=True)
    time.sleep(random.uniform(0, 0.04))
    print("E", end="", flush=True)


def process2():
    """Prints L and L"""
    time.sleep(random.uniform(0, 0.08))
    print("L", end="", flush=True)
    time.sleep(random.uniform(0, 0.04))
    print("L", end="", flush=True)


def process3():
    """Prints O"""
    time.sleep(random.uniform(0, 0.08))
    print("O", end="", flush=True)


def main():
    print("=" * 50)
    print(" Task 2A  –  HELLO  WITHOUT  Semaphores")
    print(" (order is wrong / unpredictable)")
    print("=" * 50)

    # Run 5 attempts to clearly show the non-determinism
    for attempt in range(1, 6):
        print(f"Attempt {attempt}: ", end="", flush=True)

        t1 = threading.Thread(target=process1)
        t2 = threading.Thread(target=process2)
        t3 = threading.Thread(target=process3)

        # Start all three at nearly the same moment – no ordering guarantee
        t3.start()   # deliberately start in reverse order
        t2.start()   # to show it doesn't matter – semaphores control order,
        t1.start()   # not the start sequence

        t1.join(); t2.join(); t3.join()
        print()   # newline

    print()
    print("Expected : HELLO")
    print("Actual   : see above (scrambled because no semaphores)")


if __name__ == "__main__":
    main()
