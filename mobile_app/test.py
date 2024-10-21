import flet as ft
import random

# Function to create a grid (3x3 face of the cube)
def create_face(face_colors):
    return ft.Row(
        [
            ft.Column(
                [
                    ft.Container(
                        bgcolor=color,
                        width=50,
                        height=50,
                        border_radius=5,
                        margin=5
                    ) for color in row
                ]
            ) for row in face_colors
        ]
    )

# Example colors for each face of the cube
front_face = [
    ["red", "red", "red"],
    ["red", "red", "red"],
    ["red", "red", "red"]
]

top_face = [
    ["yellow", "yellow", "yellow"],
    ["yellow", "yellow", "yellow"],
    ["yellow", "yellow", "yellow"]
]

right_face = [
    ["blue", "blue", "blue"],
    ["blue", "blue", "blue"],
    ["blue", "blue", "blue"]
]

# Update colors for animation (example of a 90-degree rotation)
def rotate_faces():
    global front_face, top_face, right_face
    # Rotate logic: you can implement actual Rubik's rotation here
    front_face = [[random.choice(["red", "green", "blue", "yellow", "white", "orange"]) for _ in range(3)] for _ in range(3)]
    top_face = [[random.choice(["red", "green", "blue", "yellow", "white", "orange"]) for _ in range(3)] for _ in range(3)]
    right_face = [[random.choice(["red", "green", "blue", "yellow", "white", "orange"]) for _ in range(3)] for _ in range(3)]

def main(page: ft.Page):
    page.title = "3D Rubik's Cube Simulation"
    
    # Create initial faces
    front = create_face(front_face)
    top = create_face(top_face)
    right = create_face(right_face)

    # Container to hold the cube with adjusted margins for 3D effect
    cube = ft.Stack(
        [
            ft.Container(content=top, left=50, top=0),   # Offset top face
            ft.Container(content=front, left=0, top=100),  # Front face
            ft.Container(content=right, left=150, top=100)  # Offset right face
        ]
    )

    # Function to handle rotation and re-render
    def animate_cube(e):
        rotate_faces()  # Update face colors
        # Rebuild the cube with new colors
        front.controls = create_face(front_face).controls
        top.controls = create_face(top_face).controls
        right.controls = create_face(right_face).controls
        page.update()

    # Button to trigger rotation
    rotate_button = ft.ElevatedButton("Rotate Cube", on_click=animate_cube)

    # Add cube and button to the page
    page.add(cube, rotate_button)

# Start the Flet app
ft.app(target=main)
