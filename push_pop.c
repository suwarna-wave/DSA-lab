#include <stdio.h>
#define MAX 100
int stack[MAX], top = -1;


// Function to add an element to the stack: Push
void push(int item) {
    if (top == MAX - 1) {
        printf("Stack Overflow\n");      //stack is full
        return;
    }
    stack[++top] = item;
}


// Function to remove an element from the stack: Pop
int pop() {
    if (top == -1) {
        printf("Stack Underflow\n");     //stack is empty
        return -1;
    }
    return stack[top--];
}



// Function to display the elements of the stack
void display() {
    if (top == -1) {
        printf("Stack is empty\n");
        return;
    }
    printf("Stack elements are:\n");
    for (int i = top; i >= 0; i--) {
        printf("%d\n", stack[i]);
    }
}


int main() {
    int choice, item;
    
    while (1) {
        printf("1. Push\n");
        printf("2. Pop\n");
        printf("3. Display\n");
        printf("4. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);
        
        switch (choice) {
            case 1:
                printf("Enter the element to be pushed: ");
                scanf("%d", &item);
                push(item);
                break;
            case 2:
                item = pop();
                if (item != -1) {
                    printf("Popped item is: %d\n", item);
                }
                break;
            case 3:
                display();
                break;
            case 4:
                return 0;
            default:
                printf("Invalid choice\n");
        }
    }
    
    return 0;
}

