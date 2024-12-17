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
def get_camera_frame(cap, center_color=(0, 0, 255)):
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

            # If it's the center block, skip color detection and fill with the specified color
            if row == 1 and col == 1:
                cv2.rectangle(img, (x1, y1), (x2, y2), center_color, -1)  # Filled rectangle
            else:
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
def get_scan_page(page: ft.Page, switch_scene, go_back):
    page.title = "Live Camera View with Color Detection"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Array to store colors of a face
    saved_colors = []

    # Storing cube as a string
    cube_colors = ""

    # Image widget to display the camera feed
    camera_image = ft.Image(width=600, height=600)

    # Button to save colors
    save_button = ft.ElevatedButton("Scan Face", on_click=lambda e: save_colors(e, saved_colors))

    next_face_button = ft.Button("Next Face", disabled=True)

    # Open the camera once at the start
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return ft.Text("Camera Error: Could not open camera.")

    # Center block color (initially red)
    center_colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 165, 0), (255, 255, 255)]
    center_colors_symbols = ['R', 'G', 'B', 'Y', 'O', 'W']
    current_color_index = 0

    # Function to update the live camera feed
    def update_camera():
    # Define an async background function for the camera update loop
        async def run_camera_update():
            while True:
                img, detected_colors = get_camera_frame(cap, center_color=center_colors[current_color_index])
                if img is not None:
                    # Convert the image to base64 and set it to the Image widget
                    base64_img = image_to_base64(img)
                    camera_image.src_base64 = base64_img
                    save_button.on_click = lambda e: save_colors(e, detected_colors)
                    page.update()

                # Sleep asynchronously for 100ms before the next frame update
                await asyncio.sleep(0.1)

        # Run the async background task
        page.run_task(run_camera_update)


    update_camera()

    def save_colors(event, detected_colors):
        saved_colors.clear()
        saved_colors.extend(detected_colors)
        next_face_button.disabled = False
        print("Saved colors:", saved_colors)
        page.update()

    def change_center_color(event):
        nonlocal current_color_index, cube_colors
        saved_colors_symbols = [color[0] for color in saved_colors]
        current_face = saved_colors_symbols[:4] + [center_colors_symbols[current_color_index]] + saved_colors_symbols[4:]
        cube_colors += "".join(current_face)
        helper_index = current_color_index +1
        current_color_index = (current_color_index + 1) % len(center_colors)
        print(cube_colors)
        next_face_button.disabled = True
        if current_color_index == 5:
            next_face_button.text = "Finish scanning"
        if helper_index >= 6:
            switch_scene(event,'cube',cube_colors)
        page.update()

    next_face_button.on_click = change_center_color

    # Return the camera feed and buttons
    return ft.Column([
        camera_image,
        ft.Row([save_button, next_face_button])
    ])
