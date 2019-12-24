# Functions here have no dependencies outside the Python Standard Library
import os
import pickle
import time

# DIRECTORY AND FILE MANIPULATION
################################################

# Find the number of files in 'directory'
# Specify 'fileformat' to only count files ending with that extension
def find_nbr_of_files(directory, extension=None):
	n = 0
	for filename in os.listdir(directory):
		if os.path.isfile(os.path.join(directory, filename)):
			if extension is not None:
				if filename.endswith(extension):
					n += 1
			else:
				n += 1
	return n

# Return list of files in 'directory'
# Specify 'fileformat' to only return files ending with that extension
def list_files(directory, extension=None, include_dir=False):
	files = []
	for filename in os.listdir(directory):
		if os.path.isfile(os.path.join(directory, filename)):
			if extension is not None:
				if not filename.endswith(extension):
					continue
			if include_dir:
				filepath = os.path.join(directory, filename)
			else:
				filepath = filename
			files.append(filepath)
	return files

# Change the filenames of files in 'directory' whose filenames are numbers to be formatted with 'n_leading_zeros' zeros
# Specify 'fileformat' to only affect files ending with that extension
def change_num_format(directory, fileformat=None, n_leading_zeros=5):
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

# Remove last part of string starting with a dot, including the dot
def remove_extension(file_path):
    if len(file_path.split('.')) > 1:
        return ''.join([x for i,x in enumerate(file_path.split('.')) if i < len(file_path.split('.'))-1])
    else:
        return file_path

        

# DATA MANIPULATION
##############################################

# Print the specified attributes of some variables
# e.g. my_np_array.shape (4,5), my_np_array.dtype int64
def print_attributes(*attributes, **variables):
	if variables is not None:
		for name, variable in variables.items():
			for attribute in attributes:
				print('{}: \n{}'.format(name+'.'+attribute, getattr(variable, attribute)))
			print()

# Return every 'n_skips' elements for all indexable objects in args.
# Requires the length of the objects in args to have same size along first dimension/axis
# e.g. a, b = downsample_skip(2, [1,2,3,4], ['a','b','c','d']) => a=[1,3], b=['a', 'c']
def downsample_skip(n_skips=1, *args):
	n_elements = len(args[0])
	for i in len(args):
		assert(len(args[i])==nElements)
	selected_elements_range = range(0, n_elements, n_skips)
	selected_elements_slice = slice(0, n_elements, n_skips)
	selected_data = tuple([arg[selected_elements_slice] if type(arg) == list else arg[selected_elements_range] for arg in args])
	return selected_data

# Return elements at indices specified in 'idx' (list) from indexable objects in 'args'
# NOTE: This functions is kind of rendered pointless by zip
def get_selected_data(idx, *args):
	n_elements = len(args[0])
	for arg in args:
		assert(len(arg)==n_elements)
	selected_data = tuple([[arg[i] for i in idx] for arg in args])
	return selected_data



# SAVING AND LOADING FILES
#####################################################

# Generates a unique (uniqueness guaranteed), random and memorable file name
# Courtesy of Jan Pettersson
def generate_name():
    t = time.localtime()
    a = random.choice(['blue', 'yellow', 'green', 'red', 'orange','pink','grey',
                       'white', 'black', 'turkouse', 'fushia', 'beige','purple',
                       'rustic', 'idyllic', 'kind', 'turbo', 'feverish','horrid',
                       'master', 'correct', 'insane', 'relevant','chocolate',
                       'silk', 'big', 'short', 'cool', 'mighty', 'weak','candid',
                       'figting','flustered', 'perplexed', 'screaming','hip',
                       'glorious','magnificent', 'crazy', 'gyrating','sleeping'])
    b = random.choice(['battery', 'horse', 'stapler', 'giraff', 'tiger', 'snake',
                       'cow', 'mouse', 'eagle', 'elephant', 'whale', 'shark',
                       'house', 'car', 'boat', 'bird', 'plane', 'sea','genius',
                       'leopard', 'clown', 'matador', 'bull', 'ant','starfish',
                       'falcon', 'eagle','warthog','fulcrum', 'tank', 'foxbat',
                       'flanker', 'fullback', 'archer', 'arrow', 'hound'])

    datestr = time.strftime("%m%d%H%M%S", t).encode('utf8')
    b36 = base36encode(int(datestr))
    name = "{}_{}_{}".format(b36,a,b)
    return name.upper()

# Courtesy of Jan Pettersson
def base36encode(integer):
    chars, encoded = '0123456789abcdefghijklmnopqrstuvwxyz', ''

    while integer > 0:
        integer, remainder = divmod(integer, 36)
        encoded = chars[remainder] + encoded

    return encoded

# Checks the number of existing files in 'directory' of format 'fileformat', and stores 'file' with the next filename in the sequence, assuming all files are named e.g. 00001.fileformat, 00002.fileformat, ....
def add_file_to_directory(file, directory, write_method, fileformat, n_leading_zeros=None):
    existing_files = os.listdir(directory)
    if n_leading_zeros is None:
    	n_leading_zeros = len(existing_files[0])
    existing_indices = [int(os.path.splitext(file)[0]) for file in existing_files if file.endswith(file_format)]
    if len(existing_indices) > 0:
        max_index = max(existing_indices)
    else:
        max_index = 0
    file_path = os.path.join(directory, str(max_index+1).zfill(n_leading_zeros)+file_format)
    write_method(file_path, file)

