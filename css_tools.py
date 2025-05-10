import re
import random

def format_color_data(colors, mode=1):
    """Turn object color data into a dictionary
    
    Example
    >>> colors = [{"name":"Oxford Blue","hex":"011936","rgb":[1,25,54],"cmyk":[98,54,0,79],"hsb":[213,98,21],"hsl":[213,96,11],"lab":[9,4,-22]},{"name":"Charcoal","hex":"465362","rgb":[70,83,98],"cmyk":[29,15,0,62],"hsb":[212,29,38],"hsl":[212,17,33],"lab":[35,-1,-10]},{"name":"Cambridge blue","hex":"82a3a1","rgb":[130,163,161],"cmyk":[20,0,1,36],"hsb":[176,20,64],"hsl":[176,15,57],"lab":[65,-12,-3]},{"name":"Olivine","hex":"9fc490","rgb":[159,196,144],"cmyk":[19,0,27,23],"hsb":[103,27,77],"hsl":[103,31,67],"lab":[75,-22,22]},{"name":"Tea green","hex":"c0dfa1","rgb":[192,223,161],"cmyk":[14,0,28,13],"hsb":[90,28,87],"hsl":[90,49,75],"lab":[85,-21,27]}]
    >>> format_color_data(colors, mode=2)
    """
    output = ""
    if mode == 2:
        output += "{\n"

    for color in colors:
        if mode == 1:
            formattedName = re.sub(r"\s+", "_", color["name"]).upper()
        else: 
            formattedName = color["name"].replace(" ", "_").lower()
        rgbValues = tuple(color["rgb"])
        
        doubleQuotation = '"'
        if mode == 1:
            output += (f"{formattedName} = {rgbValues}")
        else:
            output += (f"   {doubleQuotation}{formattedName}{doubleQuotation}: {rgbValues}, \n")
        
    if mode == 2:
        output += "}\n"
    
    return output

def element_name_list_to_css(element_name_list = "h1, h2, div, a, body", from_string=False):
    """Convert a list of element names to empty css style definers

    For example: .header .blog-title div
    
    Will become:
    .header {

    }
    .blog-title {

    }
    div {

    }
    """
    if from_string:
        element_name_list = element_name_list.split()

    for element_name in element_name_list:
        print(element_name + " {\n\n}")

#TEXT URLS: @import url('https://fonts.googleapis.com/css?family=Baloo');

def generate_random_css_style(font_family = "Times New Roman", previous = ""):
    """Generate a random css style with previous (arg) before every line"""
    # generate random RGB color
    r, g, b = random.sample(range(256), 3)
    rgb_color1 = f"rgb({r}, {g}, {b})"
    
    r, g, b = random.sample(range(256), 3)
    rgb_color2 = f"rgb({r}, {g}, {b})"
    
    r, g, b = random.sample(range(256), 3)
    rgb_color3 = f"rgb({r}, {g}, {b})"
    
    # generate random number between 5 and 100
    nums = random.sample(range(5, 255), 15)
    
    output = f"""font-size: {nums[0]}px;
font-family: "Times New Roman";
background: {rgb_color1};
color: {rgb_color2};
width: {nums[1]}px;
height: {nums[2]}px;
line-height: {nums[3]}px;
border-style: solid;
border-width: {nums[4]}px;
text-align: center;
border-color: {rgb_color3};
padding: {nums[5]}px {nums[6]}px {nums[7]}px {nums[8]}px;
margin: {nums[9]}px {nums[1]}px {nums[2]}px {nums[3]}px;
border-radius: {nums[10]}px;
text-decoration: underline;\n"""
    
    if previous != "":
        output_with_previous = ""
        for line in output.splitlines():
            output_with_previous += previous + line + "\n"

        output = output_with_previous
    
    return output

def generate_multiple_random_css_styles(style_number = int(input("How many styles? > "))):
    "Generate multiple css styles and format them"
    output = ""
    for n in range(style_number):
        output += f"style-{n+1} {"{"}\n" + generate_random_css_style(previous="    ") + "}\n"
    
    return output