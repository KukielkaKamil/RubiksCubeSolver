from ML2 import CubeSolverNet
import torch
import torch.optim as optim
import math

model = CubeSolverNet()

model.load_state_dict(torch.load('TestModel.pth'))

model.eval()

optimizer = optim.Adam(model.parameters(),lr=0.001)
optimizer.load_state_dict(torch.load('TestSolverOptimizer.pth'))

def predict_depth(edge_state, corner_state, slice_state):
    new_layout = torch.tensor([[1020, 261, 219]], dtype=torch.float32)
    with torch.no_grad():
        predicted_depth = model(new_layout).item()
    depth = math.ceil(predicted_depth)

    return predicted_depth

print(predict_depth(0,297,191))