# Save 'var' as a pickle file at 'path'
def save_pickle(var, path):
	os.makedirs(os.path.dirname(path), exist_ok=True)
	with open(path, 'wb') as file:
		pickle.dump(var, file)

# Load the contents of the pickle file at 'path'
def load_pickle(path):
	with open(path, 'rb') as file:
		return pickle.load(file)

# Save the string of 'var' to path
def save_txt(var, path):
	os.makedirs(os.path.dirname(path), exist_ok=True)
	with open(path, 'w') as file:
		file.write(str(var))

# Load the string content of the file at 'path'
def load_txt(path):
	with open(path, 'r') as file:
		return file.read()



# TIME MEASUREMENTS
#####################################################

# Class for measuring time between ticks and storing samples
# Assume time to perform tick() is negligible 
class Clocker:

	def __init__(self, buffer_size=100, log_path=None):
		self.log_path = log_path
		self.__stopwatch = Stopwatch()
		self.__buffer = RingBuffer(buffer_size)

	def tick(self):
		if self.__stopwatch.is_running():
			elapsed = self.__stopwatch.elapsed()
			self.__stopwatch.restart()
			self.__buffer.put(elapsed)
		else:
			elapsed = 0
			self.__stopwatch.start()
		return elapsed

	def samples(self):
		return self.__buffer.items()

# Class for measuring time between ticks and storing samples for multiple sources
# Assume time to perform tick() is negligible. # WARNING: Current implementation is very inefficient, assumption does not hold for some cases
# TODO: Warn user when measuring times too fast for this class to work properly with/without logging 
# TODO: Find more efficient implementation
class MultiClocker:

	def __init__(self, buffer_size=100, log_dir=None):
		self.log_dir = log_dir
		self.__sources = {}
		self.__buffer_size = buffer_size
		print('WANING: This class is currently quite inefficient, and will probably add a slight bias to time measurements.\n If used on same thread as processing, it will potentially have an impact on processing performance.')

	def tick(self, source, log_to_file=False):
		if source in self.__sources: # If we've already started measuring times for this event
			elapsed = self.__sources[source]['stopwatch'].elapsed()
			self.__sources[source]['stopwatch'].restart()
			self.__sources[source]['samples'].put(elapsed)
			if 'logfile' in self.__sources[source]:
				self.__sources[source]['logfile'].write(elapsed+'\n')
		else: # Add source to dict of measured sources
			elapsed = 0
			self.__sources[source] = {'stopwatch': Stopwatch(), 'samples': RingBuffer(self.__buffer_size)}
			if self.log_dir is not None and log_to_file:
				self.__sources[source]['logfile'] = open(os.path.join(log_dir, source+'.txt'), 'a')
			self.__sources[source]['stopwatch'].start()
		return elapsed

	def samples(self, source):
		return self.__sources[source]['samples'].items()

# Stopwatch class with similar functionality to Stopwatch in C#
class Stopwatch:

	def __init__(self):
		self.__is_running = False
		self.__elapsed = 0
		self.__start_time = 0
		self.__stop_time = 0

	def is_running(self):
		return self.__is_running

	# Return the total elapsed time measured for an interval.
	# An interval is defined to be the time during whiich the stopwatch is running.
	def elapsed(self):
 		if self.__is_running:
 			return self.__elapsed + time.time() - self.__start_time
 		else:
 			return self.__elapsed

	# Starts measuring elapsed time for an interval.
	def start(self):
		if not self.__is_running:
			self.__start_time = time.time()
			self.__is_running = True

	# Stops measuring elapsed time for an interval.
	# Returns elapsed time before stop.
	def stop(self):
		if self.__is_running:
			self.__stop_time = time.time()
			self.__elapsed += self.__stop_time - self.__start_time
			self.__is_running = False
		return self.__elapsed

	# Stops time interval measurement and resets the elapsed time to zero.
	# Returns elapsed time before reset.
	def reset(self):
		elapsed = self.stop()
		self.__elapsed = 0
		return elapsed

	# Stops time interval measurement, resets the elapsed time to zero, and starts measuring elapsed time.
	# Returns elapsed time before restart.
	def restart(self):
		elapsed = self.reset()
		self.start()
		return elapsed



# DATA STRUCTURES
##########################################

# Class which implements a simple ring buffer
# todo: Allow resizing ringbuffer after instantiation
class RingBuffer:

	def __init__(self, buffer_size=10):
		self.__items = [None]*buffer_size
		self.__buffer_size = buffer_size
		self.__index = 0

	def items(self):
		return self.__items

	def put(self, item):
		self.__items[self.__index] = item
		self.__index = (self.__index + 1) % self.__buffer_size

	def last(self):
		return self.__items[(self.__index-1) % self.__buffer_size]

	def n_last(self, n):
		assert(n <= self.__buffer_size)
		latest_items = []
		for i in reversed(range(n)):
			latest_items.append(self.__items[(self.__index-i-1) % self.__buffer_size])
		return latest_items