/**
Assignment 10: Implement C++ program for expression conversion as infix to postfix and its evaluation using stack based on given conditions:
                1.	Operands and operator, both must be sin-gle character.
                2.	Input Postfix expression must be in a de-sired format.
                3.	Only '+', '-', '*' and '/ ' operators are ex-pected.
*/

#include <iostream>
using namespace std;

#define MAX 100

class Stack {
    char arr[MAX];
    int top;

public:
    Stack() { top = -1; }

    void push(char x) {
        if (top < MAX - 1) {
            arr[++top] = x;
        }
    }

    char pop() {
        if (top >= 0) {
            return arr[top--];
        }
        return '\0'; // Return null character if stack is empty
    }

    char peek() {
        if (top >= 0) {
            return arr[top];
        }
        return '\0';
    }

    bool isEmpty() {
        return top == -1;
    }
};

// Function to determine precedence of operators
int precedence(char op) {
    if (op == '+' || op == '-') return 1;
    if (op == '*' || op == '/') return 2;
    return 0;
}

// Function to convert infix to postfix
void infixToPostfix(const char* infix, char* postfix) {
    Stack opStack;
    int j = 0; // Index for postfix

    for (int i = 0; infix[i] != '\0'; i++) {
        char ch = infix[i];

        if (isalnum(ch)) { // If the character is an operand
            postfix[j++] = ch;
        } else if (ch == '(') {
            opStack.push(ch);
        } else if (ch == ')') {
            while (!opStack.isEmpty() && opStack.peek() != '(') {
                postfix[j++] = opStack.pop();
            }
            opStack.pop(); // Pop the '('
        } else { // Operator
            while (!opStack.isEmpty() && precedence(opStack.peek()) >= precedence(ch)) {
                postfix[j++] = opStack.pop();
            }
            opStack.push(ch);
        }
    }

    // Pop all remaining operators from the stack
    while (!opStack.isEmpty()) {
        postfix[j++] = opStack.pop();
    }
    postfix[j] = '\0'; // Null-terminate the postfix string
}

// Function to evaluate postfix expression
int evaluatePostfix(const char* postfix) {
    Stack evalStack;

    for (int i = 0; postfix[i] != '\0'; i++) {
        char ch = postfix[i];

        if (isdigit(ch)) { // If the character is an operand
            evalStack.push(ch - '0'); // Convert char to int
        } else { // Operator
            int op2 = evalStack.pop();
            int op1 = evalStack.pop();
            switch (ch) {
                case '+': evalStack.push(op1 + op2); break;
                case '-': evalStack.push(op1 - op2); break;
                case '*': evalStack.push(op1 * op2); break;
                case '/': evalStack.push(op1 / op2); break;
            }
        }
    }
    return evalStack.pop(); // The result will be the last remaining value
}

int main() {
    char infix[MAX], postfix[MAX];

    cout << "Enter an infix expression: ";
    cin.getline(infix, MAX);

    infixToPostfix(infix, postfix);
    cout << "Postfix expression: " << postfix << endl;

    int result = evaluatePostfix(postfix);
    cout << "Evaluation result: " << result << endl;

    return 0;
}
