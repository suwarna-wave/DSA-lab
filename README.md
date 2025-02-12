# Data Structures and Algorithms Lab Repository

Welcome to the Data Structures and Algorithms (DSA) Lab repository. This collection encompasses a series of problems and projects undertaken during the 4th semester under the guidance of [Er. Pukar Karki](https://github.com/pukarkarki/), our esteemed subject teacher and mentor. The repository reflects an academic-oriented approach to mastering DSA concepts through practical implementation.

## Repository Structure

The repository is organized into the following directories:

- **C**: Contains implementations of various data structures and algorithms in C.
- **C++**: Features solutions and projects developed using C++.
- **Python**: Includes Python scripts for different DSA problems.
- **Projects**: Houses major projects, notably the Traveling Salesman Problem (TSP) and AVL Tree implementations.

## Highlighted Projects

### Traveling Salesman Problem (TSP) and Graph Theory Algorithms

The TSP project is a significant highlight of this repository, involving graph theory concepts to find optimal paths between nodes. This project includes:

- **Nearest Neighbor Algorithm**: A heuristic method for solving the TSP by repeatedly visiting the nearest unvisited node until all nodes are covered.
- **2-opt Algorithm**: An optimization technique that iteratively reverses segments of the path to reduce the total distance.
- **Dijkstra's Algorithm**: Used to find the shortest path between two nodes in a graph, utilizing a priority queue to efficiently explore distances.
- **Pygame Library**: Implements visualization for nodes and paths, handling graphical display, event handling, and animations.
- **Euclidean Distance Calculation**: Computes distances between nodes using the Euclidean distance formula, crucial for both TSP and shortest path solutions.
- **Heap Data Structure**: Used in Dijkstra's algorithm for efficient retrieval of the next node with the smallest known distance.
- **Animation and Visualization**: The project includes smooth animations for drawing paths and arrows, enhancing the visual representation of the algorithms' results.

For a better understanding of the TSP and its visualization, watch this tutorial:

[![TSP Algorithm Visualization](https://img.youtube.com/vi/XaXsJJh-Q5Y/0.jpg)](https://www.youtube.com/watch?v=XaXsJJh-Q5Y)

# Traveling Salesman Problem (TSP) Solver

## 🚀 Overview
This project is an **interactive Traveling Salesman Problem (TSP) solver** built using **Python** and **Pygame**, integrating multiple algorithms to efficiently optimize travel routes. The solver features real-time visualization and step-by-step pathfinding animations.

## 📌 Features
- 🗺️ **Real-time TSP visualization** with dynamic path updates.
- 🏆 Implements multiple algorithms:
  - **Nearest Neighbor (NN)** for quick approximations.
  - **2-Opt Heuristic** for route optimization.
  - **Dijkstra’s Algorithm** for shortest path calculations.
- 🏗️ **Modular Object-Oriented Design (OOP)** for easy modifications.
- 🚀 **Performance optimizations** using NumPy and efficient data structures.
- 🎨 **Intuitive Pygame UI** for interactive route plotting.

## 🔧 Installation

### Prerequisites
Ensure you have **Python 3.8+** installed. Then, install dependencies:
```sh
pip install pygame numpy
```

### Run the Application
```sh
python tsp_solver.py
```

## 🛠 Usage
1. **Run the script** and open the interactive Pygame window.
2. **Click on the map** to place cities.
3. **Press 'Solve'** to calculate the optimal path using selected algorithms.
4. **Watch the real-time visualization** as paths update dynamically.
5. **Experiment** with different algorithms to compare efficiency.

## 📈 Algorithms Used
| Algorithm        | Time Complexity | Description |
|-----------------|----------------|-------------|
| Nearest Neighbor (NN) | O(n²) | Greedy algorithm selecting the nearest unvisited node. |
| 2-Opt Heuristic | O(n²) | Swaps edges to refine the NN route for better optimization. |
| Dijkstra's Algorithm | O(n²) | Finds the shortest path between two points efficiently. |

## 🚀 Future Enhancements
- 🔄 **Implement Genetic Algorithms & Ant Colony Optimization** for smarter TSP solving.
- 🌍 **Add real-world city coordinates** for practical simulations.
- 📊 **Performance benchmarking** against larger datasets.

## 🤝 Contributing
Contributions are welcome! Fork the repo, create a new branch, and submit a **pull request**. 🚀

🚀 **Star this repository** ⭐ if you found it useful! Let's optimize the world together! 🌍



### AVL Tree Implementation

Another notable project is the implementation of the AVL Tree, a self-balancing binary search tree. This project covers:

- **Understanding AVL Trees**: Exploring the properties and importance of AVL Trees in maintaining balanced search operations.
- **Insertion and Deletion**: Implementing node insertion and deletion with necessary rotations to maintain balance.
- **Tree Traversal**: Performing in-order, pre-order, and post-order traversals to demonstrate the structure and balance of the tree.

For a deeper understanding of AVL Trees, check out this tutorial:

[![AVL Tree Insertion, Implementation, Rotation](https://img.youtube.com/vi/bBIhFbvavLk/0.jpg)](https://www.youtube.com/watch?v=bBIhFbvavLk)

## Mentor Acknowledgment

We extend our heartfelt gratitude to [Er. Pukar Karki](https://github.com/pukarkarki/), Assistant Professor at the Institute of Engineering, Tribhuvan University, for his invaluable guidance and mentorship throughout our DSA classes and practicals. His expertise and support have been instrumental in the successful completion of these projects.

## Contributing

This repository serves as a learning tool for students and enthusiasts aiming to deepen their understanding of data structures and algorithms. Contributions in the form of suggestions, improvements, or additional implementations are welcome. Please feel free to fork the repository and submit pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

*Note: This repository is a part of the academic curriculum during the 4th semester and reflects the collaborative efforts of students under the mentorship of Er. Pukar Karki.*

