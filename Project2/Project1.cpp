#include <iostream>
#include <vector>
#include <limits>
#include <fstream>
#include <memory>

// Base class for operations
class Operation {
public:
    virtual double execute(double a, double b) = 0; // Pure virtual function
    virtual std::string getName() = 0; // For logging
    virtual ~Operation() {}
};

class Add : public Operation {
public:
    double execute(double a, double b) override {
        return a + b;
    }
    
    std::string getName() override {
        return "Addition";
    }
};

class Subtract : public Operation {
public:
    double execute(double a, double b) override {
        return a - b;
    }
    
    std::string getName() override {
        return "Subtraction";
    }
};

class Multiply : public Operation {
public:
    double execute(double a, double b) override {
        return a * b;
    }
    
    std::string getName() override {
        return "Multiplication";
    }
};

class Divide : public Operation {
public:
    double execute(double a, double b) override {
        return a / b;
    }
    
    std::string getName() override {
        return "Division";
    }
};

class Calculator {
public:
    void start();

private:
    void displayMenu();
    void performOperation(char operation);
    void logResult(const std::string& operationName, double a, double b, double result);
    void clearInputBuffer();
    
    std::vector<double> results;
};

void Calculator::start() {
    char choice;

    do {
        displayMenu();
        std::cin >> choice;

        if (choice == '5') {
            std::cout << "Exiting the calculator. Goodbye!" << std::endl;
            break;
        }

        if (choice < '1' || choice > '5') {
            std::cout << "Invalid choice. Please try again." << std::endl;
            continue;
        }

        performOperation(choice);
    } while (true);
}

void Calculator::displayMenu() {
    std::cout << "\nSimple Command-Line Calculator" << std::endl;
    std::cout << "1. Add" << std::endl;
    std::cout << "2. Subtract" << std::endl;
    std::cout << "3. Multiply" << std::endl;
    std::cout << "4. Divide" << std::endl;
    std::cout << "5. Exit" << std::endl;
    std::cout << "Enter your choice: ";
}

void Calculator::performOperation(char operation) {
    double a, b;

    std::cout << "Enter first number: ";
    while (!(std::cin >> a)) {
        std::cout << "Invalid input. Please enter a number: ";
        clearInputBuffer();
    }

    std::cout << "Enter second number: ";
    while (!(std::cin >> b)) {
        std::cout << "Invalid input. Please enter a number: ";
        clearInputBuffer();
    }

    double result;
    std::unique_ptr<Operation> op;

    switch (operation) {
        case '1':
            op = std::make_unique<Add>();
            break;
        case '2':
            op = std::make_unique<Subtract>();
            break;
        case '3':
            op = std::make_unique<Multiply>();
            break;
        case '4':
            if (b == 0) {
                std::cout << "Error: Division by zero!" << std::endl;
                return;
            }
            op = std::make_unique<Divide>();
            break;
        default:
            std::cout << "Invalid operation." << std::endl;
            return;
    }

    result = op->execute(a, b);
    results.push_back(result);
    std::cout << "Result: " << result << std::endl;
    logResult(op->getName(), a, b, result);
}

void Calculator::logResult(const std::string& operationName, double a, double b, double result) {
    std::ofstream logFile("calculator_log.txt", std::ios::app);
    if (logFile.is_open()) {
        logFile << operationName << ": " << a << " and " << b << " = " << result << "\n";
        logFile.close();
    } else {
        std::cerr << "Unable to open log file!" << std::endl;
    }
}

void Calculator::clearInputBuffer() {
    std::cin.clear(); // clear the error flag
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // discard input
}

int main() {
    Calculator calc;
    calc.start();
    return 0;
}
