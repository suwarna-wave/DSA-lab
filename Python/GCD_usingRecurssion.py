# Recursive function to find GCD
def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

# Main function
def main():
    num1, num2 = map(int, input("Enter two numbers: ").split())
    print(f"GCD of {num1} and {num2} is: {gcd(num1, num2)}")

# Run the program
if __name__ == "__main__":
    main()
