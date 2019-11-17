# Functions here have no dependencies outside the Python Standard Library
import os
import pickle

# Change the filenames of files in 'directory' whose filenames are numbers to be formatted with 'n_leading_zeros' zeros
# Specify 'fileformat' to only affect files ending with that extension
def change_num_format(directory, fileformat=None, n_neading_zeros=5):
	for filename in os.listdir(directory):
		if fileformat is not None:
			if filename.endswith(fileformat):
				filename_no_ext = os.path.splitext(filename)[0]
				this_fileformat = os.path.splitext(filename)[1]
				try:
					num = int(filename_no_ext)
					new_filename = str(num).zfill(n_neading_zeros)+this_fileformat
					os.rename(filename, new_filename)
				except ValueError:
					pass

# Print the specified attributes of some variables
# e.g. my_np_array.shape (4,5), my_np_array.dtype int64
def print_attributes(*attributes, **variables):
	if variables is not None:
		for name, variable in variables.items():
			for attribute in attributes:
				print('{}: \n{}'.format(name+'.'+attribute, getattr(variable, attribute)))
			print()

# Find the number of files in 'directory'
# Specify 'fileformat' to only count files ending with that extension
def find_nbr_of_files(directory, format=None):
	n = 0
	for item in os.listdir(directory):
		if os.path.isfile(os.path.join(directory, item)):
			if format is not None:
				if item.endswith(format):
					n += 1
	return n


# Return every 'n_skips' elements for all indexable objects in args.
# Requires the length of the objects in args to have same size along first dimension/axis
# e.g. a, b = downsample_skip(2, [1,2,3,4], ['a','b','c','d']) => a=[1,3], b=['a', 'c']
def downsample_skip(n_skips=1, *args):
	n_elements = len(args[0])
	for i in len(args):
		assert(len(args[i])==nElements)
	selected_elements_range = range(0, n_elements, n_skips)
	selected_elements_slice = slice(0, n_elements, n_skips)
	selectedData = tuple([arg[selected_elements_slice] if type(arg) == list else arg[selected_elements_range] for arg in args])
	return selectedData

# Return elements at indices specified in 'idx' (list) from indexable objects in 'args'
def get_selected_data(idx, *args):
	n_elements = len(args[0])
	for arg in args:
		assert(len(arg)==n_elements)
	selected_data = tuple([[arg[i] for i in idx] for arg in args])
	return selected_data


def save_pickle(var, path):
	os.makedirs(os.path.dirname(path), exist_ok=True)
	with open(path, 'wb') as file:
		pickle.dump(var, file)

def load_pickle(path):
	with open(path, 'rb') as file:
		return pickle.load(file)

def save_txt(var, path):
	os.makedirs(os.path.dirname(path), exist_ok=True)
	with open(path, 'w') as file:
		file.write(str(var))

def load_txt(path):
	with open(path, 'r') as file:
		return file.read()