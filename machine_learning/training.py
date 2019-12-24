# GUIDELINE SCRIPT FOR TRAINING A MODEL
#################################################

# Torch
import torch

# Custom classes
import CustomModel # Torch input-output model to be trained
import custom_loss # Torch loss function
import CustomDataset # Torch dataset


# SETTINGS (Example)
#################################

learning_rate = 1e-4

batch_size = 8
n_epochs = 100
min_delta_factor = 0.05 # Only count network as significant improvement (for early stopping) if the loss is this many percent less than previous best 
patience = 10 # Number of epochs without significant improvment before early stopping

training_data_dir = './data/train'
validation_data_dir = './data/validation'
checkpoint_path = './checkpoints'




# TRAINING AND VALIDATION FUNCTION DEFINITIONS
###############################################

# Completes one epoch of training of 'model' to fit data from 'data_loader' using 'optimizer'
def train(model, data_loader, optimizer):

	if not model.training:
		model.train()

	# Iterate over batches
	for idx, data in enumerate(data_loader):
		
		# Extract data
		inputs, outputs_gt = [d.cuda() for d in data]

		# Forward propagate
		outputs_pred = model(inputs)

		# Compute loss
		loss = custom_loss(outputs_pred, outputs_gt)

		# Update weights w.r.t. loss
		optimizer.zero_grad()
		loss.backward()
		optimizer.step()

	return loss

# Computes loss of 'model' on validation data from 'data_loader'
def validate(model, data_loader):

	if model.training:
		model.eval()

	# Iterate over batches
	for idx, data in enumerate(data_loader):
		with torch.no_grad():

			# Extract data and forward propagate
			inputs, outputs_gt = [d.cuda() for d in data]
			outputs_pred = model(inputs)

			# Compute loss
			loss = custom_loss(outputs_pred, outputs_gt)

	return loss




# MAIN SCRIPT
###############################################

# Create the model
model = CustomModel()
#model = DataParallel(model).cuda() # To enable more efficient computation

# Initialize the optimizer
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate) # e.g. Adam from torch

# Create the training dataloader
training_set = CustomDataset(data_dir=training_data_dir)
training_sampler = torch.utils.data.RandomSampler(training_set)
training_sampler = torch.utils.data.BatchSampler(training_sampler, batch_size)
training_loader = torch.utils.data.DataLoader(training_set, batch_sampler=training_sampler)

# Create the validation dataloader
validation_set = CustomDataset(data_dir=validation_data_dir)
validation_sampler = torch.utils.data.RandomSampler(validation_set)
validation_sampler = torch.utils.data.BatchSampler(validation_sampler, batch_size)
validation_loader = torch.utils.data.DataLoader(validation_set, batch_sampler=validation_sampler)



# Initialize training state
if resume_training:
	print('Attempting to resume training from checkpoint at ' + checkpoint_path)
	if os.path.isfile(checkpoint_path):
		checkpoint = torch.load(checkpoint_path)
		model.load_state_dict(checkpoint['model'])
		optimizer.load_state_dict(checkpoint['optimizer'])
		loss_training_history, loss_validation_history = checkpoint['loss']
		starting_epoch = checkpoint['epoch_finished'] + 1
		loss_validation_best = checkpoint['loss_validation_best']
		loss_validation_improvement = checkpoint['loss_validation_improvement']
		n_epochs_since_improvement = checkpoint['n_epochs_since_improvement']
	else:
		print('No checkpoint found at ' + checkpoint_path + '. Exiting.')
		exit()
else:
	loss_training_history, loss_validation_history = ([],[])
	starting_epoch = 0
	loss_validation_best = 1.7976931348623157e+30
	loss_validation_improvement = loss_validation_best
	n_epochs_since_improvement = 0



# Start training
for iEpoch in range(starting_epoch, n_epochs):

	# Train the model
	loss_training = train(model, training_loader, optimizer)
	loss_training_history.append(loss_training)

	# Validate the model
	loss_validation = validate(model, validation_loader)
	loss_validation_history.append()

	# Save the checkpoint
	checkpoint = {
		'epoch_finished': iEpoch,
		'model': model.state_dict(),
		'optimizer': optimizer.state_dict(),
		'loss': (loss_training_history, loss_validation_history),
		'loss_validation_best': loss_validation_best,
		'loss_validation_improvement': loss_validation_improvement,
		'n_epochs_since_improvement': n_epochs_since_improvement
		}
	torch.save(checkpoint, os.path.join(checkpoint_dir, 'checkpoint.pt'))

	# Save the best model (TODO: Bake the datetime into filename)
	if loss_validation < loss_validation_best:
		loss_validation_best = loss_validation
		torch.save(model.state_dict(), os.path.join(checkpoint_dir, 'best.pt'))
		if loss_validation_best < loss_validation_improvement*(1-min_delta_factor):
			loss_validation_improvement = loss_validation_best
			n_epochs_since_improvement = 0
	n_epochs_since_improvement += 1

	# Check early stopping condition
	if n_epochs_since_improvement > patience:
		print('EARLY STOPPING: Stopped at epoch {} after {} epochs without significant improvement'.format(iEpoch, patience))
		break 

#End epoch loop
if iEpoch == nEpochs:
	print('Stopped at epoch {} which was the final epoch.'.format(iEpoch))
