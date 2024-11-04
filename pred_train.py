import sqlite3
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import StandardScaler


# Step 1: Load Data from SQLite Database
db_path = 'kociemba_pruning_phase1_tests.db'
connection = sqlite3.connect(db_path)
query = "SELECT edge_state, corner_state, slice_state, depth FROM pruning_table"
df = pd.read_sql(query, connection)
connection.close()

# Step 2: Split Data into Training and Validation Sets
X = df[['edge_state', 'corner_state', 'slice_state']]
y = df['depth']
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)

# Convert to PyTorch tensors
X_train_tensor = torch.tensor(X_train_scaled, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train.values, dtype=torch.float32).view(-1, 1)
X_val_tensor = torch.tensor(X_val_scaled, dtype=torch.float32)
y_val_tensor = torch.tensor(y_val.values, dtype=torch.float32).view(-1, 1)

# Create DataLoader for batch processing
train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
val_dataset = TensorDataset(X_val_tensor, y_val_tensor)

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

# Step 3: Define the Neural Network Model
class DepthPredictor(nn.Module):
    def __init__(self):
        super(DepthPredictor, self).__init__()
        self.fc1 = nn.Linear(3, 128)  # Increase to 128 hidden units
        self.fc2 = nn.Linear(128, 64) # Another hidden layer with 64 units
        self.fc3 = nn.Linear(64, 32)  # Additional layer with 32 units
        self.fc4 = nn.Linear(32, 1)  # Output layer with 1 unit for regression output

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        x = self.fc4(x)
        return x

# Instantiate the model, define loss function and optimizer
model = DepthPredictor()
criterion = nn.MSELoss()  # Mean Squared Error for regression
optimizer = optim.Adam(model.parameters(), lr=0.0005)

# Step 4: Training Loop
num_epochs = 1000
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)
for epoch in range(num_epochs):
    model.train()
    train_loss = 0.0
    
    for inputs, targets in train_loader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        train_loss += loss.item() * inputs.size(0)
    
    train_loss /= len(train_loader.dataset)
    print(f"Epoch {epoch+1}/{num_epochs}, Training Loss: {train_loss:.4f}")


    # Validation step after each epoch
    model.eval()
    val_loss = 0.0
    with torch.no_grad():
        for inputs, targets in val_loader:
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            val_loss += loss.item() * inputs.size(0)

    val_loss /= len(val_loader.dataset)
    print(f"Validation Loss: {val_loss:.4f}")

    scheduler.step()

print("Training complete!")
