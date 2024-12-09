import cv2
import numpy as np
import flet as ft

# Function to detect colors on a Rubik's Cube face
def detect_colors(image):
    color_ranges = {
        "red": [(0, 100, 100), (10, 255, 255)],        # Adjusted for better red detection
        "green": [(40, 50, 50), (90, 255, 255)],       # Adjusted for better green detection
        "blue": [(90, 50, 50), (130, 255, 255)],      # Blue range is fine for most lighting
        "yellow": [(15, 150, 150), (40, 255, 255)],    # Adjusted for more yellow detection
        "orange": [(5, 150, 150), (20, 255, 255)],    # Slight adjustment for orange
        "white": [(0, 0, 150), (180, 40, 255)],       # Adjusted for white detection
    }

    def get_color(hsv_pixel):
        hsv_pixel = hsv_pixel.astype("uint8")
        print(f"HSV Pixel: {hsv_pixel}")
        for color, (lower, upper) in color_ranges.items():
            lower = np.array(lower, dtype="uint8")
            upper = np.array(upper, dtype="uint8")
            if cv2.inRange(hsv_pixel.reshape(1, 1, 3), lower, upper):
                return color
        return "unknown"



    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    height, width, _ = image.shape
    grid_size = min(height, width) // 3
    face_colors = []

    for row in range(3):
        row_colors = []
        for col in range(3):
            x_start, y_start = col * grid_size, row * grid_size
            x_end, y_end = x_start + grid_size, y_start + grid_size
            region = hsv[y_start:y_end, x_start:x_end]
            avg_color = np.mean(region, axis=(0, 1)).astype("uint8")
            row_colors.append(get_color(avg_color))

            # Debugging: Draw the grid and print HSV value
            cv2.rectangle(image, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)

        face_colors.append(row_colors)

    print("Detected colors:", face_colors)
    return face_colors

# Flet UI for the Rubik's Cube Scanner
def main(page: ft.Page):
    def scan_face(e):
        cap = cv2.VideoCapture(0)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                page.snack_bar = ft.SnackBar(ft.Text("Error: Unable to access camera"))
                page.snack_bar.open = True
                page.update()
                break

            frame_resized = cv2.resize(frame, (300, 300))
            detected_colors = detect_colors(frame_resized)

            # Show grid visualization for debugging (real-time)
            cv2.imshow("Rubik's Cube Real-Time", frame)

            # Update UI with detected colors (real-time)
            update_cube_ui(detected_colors)

            # Exit condition for real-time video feed (press 'q' to quit)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def update_cube_ui(colors):
        cube_grid.controls.clear()
        color_map = {
            "red": ft.Colors.RED,
            "green": ft.Colors.GREEN,
            "blue": ft.Colors.BLUE,
            "yellow": ft.Colors.YELLOW,
            "orange": ft.Colors.ORANGE,
            "white": ft.Colors.WHITE,
            "unknown": ft.Colors.GREY,
        }
        
        for row in colors:
            row_widgets = []
            for color in row:
                cell = ft.Container(
                    width=50,
                    height=50,
                    bgcolor=color_map.get(color, ft.Colors.GREY),
                    border_radius=5,
                )
                row_widgets.append(cell)
            cube_grid.controls.append(ft.Row(row_widgets, spacing=5))
        page.update()

    page.title = "Rubik's Cube Real-Time Scanner"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Cube grid container
    cube_grid = ft.Column(spacing=5)

    # Button to start the scan
    scan_button = ft.ElevatedButton("Start Scanning", on_click=scan_face)

    # Layout
    page.add(
        ft.Column(
            [
                ft.Text("Rubik's Cube Real-Time Scanner", size=30, weight="bold"),
                scan_button,
                cube_grid,
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)
