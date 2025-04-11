import tkinter as tk
from tkinter import simpledialog, messagebox

class GraphGUI:
    def __init__(self, master):
        self.master = master
        master.title("Floyd–Warshall Algorithm Visualization")

        # Mode can be "add_node", "add_edge", or "select_path"
        self.mode = None  
        self.nodes = []      # List of nodes: each node is a dict with id, x, y, and canvas items.
        self.edges = []      # List of edges: each edge is a dict with src, dest, weight, and canvas items.
        self.node_radius = 20
        self.selected_node = None  # Used in edge creation and path selection.

        # Containers
        self.canvas = tk.Canvas(master, width=600, height=600, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.canvas_click)

        self.control_frame = tk.Frame(master)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # Buttons for different modes and actions.
        self.add_node_button = tk.Button(self.control_frame, text="Add Node", font=("Arial", 12),
                                         command=self.set_mode_add_node, width=20)
        self.add_node_button.pack(pady=5)

        self.add_edge_button = tk.Button(self.control_frame, text="Add Edge", font=("Arial", 12),
                                         command=self.set_mode_add_edge, width=20)
        self.add_edge_button.pack(pady=5)

        self.select_path_button = tk.Button(self.control_frame, text="Select Path", font=("Arial", 12),
                                            command=self.set_mode_select_path, width=20)
        self.select_path_button.pack(pady=5)

        self.run_fw_button = tk.Button(self.control_frame, text="Run Floyd–Warshall", font=("Arial", 12),
                                       command=self.run_floyd_warshall, width=20)
        self.run_fw_button.pack(pady=5)

        self.reset_button = tk.Button(self.control_frame, text="Reset Graph", font=("Arial", 12),
                                      command=self.reset_graph, width=20)
        self.reset_button.pack(pady=5)

        # Storage for the results from Floyd–Warshall.
        self.dist = None
        self.next = None

    def set_mode_add_node(self):
        self.mode = "add_node"
        self.selected_node = None
        messagebox.showinfo("Mode", "Click on the canvas to add a node.")

    def set_mode_add_edge(self):
        if len(self.nodes) < 2:
            messagebox.showwarning("Warning", "Need at least 2 nodes to add an edge.")
            return
        self.mode = "add_edge"
        self.selected_node = None
        messagebox.showinfo("Mode", "Click on a source node, then click on a target node to add an edge.")

    def set_mode_select_path(self):
        if len(self.nodes) < 2:
            messagebox.showwarning("Warning", "Need at least 2 nodes to select a path.")
            return
        self.mode = "select_path"
        self.selected_node = None
        messagebox.showinfo("Mode", "Click on a source node, then click on a destination node to show the shortest path.")

    def canvas_click(self, event):
        if self.mode == "add_node":
            self.add_node(event.x, event.y)
        elif self.mode == "add_edge":
            self.process_add_edge(event.x, event.y)
        elif self.mode == "select_path":
            self.process_select_path(event.x, event.y)

    def add_node(self, x, y):
        node_id = len(self.nodes)
        node = {"id": node_id, "x": x, "y": y}
        r = self.node_radius
        # Draw a circle for the node.
        oval = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="lightblue", outline="black")
        # Label the node with its id.
        text = self.canvas.create_text(x, y, text=str(node_id), font=("Arial", 12, "bold"))
        node["oval"] = oval
        node["text"] = text
        self.nodes.append(node)

    def get_node_at_position(self, x, y):
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
            # Highlight the source node.
            self.canvas.itemconfig(node["oval"], fill="yellow")
        else:
            src = self.selected_node
            dest = node
            # Reset source node highlight.
            self.canvas.itemconfig(src["oval"], fill="lightblue")
            # Ask the user for the weight.
            weight = simpledialog.askfloat("Edge Weight", f"Enter weight for edge from {src['id']} to {dest['id']}:")
            if weight is None:
                self.selected_node = None
                return
            # Draw an arrow from source to destination.
            line = self.canvas.create_line(src["x"], src["y"], dest["x"], dest["y"],
                                           arrow=tk.LAST, width=2, fill="black")
            # Calculate midpoint for displaying the weight.
            mid_x = (src["x"] + dest["x"]) / 2
            mid_y = (src["y"] + dest["y"]) / 2
            weight_text = self.canvas.create_text(mid_x, mid_y, text=str(weight),
                                                  fill="red", font=("Arial", 12, "bold"))
            edge = {"src": src["id"], "dest": dest["id"], "weight": weight,
                    "line": line, "weight_text": weight_text}
            self.edges.append(edge)
            self.selected_node = None

    def process_select_path(self, x, y):
        node = self.get_node_at_position(x, y)
        if not node:
            return
        if self.selected_node is None:
            self.selected_node = node
            self.canvas.itemconfig(node["oval"], fill="yellow")
        else:
            src = self.selected_node
            dest = node
            self.canvas.itemconfig(src["oval"], fill="lightblue")
            self.show_shortest_path(src["id"], dest["id"])
            self.selected_node = None

    def run_floyd_warshall(self):
        n = len(self.nodes)
        # Initialize distance and next matrices.
        self.dist = [[float('inf')] * n for _ in range(n)]
        self.next = [[None] * n for _ in range(n)]
        for i in range(n):
            self.dist[i][i] = 0
            self.next[i][i] = i
        # Set distances for each edge.
        for edge in self.edges:
            i = edge["src"]
            j = edge["dest"]
            self.dist[i][j] = edge["weight"]
            self.next[i][j] = j

        # Floyd–Warshall algorithm
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if self.dist[i][k] + self.dist[k][j] < self.dist[i][j]:
                        self.dist[i][j] = self.dist[i][k] + self.dist[k][j]
                        self.next[i][j] = self.next[i][k]

        messagebox.showinfo("Floyd–Warshall", "Floyd–Warshall algorithm completed.\nShortest distances computed.")

    def show_shortest_path(self, src, dest):
        if self.dist is None or self.next is None:
            messagebox.showwarning("Warning", "Please run the Floyd–Warshall algorithm first.")
            return
        if self.dist[src][dest] == float('inf'):
            messagebox.showinfo("No Path", f"No path exists from {src} to {dest}.")
            return

        # Reconstruct the path.
        path = [src]
        current = src
        while current != dest:
            current = self.next[current][dest]
            path.append(current)

        # Highlight the path on the canvas.
        self.highlight_path(path)
        total_weight = self.dist[path[0]][path[-1]]
        messagebox.showinfo("Shortest Path", f"Shortest path: {' -> '.join(map(str, path))}\nTotal weight: {total_weight}")

    def highlight_path(self, path):
        # Reset all edges to their default appearance.
        for edge in self.edges:
            self.canvas.itemconfig(edge["line"], fill="black", width=2)
        # Highlight only the edges that are part of the shortest path.
        for i in range(len(path) - 1):
            src = path[i]
            dest = path[i+1]
            for edge in self.edges:
                if edge["src"] == src and edge["dest"] == dest:
                    self.canvas.itemconfig(edge["line"], fill="green", width=4)
                    break

    def reset_graph(self):
        self.canvas.delete("all")
        self.nodes = []
        self.edges = []
        self.mode = None
        self.selected_node = None
        self.dist = None
        self.next = None

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphGUI(root)
    root.mainloop()
