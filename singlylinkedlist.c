#include<stdio.h>
#include<stdlib.h>

// Structure for a node in singly linked list
struct Node {
    int data;
    struct Node *next;
};
struct Node *first = NULL;


// Function to create a new node
void create (struct Node **first, int A[], int n)
{
    struct Node *t, *last;
    *first = (struct Node *)malloc(sizeof(struct Node));
    (*first)->data = A[0];
    (*first)->next = NULL;
    last = *first;

    for (int i = 1; i < n; i++)
    {
        t = (struct Node *)malloc(sizeof(struct Node));
        t->data = A[i];
        t->next = NULL;
        last->next = t;
        last = t;
    }
}


//function t0 display the linked list
void display(struct Node *p)
{
    while (p != NULL)
    {
        printf("%d ", p->data);
        p = p->next;
    }
}





//main function
int main ()
{ 
    int A[] = {3,5,7,10,15};
    create(&first, A, 5);
    display(first);
    display(first);
    return 0;

}