/**
Assigment 9: A palindrome is a string of character that‘s the same forward and backward. Typically, punctuation, capitalization, and spaces are ignored. For example, “Poor Dan is in a droop” is a palindrome, as can be seen by examining the characters “poor danisina droop” and observing that they are the same forward and backward. One way to check for a palindrome is to reverse the characters in the string and then compare with them the original-in a palindrome, the sequence will be identical. Write C++ program with functions-
             a)	To print original string followed by re-versed string using stack
             b)	To check whether given string is palin-drome or not
*/

#include <iostream>
#include <string>

using namespace std;

class Stack {
private:
    string arr;
    
public:
    void push(char c) {
        arr += c;  // Append to the string
    }

    void reverse() {
        cout << "\nReversed string is: ";
        for (int i = arr.length() - 1; i >= 0; i--) {
            cout << arr[i];
        }
        cout << endl;
    }

    bool checkPalindrome(const string& original) {
        return arr == string(arr.rbegin(), arr.rend());  // Check if the string is equal to its reverse
    }
};

void preprocessString(const string& str, string& processed) {
    for (char ch : str) {
        if (isalnum(ch)) {
            processed += tolower(ch);  // Add lowercase alphanumeric characters
        }
    }
}

int main() {
    Stack stack;
    string str, processed;

    cout << "Enter string to check if it is a palindrome: ";
    getline(cin, str);

    preprocessString(str, processed);

    // Push each character of the processed string onto the stack
    for (char ch : processed) {
        stack.push(ch);
    }

    // Check if the processed string is a palindrome
    if (stack.checkPalindrome(processed)) {
        cout << "\nString is a palindrome..." << endl;
    } else {
        cout << "\nString is not a palindrome..." << endl;
    }

    // Print the reversed string
    stack.reverse();

    return 0;
}
