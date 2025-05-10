from fractions import Fraction
from sys import exit

def correct_grammar(string:str):
    """Add a full stop to the end of a string if it doesn't have punctutation at the end."""
    if string[-1] not in [".", "!", "?"]: # If the last character is not a punctuation
        string += "." # Add a full stop
    return string

def limited_input(options:dict={"y": "Yes.", "n": "No."}, prompt:str="Select an option.", print_output:bool=True, allow_quit:bool=True):
    """Get user input from a list of options.

    Args
    ----
    options : dict, default={"y": "Yes.", "n": "No."}
        A dictionary of options to choose from, with keys as the option letter and values as the option description.
    prompt : str, default="Select an option."
        The prompt which will be printed.
    allow_quit : bool, default=True
        Whether to allow the user to quit. Adds a "q" option.

    Returns
    -------
    str
        The key of the selected option.
    """

    if allow_quit:
        options.update({"q": "Quit."})
    possible_options = options.keys()

    # Add full stop to end
    prompt = correct_grammar(prompt)
    for option_desc in options.values():
        option_desc = correct_grammar(option_desc)
    
    print(prompt, "Please select one of the following options:")
    for letter, option_desc in options.items(): # Print options
            print(f"{letter} | {option_desc}")

    while True:
        user_input = input(": ").lower().strip()

        if allow_quit and user_input == "q": # Quit
            exit()
        elif user_input in possible_options: # Valid
            if print_output: print(f"Selected option: {options[user_input]}")
            return user_input
        else: # Invalid
            print("Invalid input. Please try again.")

def number_input(prompt:str="Enter a number.", input_type:type=int, only_positive:bool=True, print_output:bool=True, allow_quit:bool=True):
    """Get user input for a integer or float.

    Args
    ----
    prompt : str, default="Enter a number."
        The prompt which will be printed.
    input_type : type, default=int
        The type of number that the user should enter. Can be int or float.
    only_positive : bool, default=True
        Whether to only allow positive numbers.
    allow_quit : bool, default=True
        Whether to allow the user to quit. Adds a "q" option.

    Returns
    -------
    int or float
        The number entered by the user.
    """
    
    prompt = correct_grammar(prompt) # Add full stop to end
    print(f"{prompt}{" Or q to quit" if allow_quit else ""}.", end=" ")

    if input_type == int: print(f"Please enter {"a positive " if only_positive else "an "}integer.")
    elif input_type == float: print(f"Please enter a {"positive " if only_positive else ""}float.")

    while True:
        try:
            user_input = input(": ").strip().lower()
            if allow_quit and user_input == "q":
                exit()
            
            # Convert to type or fraction
            if input_type == float: 
                try: converted_user_input = input_type(user_input) # For example this will be int(user_input)
                except: converted_user_input = float(Fraction(user_input)) # Try converting it to a fraction as well
            else: # input_type == int
                converted_user_input = input_type(user_input)
            
            # Positive only
            if only_positive and converted_user_input < 0:
                print("Please enter a positive number.")
                continue # Try again
            
            if print_output: print(f"You entered: {converted_user_input}.")
            return converted_user_input
        except Exception as e:
            print(f"Invalid input. Please try again. Error: {e}.")

