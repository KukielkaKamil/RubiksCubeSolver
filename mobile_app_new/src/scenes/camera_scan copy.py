import cv2
import numpy as np
import flet as ft
import base64
import time
import threading

def detect_color(square):
    hsv = cv2.cvtColor(square, cv2.COLOR_BGR2HSV)
    color_ranges = {
        "White": ((0, 0, 150), (180, 100, 255)),
        "Yellow": ((20, 100, 100), (30, 255, 255)),
        "Red": ((0, 100, 100), (10, 255, 255)),
        "Green": ((35, 50, 50), (85, 255, 255)),
        "Blue": ((90, 50, 50), (130, 255, 255)),
        "Orange": ((5, 100, 100), (15, 255, 255)),
    }
    for color, (lower, upper) in color_ranges.items():
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        if np.sum(mask) > 0:
            return color
    return "Unknown"

adjusted_faces_colors = {
    (0, 255, 0): ((255, 255, 255), (0, 0, 255), (0, 255, 255), (0, 165, 255)),
    (0, 0, 255): ((255, 255, 255), (255, 0, 0), (0, 255, 255), (0, 255, 0)),
    (255, 0, 0): ((255, 255, 255), (0, 165, 255), (0, 255, 255), (0, 0, 255)),
    (0, 165, 255): ((255, 255, 255), (0, 255, 0), (0, 255, 255), (255, 0, 0)),
    (255, 255, 255): ((255, 0, 0), (0, 0, 255), (0, 255, 0), (0, 165, 255)),
    (0, 255, 255): ((0, 255, 0), (0, 0, 255), (255, 0, 0), (0, 165, 255)),
}

def get_camera_frame(cap, center_color=(0, 0, 255)):
    """Capture a frame, do some color detection drawing, return (img, detected_colors)."""
    ret, img = cap.read()
    if not ret or img is None:
        return None, []

    img = cv2.resize(img, (600, 600))
    detected_colors = []

    height, width, _ = img.shape
    square_size = 30
    spacing = 50
    total_grid_width = 3 * square_size + 2 * spacing
    total_grid_height = 3 * square_size + 2 * spacing
    x_offset = (width - total_grid_width) // 2
    y_offset = (height - total_grid_height) // 2

    circle_radius = 15
    circle_positions = {
        "top": (width // 2, y_offset - circle_radius * 2),
        "right": (x_offset + total_grid_width + circle_radius * 2, height // 2),
        "bottom": (width // 2, y_offset + total_grid_height + circle_radius * 2),
        "left": (x_offset - circle_radius * 2, height // 2),
    }

    for row in range(3):
        for col in range(3):
            x1 = x_offset + col * (square_size + spacing)
            y1 = y_offset + row * (square_size + spacing)
            x2 = x1 + square_size
            y2 = y1 + square_size

            if row == 1 and col == 1:
                # The center block, fill with "center_color"
                cv2.rectangle(img, (x1, y1), (x2, y2), center_color, -1)
            else:
                square = img[y1:y2, x1:x2]
                color = detect_color(square)
                detected_colors.append(color)
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, color, (x1, y1 + 42), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    for position, center in circle_positions.items():
        if position == "top":
            circle_color = adjusted_faces_colors[center_color][0]
        elif position == "right":
            circle_color = adjusted_faces_colors[center_color][1]
        elif position == "bottom":
            circle_color = adjusted_faces_colors[center_color][2]
        elif position == "left":
            circle_color = adjusted_faces_colors[center_color][3]
        cv2.circle(img, center, circle_radius, circle_color, -1)

    return img, detected_colors

def image_to_base64(img):
    if img is None:
        return ""
    try:
        # Ensure conversion from BGR to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        _, buffer = cv2.imencode(".png", img_rgb)
        return base64.b64encode(buffer).decode("utf-8")
    except Exception as e:  
        print(f"Error encoding image: {e}")
        return ""

def get_scan_page(page: ft.Page, switch_scene, go_back):
    page.title = "Rubik's Cube Scanner"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Android-specific camera setup
    def android_camera_init():
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            # Try different camera indexes for Android
            for i in [1, 2, 3]:
                cap = cv2.VideoCapture(i, cv2.CAP_ANDROID)
                if cap.isOpened():
                    break
        return cap

    cap = android_camera_init()
    if not cap.isOpened():
        return ft.Column([ft.Text("Camera Error: Could not access camera.")])

    # Image display parameters
    target_width = 400  # Reduced resolution for mobile performance
    target_height = 400

    # Orientation handling
    orientation_lock = threading.Lock()
    current_orientation = 0  # 0, 90, 180, 270

    def rotate_image(image, angle):
        # Helper function for proper rotation
        if angle == 0:
            return image
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        return cv2.warpAffine(image, M, (w, h))

    def update_camera():
        nonlocal current_orientation
        while running:
            try:
                ret, frame = cap.read()
                if not ret:
                    continue

                # Android-specific orientation handling
                with orientation_lock:
                    frame = rotate_image(frame, current_orientation)
                    frame = cv2.flip(frame, 1)  # Mirror front-facing camera

                # Resize and process
                frame = cv2.resize(frame, (target_width, target_height))
                processed_frame, _ = process_frame(frame)

                # Convert to base64
                img_base64 = image_to_base64(processed_frame)

                # Update UI safely using page.update()
                def update_ui():
                    camera_image.src_base64 = img_base64
                    page.update()

                page.update()
                page.add(ft.Text(""))  # Workaround to force UI refresh
                page.schedule_task(update_ui)

            except Exception as e:
                print(f"Camera error: {str(e)}")
            time.sleep(0.033)  # ~30 FPS

    def image_to_base64(img):
        try:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            _, buffer = cv2.imencode(".jpg", img_rgb, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            return base64.b64encode(buffer).decode("utf-8")
        except Exception as e:
            print(f"Encoding error: {str(e)}")
            return ""

    # Simplified processing for mobile
    def process_frame(frame):
        # Add your grid drawing and color detection logic here
        # Consider simplifying for mobile performance
        return frame, []

    # UI components
    camera_image = ft.Image(
        width=target_width,
        height=target_height,
        fit=ft.ImageFit.CONTAIN
    )

    # Orientation controls (optional)
    def rotate_clockwise(e):
        nonlocal current_orientation
        with orientation_lock:
            current_orientation = (current_orientation + 90) % 360

    orientation_button = ft.IconButton(
        icon=ft.icons.ROTATE_RIGHT,
        on_click=rotate_clockwise
    )

    # Start camera thread
    running = True
    camera_thread = threading.Thread(target=update_camera, daemon=True)
    camera_thread.start()

    # Cleanup when page closes
    def cleanup():
        nonlocal running
        running = False
        if cap.isOpened():
            cap.release()

    page.on_close = cleanup

    return ft.Column(
        [
            camera_image,
            orientation_button,
            # Add your other controls here
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )