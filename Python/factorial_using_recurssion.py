def factorial(n):
    return 1 if n == 0 else n * factorial(n - 1)                       # 0! = 1, recursion for n > 0

def main():
    num = int(input("Enter a number: "))
    if num < 0:
        print("Factorial of a negative number doesn't exist.")
    else:
        print(f"Factorial of {num} is {factorial(num)}")

if __name__ == "__main__":
    main()
