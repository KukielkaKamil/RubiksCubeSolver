import asyncio
import threading
import cv2
import numpy as np
import flet as ft
import base64

# ------------------------
# Color detection utilities
# ------------------------
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

def get_camera_frame_from_existing(frame, center_color=(0, 0, 255)):
    """
    Draw a 3x3 grid on the frame with color detection in each non‑center square.
    The center square is filled with center_color, and four circles are drawn.
    Returns the processed frame and a list of detected colors.
    """
    detected_colors = []
    height, width, _ = frame.shape
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
                # Center square filled with center_color.
                cv2.rectangle(frame, (x1, y1), (x2, y2), center_color, -1)
            else:
                square = frame[y1:y2, x1:x2]
                color = detect_color(square)
                detected_colors.append(color)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, color, (x1, y1 + 42),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    for position, center in circle_positions.items():
        if position == "top":
            circle_color = adjusted_faces_colors[center_color][0]
        elif position == "right":
            circle_color = adjusted_faces_colors[center_color][1]
        elif position == "bottom":
            circle_color = adjusted_faces_colors[center_color][2]
        elif position == "left":
            circle_color = adjusted_faces_colors[center_color][3]
        cv2.circle(frame, center, circle_radius, circle_color, -1)

    return frame, detected_colors

def image_to_base64(img):
    """
    Convert an OpenCV image to Base64.
    """
    if img is None:
        return ""
    try:
        # Encode as JPEG for better performance.
        success, buffer = cv2.imencode(".jpg", img)
        if not success:
            return ""
        return base64.b64encode(buffer).decode("utf-8")
    except Exception:
        return ""

# ------------------------
# get_scan_page function
# ------------------------
def get_scan_page(page: ft.Page, switch_scene, go_back):
    """
    Returns the complete content for the "Scan" page.
    This function initializes the camera, sets up UI elements, and starts an
    asynchronous loop (in a separate event loop) to update the camera view.
    When scanning is complete, it builds the cube string and switches the view.
    """
    # Set page properties.
    page.title = "Live Camera View with Color Detection"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 360
    page.window_height = 640

    # Create a blank image to start.
    empty_img = np.zeros((600, 600, 3), dtype=np.uint8)
    empty_b64 = image_to_base64(empty_img)
    camera_image = ft.Image(
        src_base64=empty_b64,
        width=360,
        height=360,
        fit=ft.ImageFit.SCALE_DOWN
    )

    info_text = ft.Text("", size=14, color=ft.Colors.AMBER_ACCENT_700)

    # Buttons.
    save_button = ft.ElevatedButton("Scan Face")
    next_face_button = ft.Button("Next Face", disabled=True)

    # ------------------------
    # Camera Setup
    # ------------------------
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        cap = cv2.VideoCapture(1)
        if not cap.isOpened():
            return ft.Column(
                [ft.Text("Camera Error: Could not open camera.")],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )

    # ------------------------
    # Scanning Variables
    # ------------------------
    saved_colors = []
    cube_colors = ""
    current_color_index = 0
    running = True

    # Center colors and their symbols.
    center_colors = [
        (0, 255, 0),    # Green
        (0, 0, 255),    # Red
        (255, 0, 0),    # Blue
        (0, 165, 255),  # Orange
        (255, 255, 255),# White
        (0, 255, 255)   # Yellow
    ]
    center_colors_symbols = ['G', 'R', 'B', 'O', 'W', 'Y']

    # ------------------------
    # Event Handlers
    # ------------------------
    def save_colors(e, detected_colors):
        nonlocal saved_colors
        saved_colors.clear()
        saved_colors.extend(detected_colors)
        next_face_button.disabled = False
        if current_color_index == 5:
            info_text.value = "Colors saved. Click 'Finish scanning' to continue."
        else:
            info_text.value = "Colors saved. Click 'Next Face' to continue."
        page.update()

    def change_center_color(e):
        nonlocal current_color_index, cube_colors, running, saved_colors
        info_text.value = ""
        saved_colors_symbols = [color[0] if color != "Unknown" else "?" for color in saved_colors]
        current_face = saved_colors_symbols[:4] + [center_colors_symbols[current_color_index]] + saved_colors_symbols[4:]
        cube_colors += "".join(current_face)
        current_color_index += 1
        next_face_button.disabled = True
        if current_color_index == 5:
            next_face_button.text = "Finish scanning"
        if current_color_index >= 6:
            running = False
            cap.release()
            switch_scene(e, "cube", cube_colors)
        page.update()

    # ------------------------
    # Asynchronous Camera Update
    # ------------------------
    async def update_camera():
        nonlocal current_color_index
        if current_color_index > 5 or not running:
            return

        ret, frame = cap.read()
        if not ret or frame is None:
            return

        # If needed, rotate or convert the frame here.
        if len(frame.shape) == 2:
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_NV21)
            frame_rgb = cv2.cvtColor(frame_bgr, cv2.RNG_NORMAL)
            frame_rgb = cv2.rotate(frame_rgb, cv2.ROTATE_90_CLOCKWISE)
        else:
            frame_rgb = frame

        processed_frame, detected_colors = get_camera_frame_from_existing(
            frame_rgb.copy(), center_color=center_colors[current_color_index]
        )
        save_button.on_click = lambda e, colors=detected_colors: save_colors(e, colors)
        base64_img = image_to_base64(processed_frame)
        if base64_img:
            camera_image.src_base64 = base64_img
            camera_image.update()

    async def camera_loop():
        while running and current_color_index <= 5:
            await update_camera()
            await asyncio.sleep(0.03)

    # ------------------------
    # Start Asyncio Loop in Background Thread
    # ------------------------
    async_loop = asyncio.new_event_loop()

    def start_loop(loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    loop_thread = threading.Thread(target=start_loop, args=(async_loop,), daemon=True)
    loop_thread.start()

    asyncio.run_coroutine_threadsafe(camera_loop(), async_loop)

    # ------------------------
    # Cleanup on Page Disposal
    # ------------------------
    def cleanup():
        nonlocal running
        running = False
        if cap.isOpened():
            cap.release()
        async_loop.call_soon_threadsafe(async_loop.stop)
    page.on_dispose = cleanup

    # ------------------------
    # Layout / Content
    # ------------------------
    content = ft.Column(
        [
            camera_image,
            info_text,
            ft.Row(
                [save_button, next_face_button],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    next_face_button.on_click = change_center_color

    return content
