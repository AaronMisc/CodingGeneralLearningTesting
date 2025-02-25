# Learning MAT PLOT LIB!
# Source: https://www.youtube.com/watch?v=UO98lJQ3QGI&list=PL-osiE80TeTvipOqomVEeZ1HRrcEvtZB_

from matplotlib import pyplot as plt

plt.style.use("fivethirtyeight")

# Data
ages_x = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35] # The data on the x axis
dev_y = [38496, 42000, 46752, 49320, 53200, 56000, 62316, 64928, 67317, 68748, 73752] # The data on the y axis
py_dev_y = [45372, 48876, 53850, 57287, 63016, 65998, 70003, 70000, 71496, 75370, 83640]
js_dev_y = [37810, 43515, 46823, 49293, 53437, 56373, 62375, 66674, 68745, 68746, 74583]

# Plotting
data_for_x_axis, data_for_y_axis = ages_x, dev_y
plt.plot(ages_x, py_dev_y, color="#5a7d9a", marker="o", linewidth=3, label="Python Devs") # Note the order matters. This will be at the back
plt.plot(ages_x, js_dev_y, color="#adad3b", marker="o", linewidth=3, label="JavaScript Devs")
plt.plot(data_for_x_axis, data_for_y_axis, color="#444444", linestyle="--", marker="o", label="All Devs") # This will be at the front

# Labels
x_label, y_label, title = "Age (years)", "Median salary (USD)", "Median salary of cevelopers (USD) by age"
plt.xlabel(x_label)
plt.ylabel(y_label)
plt.title(title)

# Legend
plt.legend() # Makes a legend in the top left. Based on color, marker, linewidth, label, etc attributes of the plt.plot

# Showing and rendering
plt.grid(True)
plt.tight_layout() # Decrease the padding so you can see more
plt.show()



"""

NOTES
Format strings for colouring the legends:
    fmt = "[Marker][Line][Color]" # see documentation
Styles:
    print(plt.style.available) => ['Solarize_Light2', '_classic_test_patch', '_mpl-gallery', '_mpl-gallery-nogrid', 'bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn-v0_8', 'seaborn-v0_8-bright', 'seaborn-v0_8-colorblind', 'seaborn-v0_8-dark', 'seaborn-v0_8-dark-palette', 'seaborn-v0_8-darkgrid', 'seaborn-v0_8-deep', 'seaborn-v0_8-muted', 'seaborn-v0_8-notebook', 'seaborn-v0_8-paper', 'seaborn-v0_8-pastel', 'seaborn-v0_8-poster', 'seaborn-v0_8-talk', 'seaborn-v0_8-ticks', 'seaborn-v0_8-white', 'seaborn-v0_8-whitegrid', 'tableau-colorblind10']
    Styles also have different default colours, line widths, grid preferences, etc.
Saving the image:
    plt.savefig("plot.png") # Filepath and file name
"""