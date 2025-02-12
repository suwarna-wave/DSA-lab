#include <stdio.h>
#include <stdlib.h>

struct stack {
    int top;
    int size;
    int *s;
};

void createstack(struct stack *st) {
    st->top = -1;
    printf("Enter the size of the stack: ");
    scanf("%d", &st->size);
    st->s = (int *)malloc(st->size * sizeof(int));
}

void displaystack(struct stack st) 
{
    int i;
    for (i = st.top; i >= 0; i--) {
        printf("%d ", st.s[i]);
    }
    printf("\n") ;
}

void push(struct stack *st, int x) {
    if (st->top == st->size - 1) {
        printf("Stack Overflow\n");
    } else {
        st->top++;
        st->s[st->top] = x;
    }
}

void pop(struct stack *st) {
    if (st->top == -1) {
        printf("Stack Underflow\n");
    } else {
        st->top--;
    }
}

void isempty(struct stack st) {
    if (st.top == -1) {
        printf("Stack is empty\n");
    } else {
        printf("Stack is not empty\n");
    }
}

void isfull(struct stack st) {
    if (st.top == st.size - 1) {
        printf("Stack is full\n");
    } else {
        printf("Stack is not full\n");
    }
}

int main() {
    struct stack st;
    createstack(&st);

    int choice, x;
    while (1) {
        printf("1. Push\n");
        printf("2. Pop\n");
        printf("3. Display\n");
        printf("4. Check if Empty\n");
        printf("5. Check if Full\n");
        printf("6. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter the element to be pushed: ");
                scanf("%d", &x);
                push(&st, x);
                break;
            case 2:
                pop(&st);
                break;
            case 3:
                displaystack(st);
                break;
            case 4:
                isempty(st);
                break;
            case 5:
                isfull(st);
                break;
            case 6:
                free(st.s);
                return 0;
            default:
                printf("Invalid choice\n");
        }
    }
}