import flet as ft
import asyncio


CELL_SIZE = 50
GRID_SIZE = (CELL_SIZE + 10) * 3
face_positions = [0,0,0] #0-3 - F,R,B,L Faces; 0-1 U Face 0-1 D Face
cube_faces = []
def get_cube_page(page:ft.Page, switch_scene, go_back):
    current_color = "white"
    page.appbar = ft.AppBar(
            leading=ft.IconButton(ft.icons.ARROW_BACK,on_click=go_back),
            title=ft.Text("Rubik's Cube Solver")
        )

    def change_color(e,color):
        nonlocal current_color
        current_color = color

    def color_cell(e, cell):
        if face_positions[1] == 1:
            current_face = 4
        elif face_positions[2] == 1:
            current_face = 5
        else:
            current_face = face_positions[0]
        
        cube_faces[current_face][cell].bgcolor = current_color
        page.update()

    async def next_face(e):
        if face_positions[1] != 1 and face_positions[2] != 1:
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
            page.update()

            # Update the face position
            face_positions[0] = next_grid


    async def prev_face(e):
        if face_positions[1] != 1 and face_positions[2] != 1:
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
            page.update()

            # Update the face position
            face_positions[0] = prev_grid




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
        if face_positions[2] == 1:
            for cell in cube_faces[0]:
                cell.offset = ft.transform.Offset(0, 0)
            
            bottom_grid = cube_faces[5]
            for cell in bottom_grid:
                cell.offset = ft.transform.Offset(0,3.5)
            page.update()
            face_positions[2] = 0

        else:
            current_grid = face_positions[0] % 4
            for cell in cube_faces[current_grid]:
                cell.offset = ft.transform.Offset(0, 3.5)
            
            top_grid = cube_faces[4]
            for cell in top_grid:
                cell.offset = ft.transform.Offset(0,0)
            page.update()
            face_positions[1] = 1
            await asyncio.sleep(0.3)
            await reset_front_faces()

    async def down_face(e):
        if face_positions[1] == 1:
        #     reset_front_faces()
            for cell in cube_faces[0]:
                cell.offset = ft.transform.Offset(0, 0)
            
            top_grid = cube_faces[4]
            for cell in top_grid:
                cell.offset = ft.transform.Offset(0,-3.5)
            page.update()
            face_positions[1] = 0
        else:
            current_grid = face_positions[0] % 4
            for cell in cube_faces[current_grid]:
                cell.offset = ft.transform.Offset(0, -3.5)
            
            top_grid = cube_faces[5]
            for cell in top_grid:
                cell.offset = ft.transform.Offset(0,0)
            page.update()
            face_positions[2] = 1
            await asyncio.sleep(0.3)
            await reset_front_faces()


    def create_grid(bgcolor,offset_x, offset_y):
        grid_cells = []
        grid_rows = []
        for row in range(3):
            row_controls = []
            for col in range(3):
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
        
    if len(cube_faces) == 0:
        grid_1 = create_grid("green",0,0)
        grid_2 = create_grid("red",3.5,0)
        grid_3 = create_grid("blue",3.5,0)
        grid_4 = create_grid("orange",-3.5,0)
        grid_5 = create_grid("white",0,-3.5)
        grid_6 = create_grid("yellow",0,3.5)
        control_grid= create_grid(ft.colors.TRANSPARENT,0,0)
    else:
        grid_1 = recreate_grid(0)
        grid_2 = recreate_grid(1)
        grid_3 = recreate_grid(2)
        grid_4 = recreate_grid(3)
        grid_5 = recreate_grid(4)
        grid_6 = recreate_grid(5)
        control_grid = recreate_grid(6)
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
    content = ft.Column([
        ft.Row(
            [
                ft.Text("Wprowadź układ kostki",text_align=ft.TextAlign.CENTER,size=24)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Row(
            [
                ft.IconButton(
                    ft.icons.KEYBOARD_ARROW_UP,
                    icon_color = "black",
                    bgcolor="white",
                    on_click=up_face
                ),
            ],
            ft.MainAxisAlignment.CENTER
        ),
        ft.Row(
            [
                ft.IconButton(
                    ft.icons.KEYBOARD_ARROW_LEFT,
                    icon_color = "black",
                    bgcolor="orange",
                    on_click = prev_face,
                    
                ),
                cube_container,
                ft.IconButton(
                    ft.icons.KEYBOARD_ARROW_RIGHT,
                    icon_color = "black",
                    bgcolor="red",
                    on_click=next_face,
                    
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Row(
            [
                ft.IconButton(
                    ft.icons.KEYBOARD_ARROW_DOWN,
                    icon_color = "black",
                    bgcolor="yellow",
                    on_click= down_face,
                ),
            ],
            ft.MainAxisAlignment.CENTER
        ),
        ft.Row(
            [
                ft.Container(
                    content=ft.Text("0"),
                    bgcolor="red",
                    width = 50,
                    height=50,
                    padding=5,
                    border_radius=ft.border_radius.all(100),
                    col=1,
                    alignment=ft.alignment.center,
                    on_click=lambda e: change_color(e,"red")
                ),
                ft.Container(
                    content=ft.Text("0"),
                    bgcolor="Blue",
                    width = 50,
                    height=50,
                    padding=5,
                    border_radius=ft.border_radius.all(100),
                    col=1,
                    alignment=ft.alignment.center,
                    on_click=lambda e: change_color(e,"blue",)
                ),
                ft.Container(
                    content=ft.Text("0"),
                    bgcolor="Yellow",
                    width = 50,
                    height=50,
                    padding=5,
                    border_radius=ft.border_radius.all(100),
                    col=1,
                    alignment=ft.alignment.center,
                    on_click= lambda e: change_color(e,"yellow")
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Row(
            [
                ft.Container(
                    content=ft.Text("0"),
                    bgcolor="white",
                    width = 50,
                    height=50,
                    padding=5,
                    border_radius=ft.border_radius.all(100),
                    col=1,
                    alignment=ft.alignment.center,
                    on_click=lambda e: change_color(e,"white")
                ),
                ft.Container(
                    content=ft.Text("0"),
                    bgcolor="orange",
                    width = 50,
                    height=50,
                    padding=5,
                    border_radius=ft.border_radius.all(100),
                    col=1,
                    alignment=ft.alignment.center,
                    on_click=lambda e: change_color(e,"orange")
                ),
                ft.Container(
                    content=ft.Text("0"),
                    bgcolor="green",
                    width = 50,
                    height=50,
                    padding=5,
                    border_radius=ft.border_radius.all(100),
                    col=1,
                    alignment=ft.alignment.center,
                    on_click=lambda e: change_color(e,"green")
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.FilledButton("Dalej",on_click = lambda e: switch_scene(e, "algorithm"))
    ])
        

    def test(e):
        size = 50
        full_size = (size + 10) * 3
        for grid in cube_faces:
            for cell in grid:
                cell.width = size
                cell.height = size
        for container in grid_stack.controls:
            container.width = full_size
            container.height = full_size
        cube_container.width = full_size
        cube_container.height = full_size
        page.update()



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
    scube = ''.join(cube)
    print(scube)
    return(scube)
    
    