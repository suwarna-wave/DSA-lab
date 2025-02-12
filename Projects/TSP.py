import pygame        # pip install pygame if you don't have it installed this is for graphical visualization
import math          # This is for mathematical calculations
import time          #  This is for time calculations
import itertools    # This is for iteration brute force
import sys           # This is for system operations
import heapq         # This is for heap operations
import numpy as np    # This is for numerical operations pip install numpy if you don't have it installed


# Colors for the GUI window
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)


# Window dimensions for the GUI
WIDTH = 1000
HEIGHT = 700


class Node: # This is the class for the nodes
    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.radius = 8
        self.color = RED
        self.index = index

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        font = pygame.font.SysFont('Arial', 20)
        text_surface = font.render(str(self.index), True, BLACK)
        screen.blit(text_surface, (self.x - 10, self.y - 10))

class TSPSolver:
    def __init__(self, nodes):
        self.nodes = nodes
        self.n = len(nodes)
        self.distance_matrix = self.calculate_distance_matrix()

    def calculate_distance_matrix(self):
        coords = np.array([(node.x, node.y) for node in self.nodes])
        return np.linalg.norm(coords[:, None] - coords[None, :], axis=-1)

    def nearest_neighbor(self):
        path = [0]
        unvisited = set(range(1, self.n))
        
        while unvisited:
            current = path[-1]
            nearest = min(unvisited, key=lambda x: self.distance_matrix[current][x])
            path.append(nearest)
            unvisited.remove(nearest)
        
        path.append(0)
        return path

    def two_opt(self, initial_path):
        best_path = initial_path[:]
        improved = True
        
        while improved:
            improved = False
            for i in range(1, len(best_path)-2):
                for j in range(i+1, len(best_path)-1):
                    new_path = best_path[:i] + best_path[i:j+1][::-1] + best_path[j+1:]
                    if self.path_length(new_path) < self.path_length(best_path):
                        best_path = new_path[:]
                        improved = True
                        break
                if improved:
                    break
        return best_path

    def path_length(self, path):
        return sum(self.distance_matrix[path[i]][path[i+1]] for i in range(len(path)-1))

    def dijkstra(self, start, end):
        pq = [(0, start)]
        distances = {i: float('inf') for i in range(self.n)}
        distances[start] = 0
        predecessors = {}
        
        while pq:
            current_distance, current_node = heapq.heappop(pq)
            
            if current_node == end:
                break
            
            for neighbor in range(self.n):
                if neighbor == current_node:
                    continue
                distance = self.distance_matrix[current_node][neighbor]
                new_distance = current_distance + distance
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = current_node
                    heapq.heappush(pq, (new_distance, neighbor))
        
        path = []
        while end in predecessors:
            path.append(end)
            end = predecessors[end]
        path.append(start)
        return path[::-1]

class TSPVisualizer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("TSP & Shortest Path Solver")
        self.clock = pygame.time.Clock()
        self.nodes = []
        self.running = False
        self.algorithm = "nearest_neighbor"
        self.font = pygame.font.SysFont('Arial', 20)
        self.paths = []
        self.distance_text = ""
        self.animation_step = 0

    def draw_arrow(self, start, end, color):
        pygame.draw.line(self.screen, color, (start.x, start.y), (end.x, end.y), 2)
        angle = math.atan2(end.y - start.y, end.x - start.x)
        arrow_length = 10
        arrow_angle = math.pi / 6
        pygame.draw.line(self.screen, color, (end.x, end.y), 
                         (end.x - arrow_length * math.cos(angle - arrow_angle), 
                          end.y - arrow_length * math.sin(angle - arrow_angle)), 2)
        pygame.draw.line(self.screen, color, (end.x, end.y), 
                         (end.x - arrow_length * math.cos(angle + arrow_angle), 
                          end.y - arrow_length * math.sin(angle + arrow_angle)), 2)

    def animate_path(self, path, color):
        for i in range(len(path)-1):
            start = self.nodes[path[i]]
            end = self.nodes[path[i+1]]
            self.draw_arrow(start, end, color)
            pygame.display.flip()
            pygame.time.delay(200)  # Smooth animation delay

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and not self.running:
                x, y = pygame.mouse.get_pos()
                self.nodes.append(Node(x, y, len(self.nodes) + 1))
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    self.nodes = []
                    self.paths = []
                    self.distance_text = ""
                elif event.key == pygame.K_r and len(self.nodes) > 2:
                    self.running = True
                    self.solve_tsp()
                elif event.key == pygame.K_s and len(self.nodes) > 1:
                    self.solve_shortest_path()
                elif event.key == pygame.K_1:
                    self.algorithm = "nearest_neighbor"
                elif event.key == pygame.K_2:
                    self.algorithm = "two_opt"

    def solve_tsp(self):
        solver = TSPSolver(self.nodes)
        path = solver.nearest_neighbor()
        if self.algorithm == "two_opt":
            path = solver.two_opt(path)
        self.paths.append((path, BLUE))
        self.distance_text = f"TSP Distance: {solver.path_length(path):.2f}"
        self.animate_path(path, BLUE)
        self.running = False

    def solve_shortest_path(self):
        solver = TSPSolver(self.nodes)
        start, end = 0, len(self.nodes) - 1
        path = solver.dijkstra(start, end)
        self.paths.append((path, ORANGE))
        self.distance_text = f"Shortest Path Distance: {solver.path_length(path):.2f}"
        self.animate_path(path, ORANGE)
        self.running = False

    def update_display(self):
        self.screen.fill(WHITE)
        for node in self.nodes:
            node.draw(self.screen)
        for path, color in self.paths:
            for i in range(len(path)-1):
                self.draw_arrow(self.nodes[path[i]], self.nodes[path[i+1]], color)
        text_surface = self.font.render(self.distance_text, True, BLACK)
        self.screen.blit(text_surface, (10, 10))
        pygame.display.flip()
        self.clock.tick(60)
        self.handle_events()

    def run(self):
        while True:
            self.update_display()

if __name__ == "__main__":
    visualizer = TSPVisualizer()
    visualizer.run()