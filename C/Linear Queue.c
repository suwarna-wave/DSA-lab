#include <stdio.h>
#define MAX 5

struct LinearQueue {
    int front, rear;
    int items[MAX];
};

typedef struct LinearQueue LQ;

void enqueue(LQ *q, int element) {
    if (q->rear == MAX - 1) {
        printf("Queue is full\n");
    } else {
        if (q->front == -1) // Initialize front if inserting the first element
            q->front = 0;
        q->rear++;
        q->items[q->rear] = element;
        printf("Enqueued %d\n", element);
    }
}

int dequeue(LQ *q) {
    if (q->front == -1 || q->front > q->rear) {
        printf("Queue is empty\n");
        return -1;
    } else {
        int element = q->items[q->front];
        q->front++;
        return element;
    }
}

int main() {
    LQ queue = {-1, -1}; // Initialize front and rear to -1
    int choice, element;

    while (1) {
        printf("\nLinear Queue Operations:\n");
        printf("1. Enqueue\n");
        printf("2. Dequeue\n");
        printf("3. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter the element to enqueue: ");
                scanf("%d", &element);
                enqueue(&queue, element);
                break;
            case 2:
                element = dequeue(&queue);
                if (element != -1) {
                    printf("Dequeued element: %d\n", element);
                }
                break;
            case 3:
                printf("Exiting program. Goodbye!\n");
                return 0;
            default:
                printf("Invalid choice. Please try again.\n");
        }
    }

    return 0;
}
