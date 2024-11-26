import sqlite3
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import joblib
from sklearn.utils import resample
from sklearn.utils.class_weight import compute_class_weight

# -------------------
# Database Interaction
# -------------------
DB_PATH = "cube_states.db"

def load_data_from_db_and_rebalance():
    """
    Load data from the SQLite database and rebalance it to handle class imbalance.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT encoded_state, depth FROM cube_states")
        rows = cursor.fetchall()
    
    states = []
    depths = []
    for row in rows:
        encoded_state = list(map(int, row[0].strip('[]').split(',')))  # Convert string to list of integers
        depth = row[1]
        states.append(encoded_state)
        depths.append(depth)
    
    states = np.array(states)
    depths = np.array(depths)

    # Normalize depths to [0, 1] range for model training (assuming max depth is 12)
    depths = depths / 12  # Normalize depths between 0 and 1

    # Rebalance dataset using oversampling (increase samples for underrepresented depths)
    def rebalance_dataset(states, depths):
        data = list(zip(states, depths))
        max_count = max([depths.tolist().count(d) for d in set(depths)])
        
        balanced_data = []
        for depth in set(depths):
            depth_data = [item for item in data if item[1] == depth]
            oversampled = resample(depth_data, replace=True, n_samples=max_count, random_state=42)
            balanced_data.extend(oversampled)
        
        balanced_states, balanced_depths = zip(*balanced_data)
        return np.array(balanced_states), np.array(balanced_depths)

    balanced_states, balanced_depths = rebalance_dataset(states, depths)
    return balanced_states, balanced_depths

# -------------------
# Model Definition (Keras)
# -------------------
def create_model():
    """
    Creates and returns a compiled Keras model for predicting the depth of the Rubik's Cube state.
    """
    model = models.Sequential()
    model.add(layers.InputLayer(input_shape=(54,)))  # 54 input features (cube state)
    model.add(layers.Dense(256, activation='relu'))
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dropout(0.3))
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(1))  # Output layer (heuristic value)

    model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9),
                  loss='mean_absolute_error')  # Use MAE loss for regression
    
    return model

# -------------------
# Training Process (TensorFlow)
# -------------------
# -------------------
# Training Process (TensorFlow)
# -------------------
def train_model():
    """
    Train the model on the dataset with rebalancing and class weights if needed.
    """
    # Load and rebalance data
    states, depths = load_data_from_db_and_rebalance()

    # Normalize states using MinMaxScaler
    scaler = MinMaxScaler()
    states = scaler.fit_transform(states)
    joblib.dump(scaler, 'scaler.pkl')  # Save the scaler for later use in prediction

    # Split data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(states, depths, test_size=0.2, random_state=42)

    # Compute class weights to address class imbalance
    depths_original = (depths * 12).astype(int)  # Convert depths back to original scale
    unique_depths = np.unique(depths_original)  # Find the unique depths

    class_weights = compute_class_weight(
        class_weight='balanced', 
        classes=unique_depths,  # The unique depths
        y=depths_original       # The original depths
    )

    class_weights = dict(zip(unique_depths, class_weights))  # Create a dictionary of class weights

    # Create and compile the model
    model = create_model()

    # Define early stopping to prevent overfitting
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

    # Train the model
    history = model.fit(
        X_train, y_train,
        epochs=100,
        batch_size=64,
        validation_data=(X_val, y_val),
        class_weight=class_weights,  # Use class weights
        callbacks=[early_stopping],
        verbose=1
    )

    # Save the trained model
    model.save("rubiks_cube_model.h5")
    print("Model saved as 'rubiks_cube_model.h5'")

    return model, history


# -------------------
# Function to preprocess a new cube state (similar to training)
# -------------------
def preprocess_state(state):
    """
    This function takes a raw state (list of 54 integers) and preprocesses it to be compatible with the model input.
    """
    # Scale the state using the same scaler that was used for training
    scaler = joblib.load('scaler.pkl')  # Load the scaler
    state = scaler.transform([state])  # 'state' is a list of 54 integers representing the Rubik's Cube
    return state

# -------------------
# Function to make a prediction on a given state
# -------------------
def make_prediction(state):
    """
    This function preprocesses the input state and predicts the depth (heuristic) using the trained model.
    """
    # Preprocess the input state (scaling and reshaping if necessary)
    processed_state = preprocess_state(state)
    
    # Predict the heuristic (depth) for the given cube state
    predicted_depth = model.predict(processed_state)
    
    # Denormalize predicted depth (back to the original scale)
    predicted_depth = predicted_depth[0][0] * 12  # Assuming depth was normalized to [0, 1] during training
    
    # Return the predicted depth
    return predicted_depth

# -------------------
# Main Execution
# -------------------
if __name__ == "__main__":
    # Step 1: Train the model
    model, history = train_model()

    # Step 2: Example Input (your cube state for prediction)
    new_state = [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 5, 5, 5, 1, 1, 5, 1, 1, 2, 2, 2, 4, 2, 2, 4, 2, 2, 3, 3, 3, 3, 3, 0, 3, 3, 0, 4, 4, 1, 4, 4, 1, 4, 4, 4, 5, 3, 3, 5, 5, 2, 5, 5, 2]  # Your input state

    # Step 3: Make a prediction (heuristic value)
    predicted_depth = make_prediction(new_state)
    print(f"Predicted Depth (Heuristic) for the given state: {predicted_depth}")
