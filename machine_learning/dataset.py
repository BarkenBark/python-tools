# EXAMPLE OF CUSTOM DATASET CLASS
############################################

from torch.utils.data import Dataset

class CustomDataset(Dataset):
	# Doesn't have to be a directory path parameter, but user should be able to build either a training, validation or test dataset using the same class
	def __init__(self, data_dir):
		self.data_dir = data_dir 
		self.len = 0 # Must be initialized, should be equal to total number of data points in dataset

	# Return single data point consisting of inputs to CustomModel and ground truth outputs
	def __getitem__(self, index):
		raise NotImplementedError
