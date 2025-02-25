# Learning MAT PLOT LIB!
# Source: https://www.youtube.com/watch?v=UO98lJQ3QGI&list=PL-osiE80TeTvipOqomVEeZ1HRrcEvtZB_

from matplotlib import pyplot as plt

# Data
ages_x = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35] # The data on the x axis
dev_y = [38496, 42000, 46752, 49320, 53200, 56000, 62316, 64928, 67317, 68748, 73752] # The data on the y axis
py_dev_y = [45372, 48876, 53850, 57287, 63016, 65998, 70003, 70000, 71496, 75370, 83640]
js_dev_y = [37810, 43515, 46823, 49293, 53437, 56373, 62375, 66674, 68745, 68746, 74583]

# Plotting
data_for_x_axis, data_for_y_axis = ages_x, dev_y
plt.plot(data_for_x_axis, data_for_y_axis, color="#444444", linestyle="--", marker=".", label="All Devs")
plt.plot(ages_x, py_dev_y, color="#5a7d9a", marker="o", label="Python Devs")
plt.plot(ages_x, js_dev_y, color="#adad3b", marker="o", label="JavaScript Devs")

# Labels
x_label, y_label, title = "Age (years)", "Median salary (USD)", "Median salary of cevelopers (USD) by age"
plt.xlabel(x_label)
plt.ylabel(y_label)
plt.title(title)

# Legend
plt.legend()

# Showing
plt.show()

# NOTES
# Format strings for colouring the legends:
#   fmt = "[Marker][Line][Color]" # see documentation