import random
import string as string_constants
import csv
import json

def read_csv(file_name):
    read = []
    with open(file_name, mode="r", newline="") as opened_file:
        DictRead = csv.DictReader(opened_file) # Create a DictReader object
        for row in DictRead: # Iterate over each row in the CSV file
            read.append(row) # Add the row dictionary to the list
    return read

def read_json(file_name):
    with open(file_name, "r") as opened_file:
        read = json.load(opened_file)
    return read

def remove_letters_after_string(input_text = "Demo # hashtag", string = "#"):
    """Will remove the letters after a string from all lines in input_text
    
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
    random_string = ''.join(random.choices(string_constants.ascii_letters + ' ', k=length))

    return random_string