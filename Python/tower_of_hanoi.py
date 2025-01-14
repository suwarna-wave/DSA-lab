# Function to solve the Tower of Hanoi puzzle using recursion
def tower_of_hanoi(n, src, temp, dist):
    if n == 1:
        print(f"Move disk 1 from {src} to {dist}")
        return
    tower_of_hanoi(n - 1, src, dist, temp)  # Move n-1 disks from src to temp
    print(f"Move disk {n} from {src} to {dist}")  # Move the nth disk from src to dist
    tower_of_hanoi(n - 1, temp, src, dist)  # Move n-1 disks from temp to dist

# Main function
def main():
    n = int(input("Enter the number of disks: "))
    print(f"The sequence of moves for {n} disks is:")
    tower_of_hanoi(n, 'A', 'B', 'C')  # A = source, B = temporary, C = destination

# Run the program
if __name__ == "__main__":
    main()
g