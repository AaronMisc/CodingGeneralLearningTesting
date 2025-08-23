import random
import string as string_constants
import csv
import json
import re

def remove_content_in_parentheses(input_string):
    """Removes all text, including the parentheses, between brackets () in the input string."""
    # The pattern r'\(.*?\)' means:
    # \( : Matches a literal opening parenthesis. We use a backslash to escape it.
    # .*? : Matches any character (.), zero or more times (*), non-greedily (?).
    #       Non-greedily means it will match the shortest possible string
    #       until it finds the next part of the pattern, which is a closing parenthesis.
    # \) : Matches a literal closing parenthesis. We use a backslash to escape it.
    return re.sub(r'\(.*?\)', '', input_string)

def open_text(file_name):
    with open(file_name, mode="r") as opened_file:
        read = opened_file.read()
    return read

def read_csv(file_name):
    """Reads a CSV file and returns a list of dictionaries."""
    read = []
    with open(file_name, mode="r", newline="") as opened_file:
        DictRead = csv.DictReader(opened_file) # Create a DictReader object
        for row in DictRead: # Iterate over each row in the CSV file
            read.append(row) # Add the row dictionary to the list
    return read

def read_json(file_name):
    """Reads a JSON file and returns a dictionary."""
    with open(file_name, "r") as opened_file:
        read = json.load(opened_file)
    return read

def remove_letters_after_string(input_text = "Demo # hashtag", string = "#"):
    """Will remove the letters after a string from all lines in input_text.
    
    Example
        Input:
            Demo # Comment
            Demo2 # Comment 2

        String: 
            "#"
            
        Output:
            Demo
            Demo2"""
    lines = input_text.split('\n')
    new_lines = []

    for line in lines:
        if not line.startswith(string):
            line = line.split(string)[0].rstrip()
            new_lines.append(line)

    output = '\n'.join(new_lines)
    return output

def generate_random_string(length):
    """Generates a random string of the specified length."""
    random_string = ''.join(random.choices(string_constants.ascii_letters + ' ', k=length))

    return random_string

def text_pyramid(text, starting_modulo):
    """Generates a pyramid of text from the input text like this (Assuming starting_modulo = 4):
        Hello world
        el wrd
        l r
        lo
    Better with longer strings.
    Makes a jumbled mess."""
    output = ""
    for i in range(len(text)):
        output += text[i%starting_modulo :: i]
    return output


if __name__ == "__main__":
    pass