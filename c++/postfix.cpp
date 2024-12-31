#include <iostream>
#include <stack>
#include <sstream>
#include <stdexcept>
#include <string>
#include <cmath>

int evaluatePostfix(const std::string& expression) {
    std::stack<int> stack;
    std::istringstream tokens(expression);
    std::string token;

    while (tokens >> token) {
        if (isdigit(token[0]) || (token.size() > 1 && isdigit(token[1]))) {
            stack.push(std::stoi(token));
        } else if (token == "+" || token == "-" || token == "*" || token == "/" || token == "^") {
            if (stack.size() < 2) {
                throw std::invalid_argument("Invalid postfix expression");
            }
            int operand2 = stack.top();
            stack.pop();
            int operand1 = stack.top();
            stack.pop();
            int result = 0;

            if (token == "+") {
                result = operand1 + operand2;
            } else if (token == "-") {
                result = operand1 - operand2;
            } else if (token == "*") {
                result = operand1 * operand2;
            } else if (token == "^") {
                result = std::pow(operand1, operand2);
            } else if (token == "/") {
                if (operand2 == 0) {
                    throw std::runtime_error("Division by zero");
                }
                result = operand1 / operand2;
            }
            stack.push(result);
        } else {
            // Ignore invalid tokens or handle spaces
        }
    }

    if (stack.size() != 1) {
        throw std::invalid_argument("Invalid postfix expression");
    }

    return stack.top();
}

int main() {
    std::string postfixExpression = "12 3 * 4 2 - +";  // Postfix expression with multi-digit handling

    try {
        int result = evaluatePostfix(postfixExpression);
        std::cout << "Result: " << result << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }

    return 0;
}
