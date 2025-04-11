import tkinter as tk
from tkinter import simpledialog, messagebox

INF = float('inf')

class GraphGUI:
    def __init__(self, master):
        self.master = master
        master.title("Interactive Floyd–Warshall Visualization")
        
        # Modes: "add_node", "add_edge", "select_path", or None.
        self.mode = None  
        self.nodes = []      # Each node is a dict: {id, x, y, circle, label}
        self.edges = []      # Each edge is a dict: {src, dest, weight, line, weight_text}
        self.node_radius = 20
        self.selected_node = None  # Used for edge creation or path selection
        
        # To store results of Floyd–Warshall
        self.dist = None
        self.nxt = None

        # Set up the canvas.
        self.canvas = tk.Canvas(master, width=600, height=600, bg="white")
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.canvas_click)

        # Control panel on the right.
        self.control_frame = tk.Frame(master)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        self.add_node_button = tk.Button(self.control_frame, text="Add Node", width=20, font=("Arial", 12),
                                         command=self.set_mode_add_node)
        self.add_node_button.pack(pady=5)

        self.add_edge_button = tk.Button(self.control_frame, text="Add Edge", width=20, font=("Arial", 12),
                                         command=self.set_mode_add_edge)
        self.add_edge_button.pack(pady=5)

        self.run_button = tk.Button(self.control_frame, text="Run Warshall", width=20, font=("Arial", 12),
                                    command=self.run_warshall)
        self.run_button.pack(pady=5)

        self.select_path_button = tk.Button(self.control_frame, text="Select Path", width=20, font=("Arial", 12),
                                            command=self.set_mode_select_path)
        self.select_path_button.pack(pady=5)

        self.reset_button = tk.Button(self.control_frame, text="Reset Graph", width=20, font=("Arial", 12),
                                      command=self.reset_graph)
        self.reset_button.pack(pady=5)

        self.status_label = tk.Label(self.control_frame, text="Mode: None", font=("Arial", 12))
        self.status_label.pack(pady=10)

    def set_mode_add_node(self):
        self.mode = "add_node"
        self.selected_node = None
        self.status_label.config(text="Mode: Add Node (click canvas)")
        messagebox.showinfo("Mode", "Click anywhere on the canvas to add a node.")

    def set_mode_add_edge(self):
        if len(self.nodes) < 2:
            messagebox.showwarning("Warning", "At least 2 nodes are needed to add an edge.")
            return
        self.mode = "add_edge"
        self.selected_node = None
        self.status_label.config(text="Mode: Add Edge (click source node, then target node)")
        messagebox.showinfo("Mode", "Click on the source node, then the destination node to add an edge.")

    def set_mode_select_path(self):
        if self.dist is None or self.nxt is None:
            messagebox.showwarning("Warning", "Please run the Warshall algorithm first.")
            return
        if len(self.nodes) < 2:
            messagebox.showwarning("Warning", "At least 2 nodes are needed to select a path.")
            return
        self.mode = "select_path"
        self.selected_node = None
        self.status_label.config(text="Mode: Select Path (click source node, then destination node)")
        messagebox.showinfo("Mode", "Click on the source node, then the destination node to display the shortest path.")

    def canvas_click(self, event):
        if self.mode == "add_node":
            self.add_node(event.x, event.y)
        elif self.mode == "add_edge":
            self.process_add_edge(event.x, event.y)
        elif self.mode == "select_path":
            self.process_select_path(event.x, event.y)

    def add_node(self, x, y):
        node_id = len(self.nodes)
        r = self.node_radius
        # Draw node circle and label.
        circle = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="lightblue", outline="black", width=2)
        label = self.canvas.create_text(x, y, text=str(node_id), font=("Arial", 12, "bold"))
        self.nodes.append({"id": node_id, "x": x, "y": y, "circle": circle, "label": label})
        self.status_label.config(text=f"Added node {node_id}")

    def get_node_at_position(self, x, y):
        # Return node if click is within the circle.
        for node in self.nodes:
            dx = x - node["x"]
            dy = y - node["y"]
            if dx*dx + dy*dy <= self.node_radius*self.node_radius:
                return node
        return None

    def process_add_edge(self, x, y):
        node = self.get_node_at_position(x, y)
        if not node:
            return
        if self.selected_node is None:
            self.selected_node = node
            # Highlight source node.
            self.canvas.itemconfig(node["circle"], fill="yellow")
            self.status_label.config(text=f"Selected source node {node['id']} for edge")
        else:
            src = self.selected_node
            dest = node
            # Reset source highlight.
            self.canvas.itemconfig(src["circle"], fill="lightblue")
            if src["id"] == dest["id"]:
                messagebox.showwarning("Invalid Edge", "Cannot create an edge from a node to itself.")
                self.selected_node = None
                return
            # Ask for weight.
            weight = simpledialog.askfloat("Edge Weight", f"Enter weight for edge from {src['id']} to {dest['id']}:")
            if weight is None:
                self.selected_node = None
                return
            # Draw arrow for edge.
            line = self.canvas.create_line(src["x"], src["y"], dest["x"], dest["y"], arrow=tk.LAST, width=2, fill="black")
            mid_x = (src["x"] + dest["x"]) / 2
            mid_y = (src["y"] + dest["y"]) / 2
            weight_text = self.canvas.create_text(mid_x, mid_y, text=str(weight), font=("Arial", 12, "bold"), fill="red")
            self.edges.append({"src": src["id"], "dest": dest["id"], "weight": weight,
                               "line": line, "weight_text": weight_text})
            self.status_label.config(text=f"Added edge from {src['id']} to {dest['id']} (w={weight})")
            self.selected_node = None

    def run_warshall(self):
        if not self.nodes:
            messagebox.showwarning("Warning", "No nodes in the graph.")
            return
        n = len(self.nodes)
        # Initialize distance and next matrices.
        dist = [[INF] * n for _ in range(n)]
        nxt = [[None] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0
            nxt[i][i] = i
        # Set distances from edges.
        for edge in self.edges:
            i = edge["src"]
            j = edge["dest"]
            dist[i][j] = edge["weight"]
            nxt[i][j] = j

        # Run Floyd–Warshall.
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        nxt[i][j] = nxt[i][k]
                        
        self.dist = dist
        self.nxt = nxt
        self.mode = None
        self.selected_node = None
        self.status_label.config(text="Algorithm complete. Select path to view result.")
        messagebox.showinfo("Floyd–Warshall", "All pairs shortest paths computed.\nNow use 'Select Path' to display a path.")

    def process_select_path(self, x, y):
        node = self.get_node_at_position(x, y)
        if not node:
            return
        if self.selected_node is None:
            self.selected_node = node
            self.canvas.itemconfig(node["circle"], fill="yellow")
            self.status_label.config(text=f"Selected source node {node['id']} for path")
        else:
            src = self.selected_node
            dest = node
            self.canvas.itemconfig(src["circle"], fill="lightblue")
            self.selected_node = None
            self.display_path(src["id"], dest["id"])

    def display_path(self, src, dest):
        if self.dist is None or self.nxt is None:
            messagebox.showwarning("Warning", "Please run the Warshall algorithm first.")
            return
        if self.dist[src][dest] == INF:
            messagebox.showinfo("No Path", f"No path exists from {src} to {dest}.")
            return

        # Reconstruct path.
        path = [src]
        while src != dest:
            src = self.nxt[src][dest]
            path.append(src)
        self.highlight_path(path)
        messagebox.showinfo("Shortest Path", f"Shortest path: {' -> '.join(map(str, path))}\nTotal weight: {self.dist[path[0]][path[-1]]}")
        self.status_label.config(text="Path displayed. You can now add more nodes/edges or run again.")

    def highlight_path(self, path):
        # First, reset all highlights.
        self.reset_highlights()
        # Highlight nodes in the path.
        for node_id in path:
            self.canvas.itemconfig(self.nodes[node_id]["circle"], fill="orange")
        # Highlight edges in the path.
        for i in range(len(path) - 1):
            src, dest = path[i], path[i+1]
            for edge in self.edges:
                if edge["src"] == src and edge["dest"] == dest:
                    self.canvas.itemconfig(edge["line"], fill="green", width=4)
                    break

    def reset_highlights(self):
        # Reset all node and edge colors to default.
        for node in self.nodes:
            self.canvas.itemconfig(node["circle"], fill="lightblue")
        for edge in self.edges:
            self.canvas.itemconfig(edge["line"], fill="black", width=2)

    def reset_graph(self):
        self.canvas.delete("all")
        self.nodes.clear()
        self.edges.clear()
        self.mode = None
        self.selected_node = None
        self.dist = None
        self.nxt = None
        self.status_label.config(text="Mode: None")
        messagebox.showinfo("Reset", "Graph cleared. You can start building a new graph.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphGUI(root)
    root.mainloop()
