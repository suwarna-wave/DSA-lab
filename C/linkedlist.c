#include <stdio.h>
#include <stdlib.h>

// Structure for a node in doubly linked list
struct Node {
    int data;
    struct Node* prev;
    struct Node* next;
};

// Function to create a new node
struct Node* createNode(int data) {
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->data = data;
    newNode->prev = NULL;
    newNode->next = NULL;
    return newNode;
}

// Function to insert at the beginning
struct Node* insertAtBeginning(struct Node* head, int data) {
    struct Node* newNode = createNode(data);
    if (head == NULL) {
        return newNode;
    }
    newNode->next = head;
    head->prev = newNode;
    return newNode;
}

// Function to insert at the end
struct Node* insertAtEnd(struct Node* head, int data) {
    struct Node* newNode = createNode(data);
    if (head == NULL) {
        return newNode;
    }
    struct Node* temp = head;
    while (temp->next != NULL) {
        temp = temp->next;
    }
    temp->next = newNode;
    newNode->prev = temp;
    return head;
}

// Function to delete a node with given data
struct Node* deleteNode(struct Node* head, int data) {
    if (head == NULL) return NULL;
    
    struct Node* temp = head;
    
    // If head node itself holds the data
    if (temp->data == data) {
        head = temp->next;
        if (head != NULL) {
            head->prev = NULL;
        }
        free(temp);
        return head;
    }
    
    while (temp != NULL && temp->data != data) {
        temp = temp->next;
    }
    
    if (temp == NULL) return head;
    
    if (temp->next != NULL) {
        temp->next->prev = temp->prev;
    }
    temp->prev->next = temp->next;
    free(temp);
    return head;
}

// Function to display the list forward
void displayForward(struct Node* head) {
    struct Node* temp = head;
    printf("\nForward Display: ");
    while (temp != NULL) {
        printf("%d ", temp->data);
        temp = temp->next;
    }
}

// Function to display the list backward
void displayBackward(struct Node* head) {
    struct Node* temp = head;
    if (temp == NULL) return;
    
    // Go to last node
    while (temp->next != NULL) {
        temp = temp->next;
    }
    
    printf("\nBackward Display: ");
    while (temp != NULL) {
        printf("%d ", temp->data);
        temp = temp->prev;
    }
}

// Main function for testing
int main() {
    struct Node* head = NULL;
    
    // Insert some elements
    head = insertAtEnd(head, 10);
    head = insertAtEnd(head, 20);
    head = insertAtBeginning(head, 5);
    head = insertAtEnd(head, 30);
    
    // Display the list
    displayForward(head);
    displayBackward(head);
    
    // Delete a node
    head = deleteNode(head, 20);
    
    printf("\n\nAfter deleting 20:");
    displayForward(head);
    displayBackward(head);
    
    return 0;
}