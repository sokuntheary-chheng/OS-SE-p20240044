#include <iostream>
#include <thread>
#include <semaphore.h>
#include <chrono>

struct Account {
    std::string name;
    int balance;

    Account(const std::string& n, int b) : name(n), balance(b) {}
};

// ONE global mutex semaphore — initialized to 1
sem_t mutex;

void transfer(Account& from, Account& to, int amount, const std::string& workerName) {
    std::cout << workerName << " waiting to acquire mutex...\n";
    std::cout << std::flush;

    sem_wait(&mutex);

    std::cout << workerName << " acquired mutex. Transferring " << amount
              << " from " << from.name << " to " << to.name << "...\n";
    std::cout << std::flush;

    // Small sleep to simulate real processing time
    std::this_thread::sleep_for(std::chrono::milliseconds(100));

    from.balance -= amount;
    to.balance   += amount;

    std::cout << workerName << " transferred " << amount
              << " from " << from.name << " to " << to.name << "\n";
    std::cout << std::flush;

    sem_post(&mutex);
}

int main() {
    Account A("Account-A", 1000);
    Account B("Account-B", 1000);

    sem_init(&mutex, 0, 1);

    int startingTotal = A.balance + B.balance;

    std::cout << "=== Bank Transfer Deadlock Prevention ===\n";
    std::cout << "Starting balances:\n";
    std::cout << "  Account-A: " << A.balance << "\n";
    std::cout << "  Account-B: " << B.balance << "\n";
    std::cout << "Starting total: " << startingTotal << "\n\n";
    std::cout << std::flush;

    std::thread t1(transfer, std::ref(A), std::ref(B), 100, "Worker-1");
    std::thread t2(transfer, std::ref(B), std::ref(A), 200, "Worker-2");

    t1.join();
    t2.join();

    int finalTotal = A.balance + B.balance;

    std::cout << "\nFinal balances:\n";
    std::cout << "  Account-A: " << A.balance << "\n";
    std::cout << "  Account-B: " << B.balance << "\n";
    std::cout << "Final total: " << finalTotal << "\n";

    if (finalTotal == startingTotal) {
        std::cout << "Balance check PASSED: total is unchanged.\n";
    } else {
        std::cout << "Balance check FAILED: money was lost or created!\n";
    }

    std::cout << "No deadlock occurred\n";
    std::cout << std::flush;

    sem_destroy(&mutex);
    return 0;
}