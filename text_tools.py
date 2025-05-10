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