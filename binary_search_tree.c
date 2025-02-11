#include <stdio.h>
#include <stdlib.h>

struct BSTNode {                  //node structure
    int data;
    struct BSTNode *left;
    struct BSTNode *right;
};


void inorder(struct BSTNode *root)                  //inorder traversal
{        
    if (root != NULL) {
        inorder(root->left);
        printf("%d ", root->data);
        inorder(root->right);
    }
}



void preorder(struct BSTNode *root)                  //preorder traversal
{
    if (root != NULL) {
        printf("%d ", root->data);
        preorder(root->left);
        preorder(root->right);
    }
}



void postorder(struct BSTNode *root)                  //postorder traversal
{
    if (root != NULL) {
        postorder(root->left);
        postorder(root->right);
        printf("%d ", root->data);
    }
}



