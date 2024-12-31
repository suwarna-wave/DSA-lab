#include <stdio.h>
#define MAX 5

struct CircularQueue 
{
    int front, rear;
    int items[MAX];
};

typedef struct CircularQueue CQ;

void enqueue (CQ *q, int element)
{
    if ((q->rear + 1) % MAX == q->front)
    
        printf("Queue is full\n");
    else
    {q->rear = (q->rear + 1) % MAX;
    q->items[q->rear] = element;
    printf("Enqueued %d\n", element);
    }
    
}

int dequeue (CQ *q)
{
    if (q->front == q->rear)
    {
        printf("Queue is empty\n");
        return -1;
    }
    else
    {
        q->front = (q->front + 1) % MAX;
        return q->items[q->front];
    }
}

int main() {
    CQ queue = {0, 0}; 
    int choice, element;

    while (1) {
        printf("\nCircular Queue Operations:\n");
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