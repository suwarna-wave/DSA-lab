#include <stdio.h>
#include <stdlib.h>


// Define the node structure for singly linked list
struct Node {
    int data;
    struct Node* next;
};



// Function to create a new node
struct Node* createNode(int data) {
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    if (newNode == NULL) {
        printf("Memory allocation failed!\n");
        exit(1);
    }
    newNode->data = data;
    newNode->next = NULL;
    return newNode;
}



// Function to insert a node at the beginning of the list
void insertAtBeginning(struct Node** head, int data) {
    struct Node* newNode = createNode(data);
    newNode->next = *head;
    *head = newNode;
    printf("Inserted %d at the beginning\n", data);
}



// Function to insert a node at the end of the list
void insertAtEnd(struct Node** head, int data) {
    struct Node* newNode = createNode(data);
    if (*head == NULL) {
        *head = newNode;
        printf("Inserted %d at the end\n", data);
        return;
    }
    struct Node* temp = *head;
    while (temp->next != NULL) {
        temp = temp->next;
    }
    temp->next = newNode;
    printf("Inserted %d at the end\n", data);
}



// Function to insert a node at a given position
void insertAtPosition(struct Node** head, int data, int position) {
    struct Node* newNode = createNode(data);
    if (position == 1) {
        newNode->next = *head;
        *head = newNode;
        printf("Inserted %d at position %d\n", data, position);
        return;
    }
    struct Node* temp = *head;
    for (int i = 1; i < position - 1 && temp != NULL; i++) {
        temp = temp->next;
    }
    if (temp == NULL) {
        printf("Position %d doesn't exist\n", position);
        free(newNode);
        return;
    }
    newNode->next = temp->next;
    temp->next = newNode;
    printf("Inserted %d at position %d\n", data, position);
}



// Function to delete a node with a given key
void deleteNode(struct Node** head, int key) {
    struct Node* temp = *head;
    struct Node* prev = NULL;

    if (temp != NULL && temp->data == key) {
        *head = temp->next;
        free(temp);
        printf("Deleted node with key %d\n", key);
        return;
    }

    while (temp != NULL && temp->data != key) {
        prev = temp;
        temp = temp->next;
    }

    if (temp == NULL) {
        printf("Node with key %d not found\n", key);
        return;
    }

    prev->next = temp->next;
    free(temp);
    printf("Deleted node with key %d\n", key);
}



// Function to search for a node with a given key
int searchNode(struct Node* head, int key) {
    struct Node* temp = head;
    int position = 1;
    while (temp != NULL) {
        if (temp->data == key) {
            printf("Element %d is available at position %d\n", key, position);
            return position;
        }
        temp = temp->next;
        position++;
    }
    printf("Element %d is not available in the list\n", key);
    return -1;
}



// Function to print the linked list
void printList(struct Node* head) {
    struct Node* temp = head;
    while (temp != NULL) {
        printf("%d -> ", temp->data);
        temp = temp->next;
    }
    printf("NULL\n");
}



// Function to free the entire linked list
void freeList(struct Node** head) {
    struct Node* temp;
    while (*head != NULL) {
        temp = *head;
        *head = (*head)->next;
        free(temp);
    }
}



int main() {
    struct Node* head = NULL;

    insertAtBeginning(&head, 100);
    insertAtBeginning(&head, 200);
    insertAtEnd(&head, 1000);
    insertAtEnd(&head, 2000);
    printf("Linked List: ");
    printList(head);
    insertAtPosition(&head, 150, 4);

    printf("Linked List: ");
    printList(head);

    // Search for a node
    searchNode(head, 1000);
    searchNode(head, 3000);
    searchNode(head, 100);

    // Delete nodes one by one
    while (head != NULL) {
        deleteNode(&head, head->data);
        printf("Linked List after deletion: ");
        printList(head);
    }

    return 0;
}