import sqlite3
import pandas as pd
import torch
from torch.utils.data import TensorDataset, DataLoader
import torch.nn as nn
import torch.optim as optim
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from collections import Counter

# Connect to the database and load data
conn = sqlite3.connect("kociemba_pruning_phase1_tests.db")
query = 'SELECT * FROM pruning_table'
df = pd.read_sql(query, conn)
conn.close()

# Separate features and target
X = df[['edge_state', 'corner_state', 'slice_state']].values
y = df['depth'].values  # Unscaled y

# Count the frequency of each depth value in the dataset
depth_counts = Counter(y)

# Compute the total number of samples
total_samples = len(y)

# Calculate the weight for each depth class (inversely proportional to its frequency)
class_weights = {depth: total_samples / count for depth, count in depth_counts.items()}

# Normalize the weights
max_weight = max(class_weights.values())
class_weights = {depth: weight / max_weight for depth, weight in class_weights.items()}

# Create the weights tensor corresponding to each target sample
weights = torch.tensor([class_weights[int(depth)] for depth in y], dtype=torch.float32)

# Standardize input features
scaler_X = StandardScaler()
X = scaler_X.fit_transform(X)

# Normalize target (depth) to range [0, 1]
scaler_y = MinMaxScaler()
y_scaled = scaler_y.fit_transform(y.reshape(-1, 1))  # Scaled y

# Convert to tensors
X_tensor = torch.tensor(X, dtype=torch.float32)
y_tensor = torch.tensor(y_scaled, dtype=torch.float32).view(-1, 1)  # Scaled target reshaped to (N, 1)

# Create dataset and dataloader
dataset = TensorDataset(X_tensor, y_tensor, weights)  # Include weights in the dataset
dataloader = DataLoader(dataset, batch_size=64, shuffle=True)

# Define the neural network architecture
class CubeSolverNet(nn.Module):
    def __init__(self):
        super(CubeSolverNet, self).__init__()
        self.fc1 = nn.Linear(3, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 64)
        self.fc4 = nn.Linear(64, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        x = self.fc4(x)  # No activation here for regression
        return x

model = CubeSolverNet()

# Loss function and optimizer
criterion = nn.MSELoss(reduction='none')  # To calculate weighted loss
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
num_epochs = 100
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0

    for inputs, targets, sample_weights in dataloader:  # Unpack weights
        optimizer.zero_grad()

        # Forward pass
        outputs = model(inputs)

        # Calculate loss
        loss = criterion(outputs, targets.squeeze())

        # Apply weights to the loss based on the target depth values
        weighted_loss = (loss * sample_weights).mean()  # Apply weights to each sample's loss

        # Backpropagation
        weighted_loss.backward()
        optimizer.step()

        running_loss += weighted_loss.item()

    epoch_loss = running_loss / len(dataloader)
    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {epoch_loss:.4f}')

# Save the model and optimizer state
torch.save(model.state_dict(), "TestModel.pth")
torch.save(optimizer.state_dict(), "TestSolverOptimizer.pth")

# Inference with new data layout
new_layout = torch.tensor([[610, 2157, 434]], dtype=torch.float32)
new_layout = scaler_X.transform(new_layout)  # Apply input scaling
new_layout_tensor = torch.tensor(new_layout, dtype=torch.float32)

model.eval()
with torch.no_grad():
    predicted_depth_scaled = model(new_layout_tensor).item()

# Reverse scaling of the predicted depth to the original range
predicted_depth = scaler_y.inverse_transform([[predicted_depth_scaled]])[0][0]

print(f"Predicted moves to solve: {predicted_depth}")
