# Learning MAT PLOT LIB!
# Source: https://www.youtube.com/watch?v=UO98lJQ3QGI&list=PL-osiE80TeTvipOqomVEeZ1HRrcEvtZB_

import numpy as np
from matplotlib import pyplot as plt

def random_plt_style():
    all_styles = plt.style.available
    random_style = np.random.choice(all_styles)
    plt.style.use(random_style)

def bar_graph():
    # Data
    ages_x = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35] # The data on the x axis
    dev_y = [38496, 42000, 46752, 49320, 53200, 56000, 62316, 64928, 67317, 68748, 73752] # The data on the y axis
    py_dev_y = [45372, 48876, 53850, 57287, 63016, 65998, 70003, 70000, 71496, 75370, 83640]
    js_dev_y = [37810, 43515, 46823, 49293, 53437, 56373, 62375, 66674, 68745, 68746, 74583]

    # For bar graph
    x_indexes = np.arange(len(ages_x)) # Convert it to a numpy array
    width = 0.25 # Can be any number between 1 and 0, which will allow multiple bars on the same number, and is the visual width of the bars

    # Plotting
    plt.bar(x_indexes-width, dev_y, width=width, label="All Devs") # This will be at the front
    plt.bar(x_indexes, py_dev_y, width=width, label="Python Devs") # Note the order matters. This will be at the back
    plt.bar(x_indexes+width, js_dev_y, width=width, label="JavaScript Devs")

    # Labels
    plt.xticks(ticks=x_indexes, labels=ages_x)

    x_label, y_label, title = "Age (years)", "Median salary (USD)", "Median salary of developers (USD) by age"
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # Legend
    plt.legend() # Makes a legend in the top left. Based on color, marker, linewidth, label, etc attributes of the plt.plot

    # Showing and rendering
    plt.grid(True)
    plt.tight_layout() # Decrease the padding so you can see more
    plt.show()

def line_graph():
    # Data
    ages_x = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35] # The data on the x axis
    dev_y = [38496, 42000, 46752, 49320, 53200, 56000, 62316, 64928, 67317, 68748, 73752] # The data on the y axis
    py_dev_y = [45372, 48876, 53850, 57287, 63016, 65998, 70003, 70000, 71496, 75370, 83640]
    js_dev_y = [37810, 43515, 46823, 49293, 53437, 56373, 62375, 66674, 68745, 68746, 74583]

    # Plotting
    plt.plot(ages_x, dev_y, color="#444444", linestyle="--", marker="o", label="All Devs") # This will be at the front
    plt.plot(ages_x, py_dev_y, color="#5a7d9a", marker="o", linewidth=3, label="Python Devs") # Note the order matters. This will be at the back
    plt.plot(ages_x, js_dev_y, color="#adad3b", marker="o", linewidth=3, label="JavaScript Devs")

    # Labels
    x_label, y_label, title = "Age (years)", "Median salary (USD)", "Median salary of developers (USD) by age"
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # Legend
    plt.legend() # Makes a legend in the top left. Based on color, marker, linewidth, label, etc attributes of the plt.plot

    # Showing and rendering
    plt.grid(True)
    plt.tight_layout() # Decrease the padding so you can see more
    plt.show()


random_plt_style()
line_graph()
bar_graph()




"""

NOTES
Format strings for colouring the legends:
    fmt = "[Marker][Line][Color]" # see documentation
Styles:
    print(plt.style.available) => ['Solarize_Light2', '_classic_test_patch', '_mpl-gallery', '_mpl-gallery-nogrid', 'bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn-v0_8', 'seaborn-v0_8-bright', 'seaborn-v0_8-colorblind', 'seaborn-v0_8-dark', 'seaborn-v0_8-dark-palette', 'seaborn-v0_8-darkgrid', 'seaborn-v0_8-deep', 'seaborn-v0_8-muted', 'seaborn-v0_8-notebook', 'seaborn-v0_8-paper', 'seaborn-v0_8-pastel', 'seaborn-v0_8-poster', 'seaborn-v0_8-talk', 'seaborn-v0_8-ticks', 'seaborn-v0_8-white', 'seaborn-v0_8-whitegrid', 'tableau-colorblind10']
    Styles also have different default colours, line widths, grid preferences, etc.
    Remove the style use and put plt.xkcd() before the plt.show() for a xkcd style plot
    plt.plot = line graph, plt.bar = bar graph
Saving the image:
    plt.savefig("plot.png") # Filepath and file name
"""