import torch
import torch.nn as nn
import torch.optim as optim
import random
from RubiksCube import RubiksCube

# Neural network to learn LGF (Learned Guidance Function)
class LGFNet(nn.Module):
    def __init__(self):
        super(LGFNet, self).__init__()
        self.fc1 = nn.Linear(54, 256)  # 54 facelets as input
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 1)  # Output: predicted steps to solution

    def forward(self, x):
        x = torch.flatten(x)
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

# Generate training data: scramble cube and record steps to solution
def generate_training_data(cube, num_samples=1000, max_scrambles=10):
    data = []
    for _ in range(num_samples):
        cube.scramble(max_scrambles)
        state = cube.cube[:]
        steps = random.randint(1, max_scrambles)  # Simplified, use actual solver here
        data.append((state, steps))
    return data

# Train the LGF to predict steps to solution
def train_lgf(lgf, training_data, epochs=100):
    optimizer = optim.Adam(lgf.parameters(), lr=0.001)
    criterion = nn.MSELoss()

    for epoch in range(epochs):
        total_loss = 0
        for state, steps in training_data:
            state = torch.tensor([ord(c) for c in state], dtype=torch.float32)
            steps = torch.tensor([steps], dtype=torch.float32)

            optimizer.zero_grad()
            output = lgf(state)
            loss = criterion(output, steps)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f'Epoch {epoch+1}, Loss: {total_loss / len(training_data)}')

# Solve using the learned guidance function
def evolutionary_solve(cube, lgf, generations=100, pop_size=50):
    population = [cube.cube[:] for _ in range(pop_size)]

    for gen in range(generations):
        new_population = []
        for state in population:
            best_move, best_score = None, float('inf')

            for move in range(12):  # 12 possible moves
                cube.do_move(move)
                state_tensor = torch.tensor([ord(c) for c in cube.cube], dtype=torch.float32)
                score = lgf(state_tensor).item()

                if score < best_score:
                    best_score = score
                    best_move = move

                cube.undo_move(move)  # Reverse move

            if best_move is not None:
                cube.do_move(best_move)
                new_population.append(cube.cube[:])

            if cube.is_solved():
                print(f"Solved in generation {gen + 1}")
                return

        population = new_population
    print("Solution not found within generation limit.")

# Main
if __name__ == "__main__":
    # Initialize Rubik's Cube
    cube = RubiksCube()
    
    # Initialize and train the LGF
    lgf = LGFNet()
    training_data = generate_training_data(cube, num_samples=10000)
    train_lgf(lgf, training_data, epochs=50)
    
    # Try to solve the cube
    cube.scramble(10)  # Scramble cube before solving
    evolutionary_solve(cube, lgf, generations=100)
    torch.save(lgf.state_dict(), "lgf_model.pth")