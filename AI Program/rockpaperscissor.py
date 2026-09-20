import random

def get_user_choice():
    """
    Prompts the user to choose rock, paper, or scissors and validates the input.
    Returns the user's valid choice in lowercase.
    """
    while True:
        user_choice = input("Choose rock, paper, or scissors: ").lower()
        if user_choice in ["rock", "paper", "scissors"]:
            return user_choice
        else:
            print("Invalid choice. Please choose 'rock', 'paper', or 'scissors'.")

def get_computer_choice():
    """
    Generates a random choice (rock, paper, or scissors) for the computer.
    Returns the computer's choice.
    """
    return random.choice(["rock", "paper", "scissors"])

def determine_winner(user_choice, computer_choice):
    """
    Determines the winner of the round based on the game logic.
    Returns "user", "computer", or "tie".
    """
    print(f"\nYou chose: {user_choice.capitalize()}")
    print(f"Computer chose: {computer_choice.capitalize()}")

    if user_choice == computer_choice:
        return "tie"
    elif (user_choice == "rock" and computer_choice == "scissors") or \
         (user_choice == "scissors" and computer_choice == "paper") or \
         (user_choice == "paper" and computer_choice == "rock"):
        return "user"
    else:
        return "computer"

def display_result(winner):
    """
    Displays the result of the round.
    """
    if winner == "user":
        print("You win this round!")
    elif winner == "computer":
        print("Computer wins this round!")
    else:
        print("It's a tie!")

def main():
    """
    Main function to run the Rock-Paper-Scissors game.
    Includes score tracking and play-again functionality.
    """
    user_score = 0
    computer_score = 0
    round_number = 0

    print("--- Welcome to Rock-Paper-Scissors! ---")

    while True:
        round_number += 1
        print(f"\n--- Round {round_number} ---")
        print(f"Score: You {user_score} - Computer {computer_score}")

        user_choice = get_user_choice()
        computer_choice = get_computer_choice()

        winner = determine_winner(user_choice, computer_choice)
        display_result(winner)

        if winner == "user":
            user_score += 1
        elif winner == "computer":
            computer_score += 1

        print(f"Current Score: You {user_score} - Computer {computer_score}")

        play_again = input("\nDo you want to play another round? (yes/no): ").lower()
        if play_again != "yes":
            print("\n--- Game Over! ---")
            print(f"Final Score: You {user_score} - Computer {computer_score}")
            if user_score > computer_score:
                print("Congratulations! You won the game!")
            elif computer_score > user_score:
                print("Better luck next time! The computer won the game.")
            else:
                print("The game ended in a tie!")
            break
        print("-" * 30) # Separator for readability

if __name__ == "__main__":
    main()
