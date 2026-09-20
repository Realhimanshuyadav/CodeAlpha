def add(x, y):
    """Adds two numbers."""
    return x + y

def subtract(x, y):
    """Subtracts two numbers."""
    return x - y

def multiply(x, y):
    """Multiplies two numbers."""
    return x * y

def divide(x, y):
    """Divides two numbers. Handles division by zero."""
    if y == 0:
        return "Error: Division by zero!"
    return x / y

def main():
    """Main function for the calculator application."""
    print("Simple Calculator")
    print("-----------------")

    while True:
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
        except ValueError:
            print("Invalid input. Please enter numbers only.")
            continue

        print("\nSelect operation:")
        print("1. Add (+)")
        print("2. Subtract (-)")
        print("3. Multiply (*)")
        print("4. Divide (/)")
        print("5. Exit")

        choice = input("Enter choice(1/2/3/4/5): ")

        if choice == '1':
            print(f"{num1} + {num2} = {add(num1, num2)}")
        elif choice == '2':
            print(f"{num1} - {num2} = {subtract(num1, num2)}")
        elif choice == '3':
            print(f"{num1} * {num2} = {multiply(num1, num2)}")
        elif choice == '4':
            result = divide(num1, num2)
            print(f"{num1} / {num2} = {result}")
        elif choice == '5':
            print("Exiting calculator. Goodbye!")
            break
        else:
            print("Invalid input. Please choose a valid operation (1-5).")
        print("-" * 20) # Separator for readability

if __name__ == "__main__":
    main()
