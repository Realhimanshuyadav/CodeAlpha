import tkinter as tk

class Calculator:
    """
    A simple GUI calculator application using Tkinter.
    """
    def __init__(self, master):
        """
        Initializes the calculator application.

        Args:
            master: The root Tkinter window.
        """
        self.master = master
        master.title("Simple Calculator")
        master.geometry("300x400") # Set initial window size
        master.resizable(False, False) # Make window non-resizable

        # Configure background color
        master.configure(bg="#333333")

        # Entry widget to display input and results
        # relief='flat' for a modern look, bg and fg for dark theme
        self.entry = tk.Entry(master, width=20, font=('Arial', 24), bd=5,
                              insertwidth=4, bg="#555555", fg="white",
                              justify='right', relief='flat')
        self.entry.grid(row=0, column=0, columnspan=4, pady=10, padx=10, sticky="nsew")

        # Initialize variables for calculation
        self.current_expression = ""
        self.total_expression = ""
        self.operator = ""

        # Define button layout
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('C', 5, 0)
        ]

        # Create and place buttons
        for (text, row, col) in buttons:
            if text == '=':
                # Special styling for the equals button
                button = tk.Button(master, text=text, font=('Arial', 18, 'bold'),
                                   command=lambda t=text: self.on_button_click(t),
                                   bg="#FF9500", fg="white", bd=0, relief='raised',
                                   activebackground="#E08500", activeforeground="white",
                                   height=2, width=5, borderwidth=0, highlightthickness=0,
                                   cursor="hand2")
                button.grid(row=row, column=col, columnspan=1, sticky="nsew", padx=5, pady=5)
            elif text in ['/', '*', '-', '+']:
                # Styling for operator buttons
                button = tk.Button(master, text=text, font=('Arial', 18),
                                   command=lambda t=text: self.on_button_click(t),
                                   bg="#F0F0F0", fg="#333333", bd=0, relief='raised',
                                   activebackground="#E0E0E0", activeforeground="#333333",
                                   height=2, width=5, borderwidth=0, highlightthickness=0,
                                   cursor="hand2")
                button.grid(row=row, column=col, columnspan=1, sticky="nsew", padx=5, pady=5)
            elif text == 'C':
                # Styling for clear button
                button = tk.Button(master, text=text, font=('Arial', 18),
                                   command=lambda t=text: self.on_button_click(t),
                                   bg="#FF3B30", fg="white", bd=0, relief='raised',
                                   activebackground="#E03028", activeforeground="white",
                                   height=2, width=5, borderwidth=0, highlightthickness=0,
                                   cursor="hand2")
                button.grid(row=row, column=col, columnspan=1, sticky="nsew", padx=5, pady=5)
            else:
                # Styling for number and decimal buttons
                button = tk.Button(master, text=text, font=('Arial', 18),
                                   command=lambda t=text: self.on_button_click(t),
                                   bg="#888888", fg="white", bd=0, relief='raised',
                                   activebackground="#777777", activeforeground="white",
                                   height=2, width=5, borderwidth=0, highlightthickness=0,
                                   cursor="hand2")
                button.grid(row=row, column=col, columnspan=1, sticky="nsew", padx=5, pady=5)

        # Configure grid weights to make buttons expand proportionally
        for i in range(6): # 6 rows (0-5)
            master.grid_rowconfigure(i, weight=1)
        for i in range(4): # 4 columns (0-3)
            master.grid_columnconfigure(i, weight=1)

    def on_button_click(self, char):
        """
        Handles button clicks and updates the calculator's state.

        Args:
            char (str): The character/operation associated with the clicked button.
        """
        if char == 'C':
            # Clear all
            self.current_expression = ""
            self.total_expression = ""
            self.operator = ""
            self.update_entry("")
        elif char == '=':
            try:
                # Evaluate the expression
                result = str(eval(self.total_expression + self.current_expression))
                self.update_entry(result)
                self.current_expression = result
                self.total_expression = ""
                self.operator = ""
            except Exception as e:
                self.update_entry("Error")
                self.current_expression = ""
                self.total_expression = ""
                self.operator = ""
                print(f"Calculation error: {e}")
        elif char in ['/', '*', '-', '+']:
            if self.current_expression:
                # If there's a number, append it to total_expression with the operator
                if self.total_expression and self.operator:
                    # If an operator was already pressed, evaluate the partial expression
                    try:
                        self.total_expression = str(eval(self.total_expression + self.current_expression))
                    except Exception as e:
                        self.update_entry("Error")
                        self.current_expression = ""
                        self.total_expression = ""
                        self.operator = ""
                        print(f"Partial calculation error: {e}")
                        return
                else:
                    self.total_expression += self.current_expression

                self.operator = char
                self.total_expression += self.operator
                self.current_expression = ""
                self.update_entry(self.operator) # Show the operator in the entry for a moment
            else:
                # Allow changing operator if no number has been entered yet for the current operand
                if self.total_expression and self.operator:
                    self.total_expression = self.total_expression[:-1] + char # Replace last operator
                    self.operator = char
                    self.update_entry(self.operator)
        else:
            # Append numbers and decimal point
            self.current_expression += char
            self.update_entry(self.current_expression)

    def update_entry(self, value):
        """
        Updates the text displayed in the entry widget.

        Args:
            value (str): The string to display.
        """
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)

# Main part of the script
if __name__ == "__main__":
    root = tk.Tk()
    calculator_app = Calculator(root)
    root.mainloop()