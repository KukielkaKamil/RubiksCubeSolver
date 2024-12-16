import cv2
import numpy as np
import flet as ft
import base64
import asyncio

# Define the function to detect color in a square
def detect_color(square):
    hsv = cv2.cvtColor(square, cv2.COLOR_BGR2HSV)

    color_ranges = {
        "White": ((0, 0, 150), (180, 100, 255)),
        "Yellow": ((20, 100, 100), (30, 255, 255)),
        "Red": ((0, 100, 100), (10, 255, 255)),
        "Green": ((35, 50, 50), (85, 255, 255)),
        "Blue": ((90, 50, 50), (130, 255, 255)),
        "Orange": ((5, 100, 100), (15, 255, 255))
    }

    for color, (lower, upper) in color_ranges.items():
        lower_bound = np.array(lower)
        upper_bound = np.array(upper)
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        
        if np.sum(mask) > 0:
            return color

    return "Unknown"


# Function to capture the camera feed and return it as an image
def get_camera_frame(cap):
    ret, img = cap.read()
    if not ret:
        print("Failed to grab frame")
        return None

    img = cv2.resize(img, (600, 600))  # Resize for better performance
    
    # Process image (overlay grid and colors)
    detected_colors = []
    height, width, _ = img.shape
    square_size = 30
    spacing = 50
    total_grid_width = 3 * square_size + 2 * spacing
    total_grid_height = 3 * square_size + 2 * spacing
    x_offset = (width - total_grid_width) // 2
    y_offset = (height - total_grid_height) // 2

    for row in range(3):
        for col in range(3):
            x1 = x_offset + col * (square_size + spacing)
            y1 = y_offset + row * (square_size + spacing)
            x2 = x1 + square_size
            y2 = y1 + square_size
            square = img[y1:y2, x1:x2]
            color = detect_color(square)
            detected_colors.append(color)
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, color, (x1 + 5, y1 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    return img, detected_colors


# Function to convert an image to base64 string
def image_to_base64(img):
    _, buffer = cv2.imencode('.png', img)
    base64_data = base64.b64encode(buffer).decode('utf-8')
    return base64_data


# Flet app logic
async def main(page: ft.Page):
    page.title = "Live Camera View with Color Detection"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Array to store colors
    saved_colors = []

    # Image widget to display the camera feed
    camera_image = ft.Image(width=600, height=600)

    # Button to save colors
    save_button = ft.ElevatedButton("Scan Face", on_click=lambda e: save_colors(e, saved_colors))

    # Open the camera once at the start
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Function to update the live camera feed and process frames
    async def update_camera():
        while True:
            img, detected_colors = get_camera_frame(cap)

            if img is not None:
                # Convert the image to base64 and set it to the Image widget
                base64_img = image_to_base64(img)
                camera_image.src_base64 = base64_img  # Set the base64-encoded image

                # Store the colors when button is pressed
                save_button.on_click = lambda e: save_colors(e, detected_colors)

                page.update()

            # Sleep for 100ms before refreshing the image
            await asyncio.sleep(0.1)

    # Start the camera feed update loop in the background
    asyncio.create_task(update_camera())

    def save_colors(event, detected_colors):
        # Store the detected colors
        saved_colors.clear()
        saved_colors.extend(detected_colors)
        print("Saved colors:", saved_colors)

    # Add widgets to the page
    page.add(camera_image, save_button)


# Run the app
ft.app(target=main)
