import random
import string

def generate_password(length, complexity="medium"):
    """
    Generates a random password of a specified length and complexity.

    Args:
        length (int): The desired length of the password.
        complexity (str): The complexity level ("low", "medium", "high").
                          - "low": lowercase letters only
                          - "medium": lowercase, uppercase letters, and digits
                          - "high": lowercase, uppercase letters, digits, and special characters

    Returns:
        str: The generated password.
    """
    if length <= 0:
        return "Password length must be a positive number."

    characters = ""
    if complexity == "low":
        characters = string.ascii_lowercase
    elif complexity == "medium":
        characters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    elif complexity == "high":
        characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    else:
        return "Invalid complexity level. Choose 'low', 'medium', or 'high'."

    if not characters:
        return "Error: No characters available for password generation."

    password = ''.join(random.choice(characters) for i in range(length))
    return password

def main():
    """Main function for the password generator application."""
    print("--- Password Generator ---")

    while True:
        try:
            length = int(input("Enter desired password length (e.g., 12): "))
            if length <= 0:
                print("Password length must be a positive number.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number for length.")
            continue

        print("\nSelect complexity:")
        print("1. Low (lowercase letters)")
        print("2. Medium (lowercase, uppercase, digits)")
        print("3. High (lowercase, uppercase, digits, special characters)")
        complexity_choice = input("Enter choice (1/2/3): ")

        complexity_map = {
            '1': 'low',
            '2': 'medium',
            '3': 'high'
        }
        complexity = complexity_map.get(complexity_choice)

        if complexity:
            password = generate_password(length, complexity)
            print(f"\nGenerated Password: {password}")
        else:
            print("Invalid complexity choice. Please select 1, 2, or 3.")

        another_password = input("\nGenerate another password? (yes/no): ").lower()
        if another_password != 'yes':
            print("Exiting password generator. Goodbye!")
            break
        print("-" * 30) # Separator for readability

if __name__ == "__main__":
    main()
