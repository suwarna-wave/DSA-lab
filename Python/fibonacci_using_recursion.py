# Global array for memoization
table = [-1] * 1005

# Function to calculate Fibonacci using memoization
def fibo(n):
    if n <= 0:
        print("Error: Fibonacci is not defined for n <= 0.")
        return 0
    if n == 1 or n == 2:
        return 1
    if table[n] == -1:
        table[n] = fibo(n - 1) + fibo(n - 2)
    return table[n]

# Main function
def main():
    n = int(input("Enter a positive integer for Fibonacci: "))
    result = fibo(n)
    if result != -1:
        print(f"The {n}th Fibonacci term is {result}.")

# Run the program
if __name__ == "__main__":
    main()
