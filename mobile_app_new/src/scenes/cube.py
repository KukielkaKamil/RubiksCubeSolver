import flet as ft
import asyncio
from helperFunctions.test import RubiksCube as rb
import random


CELL_SIZE = 50
GRID_SIZE = (CELL_SIZE + 10) * 3
face_positions = [0,0,0] #0-3 - F,R,B,L Faces; 0-1 U Face 0-1 D Face
cube_faces = []
color_elements = []
color_counts={
    "green" : 1,
    "red": 1,
    "blue": 1,
    "orange": 1,
    "white": 1,
    "yellow": 1
}
is_button_locked = False
#Loading th scene
def get_cube_page(page:ft.Page, switch_scene, go_back, cube_string = ""):
    current_color = "white"
    prev_color_element = None
    selected_color_element = None
    page.appbar = ft.AppBar(
            leading=ft.IconButton(ft.Icons.ARROW_BACK,on_click=go_back),
            title=ft.Text("Rubik's Cube Solver")
        )

    #Changes the current color that is used for painting
    def change_color(e,color):
        nonlocal current_color,selected_color_element,prev_color_element
        current_color = color
        if selected_color_element != e.control:
            prev_color_element = selected_color_element
            selected_color_element = e.control
        selected_color_element.border = ft.border.all(4, ft.Colors.PURPLE) if not None else None
        if prev_color_element:
            prev_color_element.border = None

        page.update()

    # Updates the count of a color buttons
    def update_color_counts():
        for e in color_elements:
            e.content.value = color_counts[e.bgcolor]
        
    #Changes colors of a cell
    def color_cell(e, cell):
        if face_positions[1] == 1:
            current_face = 4
        elif face_positions[2] == 1:
            current_face = 5
        else:
            current_face = face_positions[0]
        
        facet_color = cube_faces[current_face][cell].bgcolor
        if facet_color == ft.Colors.GREY:
            color_counts[current_color] += 1
        elif facet_color != current_color:
            color_counts[current_color] += 1
            color_counts[facet_color] -= 1
        update_color_counts()
        cube_faces[current_face][cell].bgcolor = current_color
        page.update()

    async def next_face(e):
        global is_button_locked
        if is_button_locked:
            return
        if face_positions[1] != 1 and face_positions[2] != 1:
            is_button_locked = True
            current_grid = face_positions[0] % 4  # Current face index (0 to 3)
            next_grid = (current_grid + 1) % 4  # Next grid when moving forward

            # print(f"NEXT GRID : {next_grid} ")

            # Reset the positions for the grids off-screen, ready for the next transition
            prev_grid = (current_grid - 1) % 4  # Previous grid when moving forward
            for cell in cube_faces[prev_grid]:
                cell.animate_offset = None
                cell.offset = ft.Offset(3.5, 0)  # Ready to come from the right

            # Move the current grid out (to the left for 'next')
            for cell in cube_faces[current_grid]:
                cell.offset = ft.transform.Offset(-3.5, 0)  # Move out to the left

            # Move the new grid in (from the right for 'next')
            for cell in cube_faces[next_grid]:
                cell.offset = ft.transform.Offset(0, 0)      # Move in from the right

            # Update the page to reflect changes
            page.update()

            await asyncio.sleep(0.3)

            # Animate the transition for the new position
            for cell in cube_faces[prev_grid]:
                cell.animate_offset = ft.animation.Animation(300)

            face_positions[0] = next_grid
            update_move_buttons(0)
            page.update()
            await asyncio.sleep(0.3)  # Allow 300ms delay before unlocking
            is_button_locked = False

    async def prev_face(e):
        global is_button_locked
        if is_button_locked:
            return
        if face_positions[1] != 1 and face_positions[2] != 1:
            is_button_locked = True
            current_grid = face_positions[0] % 4  # Current face index (0 to 3)
            prev_grid = (current_grid + 3) % 4  # Previous grid when moving backward

            # print(f"PREV GRID : {prev_grid} ")

            # Reset the positions for the grids off-screen, ready for the next transition
            next_grid = (current_grid + 2) % 4  # Next grid when moving backward
            for cell in cube_faces[next_grid]:
                cell.animate_offset = None
                cell.offset = ft.Offset(-3.5, 0)  # Ready to come from the left

            # Move the current grid out (to the right for 'prev')
            for cell in cube_faces[current_grid]:
                cell.offset = ft.transform.Offset(3.5, 0)  # Move out to the right

            # Move the new grid in (from the left for 'prev')
            for cell in cube_faces[prev_grid]:
                cell.offset = ft.transform.Offset(0, 0)      # Move in from the left

            # Update the page to reflect changes
            page.update()

            await asyncio.sleep(0.3)

            # Animate the transition for the new position
            for cell in cube_faces[next_grid]:
                cell.animate_offset = ft.animation.Animation(300)
            
            # Update the face position
            face_positions[0] = prev_grid
            update_move_buttons(0)
            page.update()

            await asyncio.sleep(0.3)  # Allow 300ms delay before unlocking
            is_button_locked = False




    async def reset_front_faces():
        top_offset = 3.5 if face_positions[1] == 1 else -3.5
    # Reset offsets for each face
        for i in range(0, 4):
            for cell in cube_faces[i]:
                cell.animate_offset = None  # Disable animations first
                if i == 0:
                    cell.offset = ft.transform.Offset(0, top_offset)  # Position front face
                else:
                    cell.offset = ft.transform.Offset(3.5, 0)  # Move other faces off-screen

    # First update to apply the immediate changes
        page.update()
        await asyncio.sleep(0.3)
    # Now enable animations for a smooth reset transition
        for i in range(0, 4):
            for cell in cube_faces[i]:
                if i == 0:
                    cell.animate_offset = ft.animation.Animation(300)
                else:
                    cell.animate_offset = ft.animation.Animation(300)
                    cell.offset = ft.transform.Offset(3.5, 0)  # Ensure off-screen position

    # Final page update after setting up animations
        page.update()

    # Reset face positions
        face_positions[0] = 0
        

            

    async def up_face(e):
        global is_button_locked
        if is_button_locked:
            return
        if face_positions[2] == 1:
            for cell in cube_faces[0]:
                cell.offset = ft.transform.Offset(0, 0)
            
            bottom_grid = cube_faces[5]
            for cell in bottom_grid:
                cell.offset = ft.transform.Offset(0,3.5)
            page.update()
            face_positions[2] = 0
            face_positions[0] = 0
            update_move_buttons(0)
            page.update()

        else:
            current_grid = face_positions[0] % 4
            for cell in cube_faces[current_grid]:
                cell.offset = ft.transform.Offset(0, 3.5)
            
            top_grid = cube_faces[4]
            for cell in top_grid:
                cell.offset = ft.transform.Offset(0,0)
            face_positions[1] = 1
            update_move_buttons(1)
            page.update()
            await asyncio.sleep(0.3)
            await reset_front_faces()
        await asyncio.sleep(0.3)  # Allow 300ms delay before unlocking
        is_button_locked = False

    async def down_face(e):
        global is_button_locked
        if is_button_locked:
            return
        if face_positions[1] == 1:
        #     reset_front_faces()
            for cell in cube_faces[0]:
                cell.offset = ft.transform.Offset(0, 0)
            
            top_grid = cube_faces[4]
            for cell in top_grid:
                cell.offset = ft.transform.Offset(0,-3.5)
            page.update()
            face_positions[1] = 0
            face_positions[0] = 0
            update_move_buttons(0)
            page.update()
        else:
            current_grid = face_positions[0] % 4
            for cell in cube_faces[current_grid]:
                cell.offset = ft.transform.Offset(0, -3.5)
            
            top_grid = cube_faces[5]
            for cell in top_grid:
                cell.offset = ft.transform.Offset(0,0)
            face_positions[2] = 1
            update_move_buttons(2)
            page.update()
            await asyncio.sleep(0.3)
            await reset_front_faces()
        await asyncio.sleep(0.3)  # Allow 300ms delay before unlocking
        is_button_locked = False
    up_button = ft.IconButton(
                    ft.Icons.KEYBOARD_ARROW_UP,
                    icon_color = "black",
                    bgcolor="white",
                    on_click=up_face
                )
    
    down_button = ft.IconButton(
                    ft.Icons.KEYBOARD_ARROW_DOWN,
                    icon_color = "black",
                    bgcolor="yellow",
                    on_click= down_face,
                )

    right_button = ft.IconButton(
                    ft.Icons.KEYBOARD_ARROW_RIGHT,
                    icon_color = "black",
                    bgcolor="red",
                    on_click=next_face,
                    
                )
    
    left_button = ft.IconButton(
                    ft.Icons.KEYBOARD_ARROW_LEFT,
                    icon_color = "black",
                    bgcolor="orange",
                    on_click = prev_face,
                    
                )
    
    def update_move_buttons(state):


        match face_positions[0]:
            case 0:
                up_button.bgcolor = ft.Colors.WHITE
                up_button.visible = True
                right_button.bgcolor = ft.Colors.RED
                right_button.visible = True
                left_button.bgcolor = ft.Colors.ORANGE
                left_button.visible = True
                down_button.bgcolor = ft.Colors.YELLOW
                down_button.visible = True
            case 1:
                right_button.bgcolor = ft.Colors.BLUE
                left_button.bgcolor = ft.Colors.GREEN
            case 2:
                right_button.bgcolor = ft.Colors.ORANGE
                left_button.bgcolor = ft.Colors.RED
            case 3:
                right_button.bgcolor = ft.Colors.GREEN
                left_button.bgcolor = ft.Colors.BLUE
        if state == 1:
            up_button.visible = False
            right_button.visible = False
            left_button.visible = False
            down_button.bgcolor = ft.Colors.GREEN
        elif state == 2:
            up_button.bgcolor = ft.Colors.GREEN
            right_button.visible = False
            left_button.visible = False
            down_button.visible = False



    def create_grid(bgcolor,offset_x, offset_y):
        grid_cells = []
        grid_rows = []
        for row in range(3):
            row_controls = []
            for col in range(3):
                if bgcolor == ft.Colors.TRANSPARENT and not (col == 1 and row == 1):
                    cell = ft.Container(
                        bgcolor=bgcolor,
                        width=CELL_SIZE,
                        height=CELL_SIZE,
                        border_radius=5,
                        alignment=ft.alignment.center,
                        offset=ft.transform.Offset(offset_x, offset_y),  # Initially off-screen
                        animate_offset=ft.animation.Animation(300),
                        on_click= lambda e, cell= row*3 + col: color_cell(e, cell),
                    )
                elif row == 1 and col == 1:
                    cell = ft.Container(
                        bgcolor=bgcolor,
                        width=CELL_SIZE,
                        height=CELL_SIZE,
                        border_radius=5,
                        alignment=ft.alignment.center,
                        offset=ft.transform.Offset(offset_x, offset_y),  # Initially off-screen
                        animate_offset=ft.animation.Animation(300),
                    )
                else:
                    cell = ft.Container(
                        bgcolor=ft.Colors.GREY,
                        width=CELL_SIZE,
                        height=CELL_SIZE,
                        border_radius=5,
                        alignment=ft.alignment.center,
                        offset=ft.transform.Offset(offset_x, offset_y),  # Initially off-screen
                        animate_offset=ft.animation.Animation(300),
                    )

                row_controls.append(cell)
                grid_cells.append(cell)
            grid_rows.append(ft.Row(controls=row_controls, alignment=ft.MainAxisAlignment.CENTER))
        cube_faces.append(grid_cells)
        return ft.Container(
            content=ft.Column(controls=grid_rows, alignment=ft.MainAxisAlignment.CENTER),
            width=GRID_SIZE,
            height=GRID_SIZE,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            rotate=ft.Rotate(0,ft.alignment.center)
        )
    
    def recreate_grid(face):
        grid_rows =[]
        for row in range(3):
            start = 3*row
            end = start + 3
            # grid_rows.append(cube_faces[face][start:2])
            grid_rows.append(ft.Row(controls=cube_faces[face][start:end], alignment=ft.MainAxisAlignment.CENTER))
        return ft.Container(
            content=ft.Column(controls=grid_rows, alignment=ft.MainAxisAlignment.CENTER),
            width=GRID_SIZE,
            height=GRID_SIZE,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            rotate=ft.Rotate(0,ft.alignment.center)
        )
    
    def load_from_string(string):
        color_map = {
            "W" : (ft.Colors.WHITE,'white'),
            "G": (ft.Colors.GREEN,'green'),
            "R": (ft.Colors.RED,'red'),
            "B": (ft.Colors.BLUE,'blue'),
            "O": (ft.Colors.ORANGE,'orange'),
            "Y": (ft.Colors.YELLOW,'yellow'),
            "?": (ft.Colors.GREY,'grey')
        }
        for key in color_counts:
            color_counts[key] = 0
        for i,c  in enumerate(string):
            face = i//9
            facelet = i % 9
            cube_faces[face][facelet].bgcolor = color_map[c][0]
            if color_map[c][1] != 'grey':
                color_counts[color_map[c][1]] += 1
        update_color_counts()

    if len(cube_faces) == 0:
        grid_1 = create_grid("green",0,0)
        grid_2 = create_grid("red",3.5,0)
        grid_3 = create_grid("blue",3.5,0)
        grid_4 = create_grid("orange",-3.5,0)
        grid_5 = create_grid("white",0,-3.5)
        grid_6 = create_grid("yellow",0,3.5)
        control_grid= create_grid(ft.Colors.TRANSPARENT,0,0)
    else:
        grid_1 = recreate_grid(0)
        grid_2 = recreate_grid(1)
        grid_3 = recreate_grid(2)
        grid_4 = recreate_grid(3)
        grid_5 = recreate_grid(4)
        grid_6 = recreate_grid(5)
        control_grid = recreate_grid(6)

    if len(cube_string) != 0:
        load_from_string(cube_string)
    # Wrap both grids in a Stack to overlay them
    grid_stack = ft.Stack(
        controls=[grid_1, grid_2,grid_3,grid_4,grid_5,grid_6,control_grid],

    )
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
    cube_container= ft.Container(
                    grid_stack,
                    width=GRID_SIZE,
                    height=GRID_SIZE,
                )
    
    for color in color_counts.keys():
        element = ft.Container(
                    content=ft.Text("1",color="black"),
                    bgcolor=color,
                    width = 50,
                    height=50,
                    padding=5,
                    border_radius=ft.border_radius.all(100),
                    col=1,
                    alignment=ft.alignment.center,
                    border=ft.border.all(4, ft.Colors.PURPLE) if color == "white" else None,
                    on_click=lambda e, color = color: change_color(e,color)
                )
        color_elements.append(element)
    selected_color_element = next(e for e in color_elements if e.bgcolor == "white")
    def validate_cube(e):
        validator_cube = rb()
        try:
            cube_string= cube_to_list()
        except TypeError as te:
            return "Wprowadź wszystkie kolory"
        print(f"Cube_string: {cube_string}")
        validator_cube.decode_state_lett(cube_string)
        return validator_cube.verify()
    

    def go_next(e):
        """
        Validate the cube and switch to the next scene if valid.

        Args:
            e: The event that triggered this function.
        """
        validate_result = validate_cube(e)
        if validate_result == 'CUBE_OK':
            switch_scene(e, "algorithm")
        else:
            show_error_dialog(validate_result)

    def show_error_dialog(validate_result):
        """
        Show an error dialog with the validation result.

        Args:
            validate_result: The result of the cube validation.
        """
        dialog = ft.AlertDialog(
            title=ft.Text("Błąd"),
            content=ft.Text(validate_result),
            actions=[
                ft.TextButton("OK", on_click=lambda e: close_dialog(dialog))
            ]
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def close_dialog(dialog):
        """
        Close the error dialog.

        Args:
            dialog: The dialog to be closed.
        """
        dialog.open = False
        page.update()
        page.overlay.remove(dialog)

    def scramble_cube(e):
        scrambled_cube = rb()
        random_moves = random.randint(5,20)
        scrambled_cube.scramble(random_moves)
        cube_string = scrambled_cube.encode_to_cubestring()
        load_from_string(cube_string)
        page.update()
        print(cube_string)


    content = ft.Column([
        ft.Row(
            [
                ft.Text("Wprowadź układ kostki",text_align=ft.TextAlign.CENTER,size=24)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Row(
            [
                up_button
            ],
            ft.MainAxisAlignment.CENTER
        ),
        ft.Row(
            [
                left_button,
                cube_container,
                right_button
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Row(
            [
                down_button
            ],
            ft.MainAxisAlignment.CENTER
        ),
        ft.Row(
            [
                color_elements[0],
                color_elements[1],
                color_elements[2],
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Row(
            [
                color_elements[3],
                color_elements[4],
                color_elements[5],
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Row(
            [
                ft.FilledButton("Użyj aparatu",on_click = lambda e: switch_scene(e, "scan")),
                ft.FilledButton("Dalej",on_click =go_next),
                ft.FilledButton("Polosuj",on_click = scramble_cube)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    ])

    return content



def color_to_letter(color):
    match color:
        case "white":
            return "W"
        case "green":
            return "G"
        case "red":
            return "R"
        case "blue":
            return "B"
        case "orange":
            return "O"
        case "yellow":
            return "Y"
    

def cube_to_list():
    cube = list()
    for grid in range(6):
        for cell in cube_faces[grid]:
            color = color_to_letter(cell.bgcolor)
            cube.append(color)
    try:
        scube = ''.join(cube)
    except TypeError as tr:
        raise tr
    print(scube)
    return scube