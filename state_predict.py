import tensorflow as tf
import numpy as np
import joblib
from sklearn.preprocessing import MinMaxScaler

# Load the trained model
model = tf.keras.models.load_model('rubiks_cube_model.h5')
print("Model loaded successfully.")

# Load the scaler (this should be the same scaler used during training)
scaler = joblib.load('scaler.pkl')  # You must save the scaler during training

# -------------------
# Function to preprocess a new cube state (similar to training)
# -------------------
def preprocess_state(state):
    """
    This function takes a raw state (list of 54 integers) and preprocesses it to be compatible with the model input.
    """
    # Scale the state using the same scaler that was used for training
    state = scaler.transform([state])  # 'state' is a list of 54 integers representing the Rubik's Cube
    return state

# -------------------
# Function to make a prediction on a given state
# -------------------
# Maximum depth used during training (you should replace 4.0 with the actual max depth used)
MAX_DEPTH = 12.0

def make_prediction(state):
    """
    This function preprocesses the input state and predicts the depth (heuristic) using the trained model.
    """
    # Preprocess the input state (scaling and reshaping if necessary)
    processed_state = preprocess_state(state)
    
    # Predict the normalized heuristic (depth) for the given cube state
    normalized_predicted_depth = model.predict(processed_state)

    print(f"Normalized Predicted Depth: {normalized_predicted_depth[0][0]}")

    
    # Denormalize the predicted depth
    predicted_depth = normalized_predicted_depth[0][0] * MAX_DEPTH
    
    # Return the denormalized predicted depth
    return predicted_depth


# -------------------
# Example Input (your cube state)
# -------------------
new_state = [3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5]

# Make a prediction (heuristic value)
predicted_depth = make_prediction(new_state)
print(f"Predicted Depth (Heuristic) for the given state: {predicted_depth}")
