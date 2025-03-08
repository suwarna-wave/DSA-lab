import tkinter as tk
from tkinter import messagebox, ttk
import time
import json

class AVLNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

class AVLTreeVisualizer:
    def __init__(self):
        # Window setup
        self.root = None
        self.window = tk.Tk()
        self.window.title("AVL Tree Visualizer")
        self.window.geometry("1000x700")
        
        # Theme
        self.dark_mode = False
        self.colors = {
            'balanced': '#90EE90',
            'unbalanced': '#FFB6C1',
            'bg': '#FFFFFF',
            'text': '#000000'
        }
        
        # Main frames
        self.canvas_frame = tk.Frame(self.window)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.canvas_frame, width=800, height=500)
        self.canvas.pack(pady=10)
        
        self.control_frame = tk.Frame(self.window)
        self.control_frame.pack(pady=10)
        
        self.info_frame = tk.Frame(self.window)
        self.info_frame.pack(pady=10)
        
        # Controls
        self.entry = tk.Entry(self.control_frame, width=10)
        self.entry.grid(row=0, column=0, padx=5)
        
        buttons = [
            ("Insert", self.insert_value),
            ("Delete", self.delete_value),
            ("Search", self.search_value),
            ("Reset", self.reset_tree),
            ("Save", self.save_tree),
            ("Load", self.load_tree),
            ("Toggle Theme", self.toggle_theme)
        ]
        
        for i, (text, cmd) in enumerate(buttons):
            tk.Button(self.control_frame, text=text, command=cmd).grid(row=0, column=i+1, padx=5)
        
        # Traversal display
        self.traversal_var = tk.StringVar()
        tk.Label(self.info_frame, text="Traversals:").pack()
        tk.Label(self.info_frame, textvariable=self.traversal_var).pack()
        
        # Keyboard bindings
        self.window.bind('<Return>', lambda e: self.insert_value())
        self.window.bind('<Delete>', lambda e: self.delete_value())
        self.window.bind('<Control-s>', lambda e: self.save_tree())
        
    # Tree Operations
    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def update_height(self, node):
        node.height = max(self.get_height(node.left), self.get_height(node.right)) + 1

    def right_rotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self.update_height(y)
        self.update_height(x)
        return x

    def left_rotate(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self.update_height(x)
        self.update_height(y)
        return y

    def insert(self, root, value):
        if not root:
            return AVLNode(value)
            
        if value < root.value:
            root.left = self.insert(root.left, value)
        elif value > root.value:
            root.right = self.insert(root.right, value)
        else:
            return root
            
        self.update_height(root)
        balance = self.get_balance(root)
        
        # Left Left
        if balance > 1 and value < root.left.value:
            return self.right_rotate(root)
            
        # Right Right
        if balance < -1 and value > root.right.value:
            return self.left_rotate(root)
            
        # Left Right
        if balance > 1 and value > root.left.value:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
            
        # Right Left
        if balance < -1 and value < root.right.value:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)
            
        return root

    def min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def delete(self, root, value):
        if not root:
            return root
            
        if value < root.value:
            root.left = self.delete(root.left, value)
        elif value > root.value:
            root.right = self.delete(root.right, value)
        else:
            if not root.left:
                return root.right
            elif not root.right:
                return root.left
                
            temp = self.min_value_node(root.right)
            root.value = temp.value
            root.right = self.delete(root.right, temp.value)
            
        if not root:
            return root
            
        self.update_height(root)
        balance = self.get_balance(root)
        
        # Left Left
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)
            
        # Left Right
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
            
        # Right Right
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)
            
        # Right Left
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)
            
        return root

    def search(self, root, value):
        if not root or root.value == value:
            return root
        if value < root.value:
            return self.search(root.left, value)
        return self.search(root.right, value)

    # Visualization
    def draw_tree(self, node, x, y, x_dist, animation=False):
        if not node:
            return
            
        color = self.colors['balanced'] if abs(self.get_balance(node)) <= 1 else self.colors['unbalanced']
        node_id = self.canvas.create_oval(x-15, y-15, x+15, y+15, fill=color)
        text_id = self.canvas.create_text(x, y, text=str(node.value), fill=self.colors['text'])
        
        if animation:
            self.canvas.update()
            time.sleep(0.1)
            
        if node.left:
            self.canvas.create_line(x, y+15, x-x_dist, y+75, fill=self.colors['text'])
            self.draw_tree(node.left, x-x_dist, y+80, x_dist/2, animation)
            
        if node.right:
            self.canvas.create_line(x, y+15, x+x_dist, y+75, fill=self.colors['text'])
            self.draw_tree(node.right, x+x_dist, y+80, x_dist/2, animation)

    # Traversals
    def inorder(self, root, result=[]):
        if root:
            self.inorder(root.left, result)
            result.append(str(root.value))
            self.inorder(root.right, result)
        return result

    def preorder(self, root, result=[]):
        if root:
            result.append(str(root.value))
            self.preorder(root.left, result)
            self.preorder(root.right, result)
        return result

    def postorder(self, root, result=[]):
        if root:
            self.postorder(root.left, result)
            self.postorder(root.right, result)
            result.append(str(root.value))
        return result

    def update_traversals(self):
        ino = "Inorder: " + " ".join(self.inorder(self.root))
        pre = "Preorder: " + " ".join(self.preorder(self.root))
        post = "Postorder: " + " ".join(self.postorder(self.root))
        self.traversal_var.set(f"{ino}\n{pre}\n{post}")

    # User Actions
    def insert_value(self):
        try:
            value = int(self.entry.get())
            self.root = self.insert(self.root, value)
            self.canvas.delete("all")
            self.draw_tree(self.root, 400, 50, 200, animation=True)
            self.update_traversals()
            self.entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer")

    def delete_value(self):
        try:
            value = int(self.entry.get())
            self.root = self.delete(self.root, value)
            self.canvas.delete("all")
            self.draw_tree(self.root, 400, 50, 200, animation=True)
            self.update_traversals()
            self.entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer")

    def search_value(self):
        try:
            value = int(self.entry.get())
            result = self.search(self.root, value)
            self.canvas.delete("all")
            self.draw_tree(self.root, 400, 50, 200)
            if result:
                messagebox.showinfo("Search", f"Value {value} found in tree!")
            else:
                messagebox.showinfo("Search", f"Value {value} not found in tree!")
            self.entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer")

    def reset_tree(self):
        self.root = None
        self.canvas.delete("all")
        self.traversal_var.set("")

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.colors = {
                'balanced': '#4CAF50',
                'unbalanced': '#F44336',
                'bg': '#212121',
                'text': '#FFFFFF'
            }
        else:
            self.colors = {
                'balanced': '#90EE90',
                'unbalanced': '#FFB6C1',
                'bg': '#FFFFFF',
                'text': '#000000'
            }
        self.window.configure(bg=self.colors['bg'])
        self.canvas.configure(bg=self.colors['bg'])
        self.canvas.delete("all")
        self.draw_tree(self.root, 400, 50, 200)

    # Save/Load
    def tree_to_dict(self, node):
        if not node:
            return None
        return {
            'value': node.value,
            'left': self.tree_to_dict(node.left),
            'right': self.tree_to_dict(node.right)
        }

    def dict_to_tree(self, data):
        if not data:
            return None
        node = AVLNode(data['value'])
        node.left = self.dict_to_tree(data.get('left'))
        node.right = self.dict_to_tree(data.get('right'))
        self.update_height(node)
        return node

    def save_tree(self):
        if not self.root:
            messagebox.showwarning("Warning", "Tree is empty!")
            return
        with open("avl_tree.json", "w") as f:
            json.dump(self.tree_to_dict(self.root), f)
        messagebox.showinfo("Save", "Tree saved successfully!")

    def load_tree(self):
        try:
            with open("avl_tree.json", "r") as f:
                data = json.load(f)
            self.root = self.dict_to_tree(data)
            self.canvas.delete("all")
            self.draw_tree(self.root, 400, 50, 200)
            self.update_traversals()
            messagebox.showinfo("Load", "Tree loaded successfully!")
        except FileNotFoundError:
            messagebox.showerror("Error", "No saved tree found!")
        except:
            messagebox.showerror("Error", "Error loading tree!")

    def run(self):
        self.window.configure(bg=self.colors['bg'])
        self.canvas.configure(bg=self.colors['bg'])
        self.window.mainloop()

if __name__ == "__main__":
    visualizer = AVLTreeVisualizer()
    visualizer.run()