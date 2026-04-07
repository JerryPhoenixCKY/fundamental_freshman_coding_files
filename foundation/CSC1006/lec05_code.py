# CSC1006 lecture 5 supplementary codes
# By Fangxun Zhong, 2025.03
# Go to Google Colab, open a new notebook file and paste the below codes on it
# Click "Runtime" and select "Run All" (or Ctrl+F9) to run
# After completion, the resultant estimated function layout is drawn

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tensorflow as tf
from tensorflow import layers, models

# Generate training data
def generate_data(num_samples=1000):
    x = np.random.uniform(-10, 10, num_samples)
    y = np.random.uniform(-10, 10, num_samples)
    z = x**2 + 2*y**2  # Target function: z = x^2 + 2*y^2
    return x, y, z

# Build the neural network
def build_model():
    model = models.Sequential([
        layers.Input(shape=(2,)),  # Input layer with 2 inputs
        layers.Dense(3, activation='relu'),  # First hidden layer with 3 neurons
        layers.Dense(3, activation='relu'),  # Second hidden layer with 3 neurons
        layers.Dense(1)  # Output layer with 1 output
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

# Train the neural network
def train_model(model, x_train, y_train, z_train, epochs=100):
    # Combine x and y into input data
    inputs = np.stack((x_train, y_train), axis=1)  # Convert to shape (num_samples, 2)
    history = model.fit(inputs, z_train, epochs=epochs, verbose=1, batch_size=32)
    return history

# Test the neural network
def test_model(model, x_test, y_test):
    inputs = np.stack((x_test, y_test), axis=1)  # Convert to shape (num_samples, 2)
    z_pred = model.predict(inputs)
    return z_pred

# Main function
def main():
    # Generate training data
    x_train, y_train, z_train = generate_data(1000)
    
    # Build the neural network
    model = build_model()
    
    # Train the neural network
    print("Training the model...")
    train_model(model, x_train, y_train, z_train, epochs=100)
    
    # Test the neural network
    print("Testing the model...")
    x_test, y_test = np.meshgrid(np.linspace(-10, 10, 50), np.linspace(-10, 10, 50))
    x_test_flat = x_test.ravel()  # Flatten the grid points
    y_test_flat = y_test.ravel()  # Flatten the grid points
    z_true = x_test_flat**2 + 2*y_test_flat**2  # True z values
    z_pred = test_model(model, x_test_flat, y_test_flat).ravel()  # Predicted z values by the neural network

    # Plot the results
    fig = plt.figure(figsize=(12, 6))
    
    # True function visualization
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.scatter(x_test_flat, y_test_flat, z_true, c=z_true, cmap='viridis', s=5)
    ax1.set_title('True Function')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_zlabel('z')
    
    # Neural network fitted function visualization
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.scatter(x_test_flat, y_test_flat, z_pred, c=z_pred, cmap='viridis', s=5)
    ax2.set_title('Predicted Function by Neural Network')
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    ax2.set_zlabel('z')
    
    plt.show()

# Run the main function
if __name__ == "__main__":
    main()