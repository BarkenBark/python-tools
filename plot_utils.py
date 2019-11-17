# Functions here may depend on the matplotlib package
import random
import itertools

import matplotlib.pyplot as plt
from matplotlib import colors as mcolors



# Variables 
##########################################
plt_colors_base = list(dict(mcolors.BASE_COLORS).keys())
plt_colors_css4 = list(dict(mcolors.CSS4_COLORS).keys())




# Functions
##########################################

# Returns colorCycler which can be iterated with using 'next(coclorCycler)''
# order can either be a string ('random') or a list
# if order is a string, the number of colors can be specified with nColors
# if order is a list, the number of colors is taken to be the length of the list
# TO-DO: Better solution for seeding. Currently, seeding would affect all randomizations for the rest of the functions in this module, right?
def color_cycler_plt(colormap='base', order=None, n_colors=None, seed=None): 

	if colormap == 'base':
		plt_colors = plt_colors_base
	elif colormap == 'css4':
		plt_colors = plt_colors_css4
	else:
		print('plt_color_cycler: Please specify a valid colormap. Using base for now.')
		plt_colors = plt_colors_base

	if seed is not None:
		random.seed(seed)

	if order is not None:
		if order == 'random':
			order = list(range(len(plt_colors)))
			random.shuffle(order)
			if n_colors is not None:
				order = [order[i] for i in range(n_colors)] # Shrink the list

		assert(isinstance(order, list))
		plt_colors = [plt_colors[i] for i in order]

	plt_color_cycler = itertools.cycle(plt_colors) # next(plt_color_cycler)

	return plt_color_cycler




# Classes
#####################################

# Abstract class
# Updates content of axis according to index
# Usage: 
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax_gen.__update_ax__(ax, index)
class AxesGenerator(object):
    def __update_ax__(self, ax, index):
        raise NotImplementedError
    def __len__(self):
        raise NotImplementedError

# Updates the axes object of a figure when you scroll according to an Axes-generator which outputs an axes according to an index 
class PlotScroller(object):
    def __init__(self, ax, ax_gen):
        # Axes Generator
        self.ax_gen = ax_gen # Instance of AxesGenerator
        self.len = self.ax_gen.len
        self.ax = ax

		# State
        self.index = 0

        # Initialize
        self.draw()
        self.ax.get_figure().canvas.mpl_connect('scroll_event', onscroll)

    def onscroll(self, event): 
        if event.button == 'up':
            self.index = (self.index + 1) % self.len
        else:
            self.index = (self.index - 1) % self.len
        self.draw()

    def draw(self):
        self.ax_gen.__update_ax__(self.ax, self.index)
        plt.draw()