#include <stdio.h>
#include <stdlib.h>




struct BSTNode {
    int data;
    struct BSTNode *left;
    struct BSTNode *right;
};




void inorder(struct BSTNode *root) {
    if (root != NULL) {
        inorder(root->left);
        printf("%d ", root->data);
        inorder(root->right);
    }
}




void preorder(struct BSTNode *root) {
    if (root != NULL) {
        printf("%d ", root->data);
        preorder(root->left);
        preorder(root->right);
    }
}




void postorder(struct BSTNode *root) {
    if (root != NULL) {
        postorder(root->left);
        postorder(root->right);
        printf("%d ", root->data);
    }
}




struct BSTNode* search(struct BSTNode *root, int key) {
    if (root == NULL || root->data == key) {
        return root;
    }
    if (root->data < key) {
        return search(root->right, key);
    }
    return search(root->left, key);
}




struct BSTNode* findMinimum(struct BSTNode *root) {
    while (root->left != NULL) {
        root = root->left;
    }
    return root;
}




struct BSTNode* findMaximum(struct BSTNode *root) {
    while (root->right != NULL) {
        root = root->right;
    }
    return root;
}




struct BSTNode* insert(struct BSTNode *root, int element) {
    if (root == NULL) {
        root = (struct BSTNode *)malloc(sizeof(struct BSTNode));
        root->data = element;
        root->left = root->right = NULL;
    } else if (element <= root->data) {
        root->left = insert(root->left, element);
    } else {
        root->right = insert(root->right, element);
    }
    return root;
}




struct BSTNode* deletenode(struct BSTNode *root, int element) {
    if (root == NULL) {
        return root;
    }
    if (element < root->data) {
        root->left = deletenode(root->left, element);
    } else if (element > root->data) {
        root->right = deletenode(root->right, element);
    } else {
        if (root->left == NULL) {
            struct BSTNode *temp = root->right;
            free(root);
            return temp;
        } else if (root->right == NULL) {
            struct BSTNode *temp = root->left;
            free(root);
            return temp;
        }
        struct BSTNode *temp = findMinimum(root->right);
        root->data = temp->data;
        root->right = deletenode(root->right, temp->data);
    }
    return root;
}





int main() {
    struct BSTNode *root = NULL;
    int choice, element;

    while (1) {
        printf("\nMenu:\n");
        printf("1. Insert\n");
        printf("2. Delete\n");
        printf("3. Search\n");
        printf("4. Inorder Traversal\n");
        printf("5. Preorder Traversal\n");
        printf("6. Postorder Traversal\n");
        printf("7. Find Minimum\n");
        printf("8. Find Maximum\n");
        printf("9. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter element to insert: ");
                scanf("%d", &element);
                root = insert(root, element);
                break;


            case 2:
                printf("Enter element to delete: ");
                scanf("%d", &element);
                root = deletenode(root, element);
                break;


            case 3:
                printf("Enter element to search: ");
                scanf("%d", &element);
                struct BSTNode *temp = search(root, element);
                if (temp != NULL) {
                    printf("Element found: %d\n", temp->data);
                } else {
                    printf("Element not found\n");
                }
                break;


            case 4:
                printf("Inorder traversal: ");
                inorder(root);
                printf("\n");
                break;


            case 5:
                printf("Preorder traversal: ");
                preorder(root);
                printf("\n");
                break;


            case 6:
                printf("Postorder traversal: ");
                postorder(root);
                printf("\n");
                break;


            case 7:
                if (root != NULL) {
                    printf("Minimum element: %d\n", findMinimum(root)->data);
                } else {
                    printf("Tree is empty\n");
                }
                break;


            case 8:
                if (root != NULL) {
                    printf("Maximum element: %d\n", findMaximum(root)->data);
                } else {
                    printf("Tree is empty\n");
                }
                break;


            case 9:
                exit(0);
            default:
                printf("Invalid choice\n");
        }
    }
    return 0;
}


//TODO:Implement AVL tree from scratch using any language of your choice. 
//TODO : travelling Salesman Problem using GUI in python