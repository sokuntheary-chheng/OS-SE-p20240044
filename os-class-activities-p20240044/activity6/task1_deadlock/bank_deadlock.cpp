#include <iostream>
#include <thread>
#include <semaphore.h>
#include <chrono>
#include <atomic>

struct Account {
    std::string name;
    int balance;
    sem_t lock;

    Account(const std::string& n, int b) : name(n), balance(b) {
        sem_init(&lock, 0, 1);
    }
    ~Account() {
        sem_destroy(&lock);
    }
};

std::atomic<int> completedTransfers(0);

void transfer(Account& from, Account& to, int amount, const std::string& workerName) {
    std::cout << workerName << " trying to lock FROM " << from.name << "\n";
    sem_wait(&from.lock);
    std::cout << workerName << " locked FROM " << from.name << "\n";

    // Sleep so the other thread has time to grab its first lock
    std::this_thread::sleep_for(std::chrono::milliseconds(100));

    std::cout << workerName << " trying to lock TO " << to.name << "\n";
    sem_wait(&to.lock);   // <-- DEADLOCK POINT
    std::cout << workerName << " locked TO " << to.name << "\n";

    from.balance -= amount;
    to.balance   += amount;

    std::cout << workerName << " transfer of " << amount << " completed\n";

    sem_post(&to.lock);
    sem_post(&from.lock);

    completedTransfers++;
}

int main() {
    Account A("Account-A", 1000);
    Account B("Account-B", 1000);

    std::cout << "=== Bank Transfer Deadlock Simulation ===\n";
    std::cout << "Starting balances:\n";
    std::cout << "  Account-A: " << A.balance << "\n";
    std::cout << "  Account-B: " << B.balance << "\n";
    std::cout << "Starting total: " << (A.balance + B.balance) << "\n\n";

    std::thread t1(transfer, std::ref(A), std::ref(B), 100, "Worker-1");
    std::thread t2(transfer, std::ref(B), std::ref(A), 200, "Worker-2");

    // Watchdog: wait up to 3 seconds for transfers to complete
    int elapsed = 0;
    while (elapsed < 3) {
        std::this_thread::sleep_for(std::chrono::seconds(1));
        elapsed++;
        if (completedTransfers >= 2) break;
    }

    if (completedTransfers < 2) {
        std::cout << "\n*** Deadlock detected: transactions are stuck ***\n";
        std::cout << "Worker-1 is waiting for Account-B\n";
        std::cout << "Worker-2 is waiting for Account-A\n";
        std::cout << "Neither thread can proceed. Terminating program.\n";
        std::cout << std::flush;
        t1.detach();
        t2.detach();
        return 1;
    }

    t1.join();
    t2.join();

    std::cout << "\nFinal balances:\n";
    std::cout << "  Account-A: " << A.balance << "\n";
    std::cout << "  Account-B: " << B.balance << "\n";

    return 0;
}