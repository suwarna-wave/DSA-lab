import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import heapq
import math

class DijkstraVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Dijkstra's Algorithm Visualizer")

        self.canvas = tk.Canvas(self.root, width=800, height=600, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.mode = tk.StringVar(value="Undirected")
        self.nodes = []
        self.nodes_ui = []
        self.edges = {}
        self.node_radius = 20
        self.highlighted_elements = []

        self.create_ui()
        self.canvas.bind("<Button-1>", self.handle_click)

    def create_ui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        tk.Label(control_frame, text="Graph Mode:").pack(side=tk.LEFT)
        graph_type_menu = ttk.Combobox(control_frame, textvariable=self.mode, 
                                       values=["Undirected", "Directed"], state="readonly")
        graph_type_menu.pack(side=tk.LEFT, padx=5)

        tk.Button(control_frame, text="Add Node", command=self.set_add_node_mode).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Add Edge", command=self.set_add_edge_mode).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Run Dijkstra", command=self.run_dijkstra).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Reset", command=self.reset).pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(self.root, text="Mode: Add Node", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        self.current_mode = "add_node"
        self.selected_node = None

    def set_add_node_mode(self):
        self.current_mode = "add_node"
        self.selected_node = None
        self.status_label.config(text="Mode: Add Node (click on canvas)")

    def set_add_edge_mode(self):
        if len(self.nodes) < 2:
            messagebox.showwarning("Warning", "You need at least 2 nodes to add an edge.")
            return
        self.current_mode = "add_edge"
        self.selected_node = None
        self.status_label.config(text="Mode: Add Edge (select source node)")

    def handle_click(self, event):
        if self.current_mode == "add_node":
            self.add_node(event)
        elif self.current_mode == "add_edge":
            self.process_edge_selection(event)

    def add_node(self, event):
        x, y = event.x, event.y

        for nx, ny in self.nodes:
            if math.sqrt((x - nx)**2 + (y - ny)**2) < self.node_radius * 2:
                messagebox.showwarning("Warning", "Nodes are too close together.")
                return

        node_id = len(self.nodes)
        self.nodes.append((x, y))
        self.edges[node_id] = []

        circle = self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                x + self.node_radius, y + self.node_radius,
                                fill='skyblue', outline='black')
        label = self.canvas.create_text(x, y, text=str(node_id), font=("Arial", 12, "bold"))
        self.nodes_ui.append((circle, label))
        self.status_label.config(text=f"Node {node_id} added")

    def process_edge_selection(self, event):
        x, y = event.x, event.y
        node_id = self.get_node_at_position(x, y)

        if node_id is None:
            return

        if self.selected_node is None:
            self.selected_node = node_id
            self.canvas.itemconfig(self.nodes_ui[node_id][0], fill='yellow')
            self.status_label.config(text=f"Selected source node {node_id}. Now select destination node.")
        else:
            source = self.selected_node
            target = node_id
            self.canvas.itemconfig(self.nodes_ui[source][0], fill='skyblue')

            if source == target:
                messagebox.showwarning("Warning", "Cannot create an edge from a node to itself.")
                self.selected_node = None
                return

            weight = simpledialog.askfloat("Edge Weight", 
                                          f"Enter weight for edge from {source} to {target}:",
                                          minvalue=0.0)
            if weight is None:
                self.selected_node = None
                return

            self.add_edge_between_nodes(source, target, weight)
            self.selected_node = None
            self.status_label.config(text="Edge added")

    def get_node_at_position(self, x, y):
        for i, (nx, ny) in enumerate(self.nodes):
            if math.sqrt((x - nx)**2 + (y - ny)**2) <= self.node_radius:
                return i
        return None

    def add_edge_between_nodes(self, source, target, weight):
        x1, y1 = self.nodes[source]
        x2, y2 = self.nodes[target]

        for neighbor, w, line_id, text_id in self.edges[source]:
            if neighbor == target:
                messagebox.showwarning("Warning", f"Edge from {source} to {target} already exists.")
                return

        arrow = tk.LAST if self.mode.get() == "Directed" else None
        line = self.canvas.create_line(x1, y1, x2, y2, fill='black', width=2, arrow=arrow)

        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        offset = 10
        if abs(x2 - x1) > abs(y2 - y1):
            mid_y -= offset
        else:
            mid_x += offset

        text = self.canvas.create_text(mid_x, mid_y, text=str(weight), 
                                     fill="red", font=("Arial", 10, "bold"))

        self.edges[source].append((target, weight, line, text))

        if self.mode.get() == "Undirected":
            rev_line = self.canvas.create_line(x2, y2, x1, y1, fill='black', width=2, state='hidden')
            self.edges[target].append((source, weight, rev_line, text))

    def run_dijkstra(self):
        if len(self.nodes) < 2:
            messagebox.showwarning("Warning", "Need at least 2 nodes to run algorithm.")
            return

        for elem in self.highlighted_elements:
            self.canvas.delete(elem)
        self.highlighted_elements = []

        start = simpledialog.askinteger("Start Node", 
                                      f"Enter start node (0-{len(self.nodes)-1}):",
                                      minvalue=0, maxvalue=len(self.nodes)-1)
        if start is None:
            return

        end = simpledialog.askinteger("End Node", 
                                     f"Enter end node (0-{len(self.nodes)-1}):",
                                     minvalue=0, maxvalue=len(self.nodes)-1)
        if end is None:
            return

        dist, prev = self.dijkstra(start)

        if dist[end] == float('inf'):
            messagebox.showinfo("Result", f"No path exists from node {start} to node {end}.")
            return

        path = []
        current = end
        while current is not None:
            path.append(current)
            current = prev[current]
        path.reverse()

        self.highlight_path(path, dist[end])

    def dijkstra(self, start):
        dist = {node: float('inf') for node in range(len(self.nodes))}
        dist[start] = 0
        prev = {node: None for node in range(len(self.nodes))}

        pq = [(0, start)]

        while pq:
            current_dist, current = heapq.heappop(pq)

            if current_dist > dist[current]:
                continue

            for neighbor, weight, _, _ in self.edges[current]:
                distance = current_dist + weight

                if distance < dist[neighbor]:
                    dist[neighbor] = distance
                    prev[neighbor] = current
                    heapq.heappush(pq, (distance, neighbor))

        return dist, prev

    def highlight_path(self, path, total_distance):
        for node_id in path:
            x, y = self.nodes[node_id]
            highlighted_node = self.canvas.create_oval(
                x - self.node_radius, y - self.node_radius,
                x + self.node_radius, y + self.node_radius,
                outline='green', width=3)
            self.highlighted_elements.append(highlighted_node)

        for i in range(len(path)-1):
            source = path[i]
            target = path[i+1]

            for neighbor, weight, line_id, _ in self.edges[source]:
                if neighbor == target:
                    x1, y1 = self.nodes[source]
                    x2, y2 = self.nodes[target]
                    line = self.canvas.create_line(x1, y1, x2, y2, fill='green', width=3)
                    self.highlighted_elements.append(line)
                    break

        messagebox.showinfo("Shortest Path", f"Shortest distance (minimum cost): {total_distance}\nPath: {' -> '.join(map(str, path))}")

    def reset(self):
        self.canvas.delete("all")
        self.nodes.clear()
        self.nodes_ui.clear()
        self.edges.clear()
        self.highlighted_elements.clear()
        self.set_add_node_mode()

if __name__ == "__main__":
    root = tk.Tk()
    app = DijkstraVisualizer(root)
    root.mainloop()