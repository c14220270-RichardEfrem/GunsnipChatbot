# Import necessary libraries
import json
import torch
import torch.nn as nn
import numpy as np
from torch.utils.data import Dataset, DataLoader

# Import custom modules
from nltkPreprocessing import tokenize, stem, bag_of_words
from trainingModel import NeuralNet

# Load intents data from JSON file
with open('intentsGunsnip.json', 'r') as f:
    intents_data = json.load(f)

# Initialize lists to store words, tags, and training data
all_words = []
tags = []
training_data = []

# Loop through intents data to extract patterns and tags
for intent in intents_data['intents']:
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        words = tokenize(pattern)
        all_words.extend(words)
        training_data.append((words, tag))

# Stem and preprocess words, removing duplicates and punctuation
ignore_words = ['?', '.', '!', ',', ';', ':']
all_words = [stem(w) for w in all_words if w not in ignore_words]
all_words = sorted(set(all_words))
tags = sorted(set(tags))

# Create training data in bag-of-words format
X_train = []
y_train = []
for (pattern_words, tag) in training_data:
    bag = bag_of_words(pattern_words, all_words)
    X_train.append(bag)
    y_train.append(tags.index(tag))

# Convert training data to numpy arrays
X_train = np.array(X_train)
y_train = np.array(y_train)

# Define hyperparameters
num_epochs = 1200
batch_size = 8
learning_rate = 0.0001
input_size = len(X_train[0])
hidden_size = 8
output_size = len(tags)

# Define custom dataset class for training
class ChatDataset(Dataset):
    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.n_samples

# Create DataLoader for the dataset
dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset,
                          batch_size=batch_size,
                          shuffle=True,
                          num_workers=0)

# Determine device (CPU or GPU)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Initialize neural network model
model = NeuralNet(input_size, hidden_size, output_size).to(device)

# Define loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Train the model
for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.to(dtype=torch.long).to(device)
        
        outputs = model(words)
        loss = criterion(outputs, labels)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
    if (epoch+1) % 100 == 0:
        print (f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.7f}')

# Print final loss
print(f'Final loss: {loss.item():.4f}')

# Save model and related data
model_data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "output_size": output_size,
    "hidden_size": hidden_size,
    "all_words": all_words,
    "tags": tags
}
FILE = "gunsnipBotData.pth"
torch.save(model_data, FILE)
print(f'Training Complete. Model Saved to {FILE}')
