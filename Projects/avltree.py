import tkinter as tk
from tkinter import messagebox, ttk
import json
import math

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
        self.window.geometry("1200x800")
        
        # Theme
        self.dark_mode = False
        self.colors = {
            'balanced': '#90EE90',      # Light green
            'unbalanced': '#FF6347',    # Tomato red
            'bg': '#F5F5F5',            # Light gray
            'text': '#000000',          # Black (adjusted dynamically)
            'highlight': '#FFFF99',     # Light yellow
            'outline_unbalanced': '#FF0000',  # Red
            'branch': '#555555'         # Gray
        }
        
        # Zoom factor
        self.zoom_factor = 1.0
        
        # Main frames
        self.canvas_frame = ttk.Frame(self.window)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.canvas = tk.Canvas(self.canvas_frame, width=900, height=600, bg="white", highlightthickness=1, highlightbackground="#CCCCCC")
        self.hsb = tk.Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
        self.vsb = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.hsb.set, yscrollcommand=self.vsb.set)
        self.hsb.pack(side="bottom", fill="x")
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.control_frame = ttk.Frame(self.window)
        self.control_frame.pack(pady=10, fill=tk.X, padx=10)
        
        self.info_frame = ttk.Frame(self.window)
        self.info_frame.pack(pady=10, padx=10, fill=tk.Y)
        
        # Controls
        ttk.Label(self.control_frame, text="Value:").grid(row=0, column=0, padx=5, pady=5)
        self.entry = ttk.Entry(self.control_frame, width=10)
        self.entry.grid(row=0, column=1, padx=5, pady=5)
        
        buttons = [
            ("Insert", self.insert_value, "#4CAF50"),
            ("Delete", self.delete_value, "#F44336"),
            ("Search", self.search_value, "#2196F3"),
            ("Reset", self.reset_tree, "#9E9E9E"),
            ("Save", self.save_tree, "#2196F3"),
            ("Load", self.load_tree, "#2196F3"),
            ("Toggle Theme", self.toggle_theme, "#607D8B")
        ]
        for i, (text, cmd, color) in enumerate(buttons):
            ttk.Button(self.control_frame, text=text, command=cmd).grid(row=0, column=i+2, padx=5, pady=5)
        
        # Zoom buttons
        ttk.Button(self.control_frame, text="Zoom In", command=self.zoom_in).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(self.control_frame, text="Zoom Out", command=self.zoom_out).grid(row=1, column=1, padx=5, pady=5)
        
        # Traversal buttons
        ttk.Button(self.control_frame, text="In-Order", command=self.start_inorder_traversal).grid(row=1, column=2, padx=5, pady=5)
        ttk.Button(self.control_frame, text="Pre-Order", command=self.start_preorder_traversal).grid(row=1, column=3, padx=5, pady=5)
        ttk.Button(self.control_frame, text="Post-Order", command=self.start_postorder_traversal).grid(row=1, column=4, padx=5, pady=5)
        
        # Info display
        self.traversal_var = tk.StringVar()
        ttk.Label(self.info_frame, text="Traversals:").pack(pady=5)
        ttk.Label(self.info_frame, textvariable=self.traversal_var, wraplength=300).pack(pady=5)
        
        self.step_var = tk.StringVar()
        ttk.Label(self.info_frame, text="Balancing Steps:").pack(pady=5)
        self.step_label = ttk.Label(self.info_frame, textvariable=self.step_var, wraplength=300, justify=tk.LEFT)
        self.step_label.pack(pady=5)
        
        # Bindings
        self.window.bind('<Return>', lambda e: self.insert_value())
        self.window.bind('<Delete>', lambda e: self.delete_value())
        self.window.bind('<Control-s>', lambda e: self.save_tree())
        self.canvas.bind("<Button-1>", self.on_node_click)
        self.canvas.bind("<Button-3>", self.on_node_right_click)
        self.canvas.bind("<Motion>", self.on_node_hover)
        self.canvas.bind("<Leave>", self.on_canvas_leave)
        
        # Initial state
        self.positions = {}
        self.current_hover = None
        self.redraw_tree()

    ### Tree Operations
    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def update_height(self, node):
        if node:
            node.height = max(self.get_height(node.left), self.get_height(node.right)) + 1

    def right_rotate(self, y):
        self.steps.append(f"🌟 Right Rotation at {y.value}")
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self.update_height(y)
        self.update_height(x)
        return x

    def left_rotate(self, x):
        self.steps.append(f"🌟 Left Rotation at {x.value}")
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
        if balance > 1:
            if value < root.left.value:
                return self.right_rotate(root)
            else:
                root.left = self.left_rotate(root.left)
                return self.right_rotate(root)
        if balance < -1:
            if value > root.right.value:
                return self.left_rotate(root)
            else:
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
        if balance > 1:
            if self.get_balance(root.left) >= 0:
                return self.right_rotate(root)
            else:
                root.left = self.left_rotate(root.left)
                return self.right_rotate(root)
        if balance < -1:
            if self.get_balance(root.right) <= 0:
                return self.left_rotate(root)
            else:
                root.right = self.right_rotate(root.right)
                return self.left_rotate(root)
        return root

    def search(self, root, value):
        if not root or root.value == value:
            return root
        if value < root.value:
            return self.search(root.left, value)
        return self.search(root.right, value)

    ### Visualization
    def calculate_positions(self, node, x, y, x_dist):
        positions = {}
        if node:
            positions[node] = (x, y)
            if node.left:
                positions.update(self.calculate_positions(node.left, x - x_dist, y + 80, x_dist / 2))
            if node.right:
                positions.update(self.calculate_positions(node.right, x + x_dist, y + 80, x_dist / 2))
        return positions

    def draw_tree_with_positions(self, positions, highlight=None):
        self.canvas.delete("all")
        for node, (x, y) in positions.items():
            # Shadow
            self.canvas.create_oval(x - 17.5 + 2, y - 17.5 + 2, x + 17.5 + 2, y + 17.5 + 2, fill='#CCCCCC', outline='')
            # Base color
            base_color = self.colors['highlight'] if node.value == highlight else \
                        self.colors['unbalanced'] if abs(self.get_balance(node)) > 1 else self.colors['balanced']
            # Gradient
            for i in range(5):
                r = 17.5 - i * 2
                color = f'#{int(int(base_color[1:3], 16) * (1 - i/10)):02x}' \
                        f'{int(int(base_color[3:5], 16) * (1 - i/10)):02x}' \
                        f'{int(int(base_color[5:], 16) * (1 - i/10)):02x}'
                self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline='')
            # Outline
            outline = self.colors['outline_unbalanced'] if abs(self.get_balance(node)) > 1 else self.colors['text']
            self.canvas.create_oval(x - 17.5, y - 17.5, x + 17.5, y + 17.5, outline=outline, width=2)
            # Text
            text_color = '#000000' if self.dark_mode else '#FFFFFF'
            self.canvas.create_text(x, y, text=str(node.value), fill=text_color, font=("Helvetica", 10, "bold"))
        # Branches
        for node, (x, y) in positions.items():
            if node.left and node.left in positions:
                lx, ly = positions[node.left]
                self.canvas.create_line(x, y + 17.5, lx, ly - 17.5, fill=self.colors['branch'], width=1)
            if node.right and node.right in positions:
                rx, ry = positions[node.right]
                self.canvas.create_line(x, y + 17.5, rx, ry - 17.5, fill=self.colors['branch'], width=1)
        # Scrollregion
        if positions:
            min_x = min(pos[0] for pos in positions.values()) - 50
            max_x = max(pos[0] for pos in positions.values()) + 50
            min_y = min(pos[1] for pos in positions.values()) - 50
            max_y = max(pos[1] for pos in positions.values()) + 50
            self.canvas.config(scrollregion=(min_x, min_y, max_x, max_y))

    def redraw_tree(self):
        unscaled_positions = self.calculate_positions(self.root, 400, 50, 200)
        self.positions = {node: (x * self.zoom_factor, y * self.zoom_factor) for node, (x, y) in unscaled_positions.items()}
        self.draw_tree_with_positions(self.positions)

    def animate_tree(self, current_positions, target_positions, steps=10):
        current_scaled = {node: (x * self.zoom_factor, y * self.zoom_factor) for node, (x, y) in current_positions.items()}
        target_scaled = {node: (x * self.zoom_factor, y * self.zoom_factor) for node, (x, y) in target_positions.items()}
        drawing_nodes = set(target_scaled.keys())
        deleted_nodes = set(current_scaled.keys()) - set(target_scaled.keys())
        
        def interpolate(step):
            animated_positions = {}
            for node in drawing_nodes:
                if node in current_scaled:
                    cx, cy = current_scaled[node]
                    tx, ty = target_scaled[node]
                    ax = cx + (tx - cx) * step / steps
                    ay = cy + (ty - cy) * step / steps
                    animated_positions[node] = (ax, ay)
                else:
                    animated_positions[node] = target_scaled[node]
            for node in deleted_nodes:
                animated_positions[node] = current_scaled[node]
            self.draw_tree_with_positions(animated_positions)
            if step < steps:
                self.window.after(50, interpolate, step + 1)
            else:
                self.positions = target_scaled
                self.draw_tree_with_positions(target_scaled)
        
        interpolate(1)

    ### User Actions
    def insert_value(self):
        try:
            value = int(self.entry.get())
            self.steps = []
            current_positions = self.calculate_positions(self.root, 400, 50, 200)
            self.root = self.insert(self.root, value)
            target_positions = self.calculate_positions(self.root, 400, 50, 200)
            self.animate_tree(current_positions, target_positions)
            self.step_var.set("\n".join(self.steps) if self.steps else "No balancing needed!")
            self.update_traversals()
            self.entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer")

    def delete_value(self):
        try:
            value = int(self.entry.get())
            self.steps = []
            if self.search(self.root, value):
                current_positions = self.calculate_positions(self.root, 400, 50, 200)
                self.root = self.delete(self.root, value)
                target_positions = self.calculate_positions(self.root, 400, 50, 200)
                self.animate_tree(current_positions, target_positions)
                self.step_var.set("\n".join(self.steps) if self.steps else "Deletion complete!")
                self.update_traversals()
            else:
                self.step_var.set(f"🔍 Value {value} not found!")
            self.entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer")

    def search_value(self):
        try:
            value = int(self.entry.get())
            result = self.search(self.root, value)
            self.redraw_tree()
            if result:
                self.draw_tree_with_positions(self.positions, highlight=value)
                messagebox.showinfo("Search", f"Value {value} found!")
            else:
                messagebox.showinfo("Search", f"Value {value} not found!")
            self.entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer")

    def reset_tree(self):
        self.root = None
        self.steps = []
        self.canvas.delete("all")
        self.step_var.set("Tree reset!")
        self.traversal_var.set("")

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.colors = {
                'balanced': '#4CAF50', 'unbalanced': '#F44336', 'bg': '#212121',
                'text': '#FFFFFF', 'highlight': '#FFFF99', 'outline_unbalanced': '#FF0000',
                'branch': '#A0A0A0'
            }
            self.canvas.configure(bg='#333333')
        else:
            self.colors = {
                'balanced': '#90EE90', 'unbalanced': '#FF6347', 'bg': '#F5F5F5',
                'text': '#000000', 'highlight': '#FFFF99', 'outline_unbalanced': '#FF0000',
                'branch': '#555555'
            }
            self.canvas.configure(bg='white')
        self.window.configure(bg=self.colors['bg'])
        self.redraw_tree()

    ### Interactive Features
    def on_node_click(self, event):
        x, y = event.x, event.y
        for node, (nx, ny) in self.positions.items():
            if math.sqrt((x - nx)**2 + (y - ny)**2) <= 17.5:
                self.highlight_node(node)
                break

    def highlight_node(self, node):
        self.draw_tree_with_positions(self.positions, highlight=node.value)
        messagebox.showinfo("Node Info", f"Value: {node.value}\nBalance: {self.get_balance(node)}")

    def on_node_right_click(self, event):
        x, y = event.x, event.y
        for node, (nx, ny) in self.positions.items():
            if math.sqrt((x - nx)**2 + (y - ny)**2) <= 17.5:
                self.show_node_menu(node, event.x_root, event.y_root)
                break

    def show_node_menu(self, node, x, y):
        menu = tk.Menu(self.window, tearoff=0)
        menu.add_command(label="Delete Node", command=lambda: self.delete_node(node))
        menu.tk_popup(x, y)

    def delete_node(self, node):
        self.steps = []
        current_positions = self.calculate_positions(self.root, 400, 50, 200)
        self.root = self.delete(self.root, node.value)
        target_positions = self.calculate_positions(self.root, 400, 50, 200)
        self.animate_tree(current_positions, target_positions)
        self.step_var.set("\n".join(self.steps) if self.steps else "Deletion complete!")
        self.update_traversals()

    def on_node_hover(self, event):
        x, y = event.x, event.y
        for node, (nx, ny) in self.positions.items():
            if math.sqrt((x - nx)**2 + (y - ny)**2) <= 17.5:
                if self.current_hover != node:
                    self.current_hover = node
                    self.draw_tree_with_positions(self.positions, highlight=node.value)
                break
        else:
            if self.current_hover is not None:
                self.current_hover = None
                self.draw_tree_with_positions(self.positions)

    def on_canvas_leave(self, event):
        if self.current_hover is not None:
            self.current_hover = None
            self.draw_tree_with_positions(self.positions)

    ### Traversals
    def inorder(self, root, result=[]):
        if root:
            self.inorder(root.left, result)
            result.append(root)
            self.inorder(root.right, result)
        return result

    def preorder(self, root, result=[]):
        if root:
            result.append(root)
            self.preorder(root.left, result)
            self.preorder(root.right, result)
        return result

    def postorder(self, root, result=[]):
        if root:
            self.postorder(root.left, result)
            self.postorder(root.right, result)
            result.append(root)
        return result

    def update_traversals(self):
        if self.root:
            ino = "Inorder: " + " ".join(str(node.value) for node in self.inorder(self.root))
            pre = "Preorder: " + " ".join(str(node.value) for node in self.preorder(self.root))
            post = "Postorder: " + " ".join(str(node.value) for node in self.postorder(self.root))
            self.traversal_var.set(f"{ino}\n{pre}\n{post}")
        else:
            self.traversal_var.set("Tree is empty")

    def start_inorder_traversal(self):
        if not self.root:
            messagebox.showwarning("Warning", "Tree is empty!")
            return
        self.animate_traversal(self.inorder(self.root))

    def start_preorder_traversal(self):
        if not self.root:
            messagebox.showwarning("Warning", "Tree is empty!")
            return
        self.animate_traversal(self.preorder(self.root))

    def start_postorder_traversal(self):
        if not self.root:
            messagebox.showwarning("Warning", "Tree is empty!")
            return
        self.animate_traversal(self.postorder(self.root))

    def animate_traversal(self, traversal, index=0):
        if index < len(traversal):
            node = traversal[index]
            self.draw_tree_with_positions(self.positions, highlight=node.value)
            self.window.after(500, self.animate_traversal, traversal, index + 1)
        else:
            self.draw_tree_with_positions(self.positions)

    ### Zoom
    def zoom_in(self):
        if self.zoom_factor < 3.0:
            self.zoom_factor *= 1.2
            self.redraw_tree()

    def zoom_out(self):
        if self.zoom_factor > 0.3:
            self.zoom_factor /= 1.2
            self.redraw_tree()

    ### Save/Load
    def tree_to_dict(self, node):
        if not node:
            return None
        return {'value': node.value, 'left': self.tree_to_dict(node.left), 'right': self.tree_to_dict(node.right)}

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
            self.redraw_tree()
            self.update_traversals()
            messagebox.showinfo("Load", "Tree loaded successfully!")
        except FileNotFoundError:
            messagebox.showerror("Error", "No saved tree found!")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading tree: {str(e)}")

    def run(self):
        self.window.configure(bg=self.colors['bg'])
        self.window.mainloop()

if __name__ == "__main__":
    visualizer = AVLTreeVisualizer()
    visualizer.run()