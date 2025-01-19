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
        _, buffer = cv2.imencode(".png", img)
        return base64.b64encode(buffer).decode("utf-8")
    except Exception as e:
        return ""

def get_scan_page(page: ft.Page, switch_scene, go_back):
    page.title = "Live Camera View with Color Detection"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    running = True
    saved_colors = []
    cube_colors = ""
    current_color_index = 0

    # ---- DEBUG UI ----
    debug_log = ft.TextField(
        value="",
        multiline=True,
        read_only=True,
        expand=False,
        width=600,
        height=150,
        label="Debug Output",
    )

    def log_debug(msg):
        """Append a line of debug text to the debug_log UI."""
        debug_log.value += msg + "\n"
        page.update()

    # ---- CAMERA IMAGE DISPLAY ----
    empty_img = np.zeros((600, 600, 3), dtype=np.uint8)
    _, buf = cv2.imencode(".png", empty_img)
    empty_b64 = base64.b64encode(buf).decode("utf-8")

    camera_image = ft.Image(
        src_base64=empty_b64,
        width=600,
        height=600,
        fit=ft.ImageFit.CONTAIN
    )

    # ---- BUTTONS ----
    save_button = ft.ElevatedButton("Scan Face")
    next_face_button = ft.Button("Next Face", disabled=True)

    # ---- TEXT ----
    info_text = ft.Text("", size=14, color=ft.Colors.AMBER_ACCENT_700)

    # ---- OPEN CAMERA ----
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        log_debug("Error: Could not open camera (index=0). Trying index=1...")
        cap = cv2.VideoCapture(1)
        if not cap.isOpened():
            log_debug("Error: Could not open camera (index=1). No camera available.")
            return ft.Column([ft.Text("Camera Error: Could not open camera."), debug_log])

    log_debug("Camera opened successfully!")

    # Center colors
    center_colors = [(0, 255, 0), (0, 0, 255), (255, 0, 0), (0, 165, 255), (255, 255, 255), (0, 255, 255)]
    center_colors_symbols = ['G', 'R', 'B', 'O', 'W', 'Y']

    def update_camera():
        """Capture and show one frame, plus some debug info."""
        nonlocal current_color_index
        if current_color_index <= 5 and running:
            # Grab raw frame from camera
            ret, raw_frame = cap.read()

            if not ret or raw_frame is None:
                log_debug("Failed to grab frame from camera.")
                return

            # Print debug info about the raw frame
            avg_pixel = np.mean(raw_frame)
            log_debug(f"Raw frame shape: {raw_frame.shape}, average pixel: {avg_pixel:.2f}")

            # Resize and do color detection drawing
            raw_frame = cv2.resize(raw_frame, (600, 600))
            img, detected_colors = get_camera_frame_from_existing(raw_frame, center_color=center_colors[current_color_index])

            if img is not None:
                # Additional debug
                log_debug(f"Processed average pixel: {np.mean(img):.2f}")
                base64_img = image_to_base64(img)
                log_debug(f"Base64 length: {len(base64_img)}")

                if base64_img:
                    camera_image.src_base64 = base64_img
                    # link the "scan face" button to the newly detected colors
                    save_button.on_click = lambda e: save_colors(e, detected_colors)
                    page.update()

    def get_camera_frame_from_existing(frame, center_color=(0, 0, 255)):
        # Just a helper that reuses your "get_camera_frame" logic, 
        # but we skip the actual cap.read() step because we already have the frame in memory.
        # We'll do minimal changes here:
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
                    cv2.rectangle(frame, (x1, y1), (x2, y2), center_color, -1)
                else:
                    square = frame[y1:y2, x1:x2]
                    color = detect_color(square)
                    detected_colors.append(color)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, color, (x1, y1 + 42), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

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

    def save_colors(event, detected_colors):
        saved_colors.clear()
        saved_colors.extend(detected_colors)
        next_face_button.disabled = False
        if current_color_index == 5:
            info_text.value = "Colors saved. Click 'Finish scanning' to continue."
        else:
            info_text.value = "Colors saved. Click 'Next Face' to continue."
        page.update()

    def change_center_color(event):
        nonlocal current_color_index, cube_colors, running
        info_text.value = ""
        saved_colors_symbols = [color[0] for color in saved_colors]
        current_face = saved_colors_symbols[:4] + [center_colors_symbols[current_color_index]] + saved_colors_symbols[4:]
        cube_colors += "".join(current_face)
        current_color_index += 1
        next_face_button.disabled = True
        if current_color_index == 5:
            next_face_button.text = "Finish scanning"
        if current_color_index >= 6:
            running = False
            cap.release()
            switch_scene(event, "cube", cube_colors)
        page.update()

    def cleanup():
        nonlocal running
        running = False
        if cap.isOpened():
            cap.release()

    # Thread function that updates camera repeatedly
    def start_camera_loop():
        while running and current_color_index <= 5:
            update_camera()
            time.sleep(0.1)

    # Create a one-shot button to see if we can get any frame
    def snap_once(e):
        update_camera()

    # Start the capture loop in a separate thread
    camera_thread = threading.Thread(target=start_camera_loop, daemon=True)
    camera_thread.start()

    save_button.on_click = lambda e: save_colors(e, saved_colors)
    next_face_button.on_click = change_center_color
    page.on_dispose = cleanup

    # Additional button for manual snapshot
    snap_button = ft.ElevatedButton("Snap Once", on_click=snap_once)

    # Layout
    content = ft.Column(
        [
            camera_image,
            info_text,
            ft.Row(
                [
                    save_button,
                    next_face_button,
                    snap_button,
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            debug_log,  # Our debug text area
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )
    return content
