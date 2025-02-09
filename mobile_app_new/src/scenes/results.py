import flet as ft
import asyncio
from scenes.cube import cube_to_list
from helperFunctions.RubiksCube import RubiksCube as rb
from scenes.cube import CELL_SIZE, GRID_SIZE
from copy import deepcopy
import math
import aiohttp

initial_content = ft.Column()
player_cells=[]
move_sequence = []
move_index = 0
current_page = None
is_playing = False
text_elements = []
player_cube = rb()
is_button_locked = False
intial_cube = deepcopy(player_cube)
curr_endpoint=None


URL_prefix = "http://192.168.43.169:5000"

def reset_values():
    global player_cells, move_sequence, move_index, is_playing, text_elements
    player_cells = []
    move_sequence = []
    move_index = 0
    is_playing = False
    text_elements = []

def get_results_page(page:ft.Page, switch_scene, go_back,endpoint):
    global current_page, curr_endpoint,player_cube
    reset_values()
    player_cube = rb()
    current_page = page
    curr_endpoint = endpoint
    initial_content.controls.clear()
    initial_content.controls.insert(0,ft.ProgressRing(width=32,height=32,stroke_width=2))

    # asyncio.run(test())
    asyncio.run(send_request(page))


    return initial_content


    
def change_color(cell:ft.Container,color_symbol):

    match color_symbol:
        case "🟩":
            color = ft.Colors.GREEN
        case "🟥":
            color = ft.Colors.RED
        case "🟦": 
            color = ft.Colors.BLUE
        case "🟧":
            color = ft.Colors.ORANGE
        case "⬜":
            color = ft.Colors.WHITE
        case "🟨":
            color = ft.Colors.YELLOW

    cell.bgcolor = color

player_container = ft.Container()

def create_player():
    global player_container
    bg_grid, bg_cells = create_grid()
    front_grid, front_cells = create_grid()
    for i in range(9):
        change_color(front_cells[i],player_cube.cube[i])


    grid_stack = ft.Stack(
        controls=[bg_grid, front_grid],
        animate_rotation = ft.animation.Animation(300)
    )
    player_container = grid_stack
    player_cells.append(front_cells)
    player_cells.append(bg_cells)
    player_content = ft.Container(grid_stack, width=GRID_SIZE, height=GRID_SIZE)
    
    controler_buttons = ft.Row(
            [
                ft.IconButton(
                    icon=ft.icons.KEYBOARD_DOUBLE_ARROW_RIGHT,
                    icon_color="blue400",
                    icon_size=20,
                    tooltip="Next move",
                    on_click= lambda e, page=current_page: asyncio.run(next_move(e,page))
                ),
                ft.IconButton(
                    icon=ft.icons.KEYBOARD_DOUBLE_ARROW_LEFT,
                    icon_color="pink600",
                    icon_size=40,
                    tooltip="Prev move",
                    on_click= lambda e, page=current_page: asyncio.run(prev_move(e,page))
                ),ft.IconButton(
                    icon=ft.icons.PLAY_ARROW,
                    icon_color="blue400",
                    icon_size=20,
                    tooltip="Play",
                    on_click= lambda e, page=current_page: asyncio.run(play_sequence(e,page))
                ),
                ft.IconButton(
                    icon=ft.icons.PAUSE,
                    icon_color="pink600",
                    icon_size=40,
                    tooltip="Pause",
                    on_click= pause_player
                ),
            ]
        )
    return ft.Column([
        player_content,
        controler_buttons
    ])




import aiohttp  # Import aiohttp instead of httpx

# The previous send_request function modified to use aiohttp:
async def send_request(page):
    global move_sequence, text_elements, URL_prefix, curr_endpoint

    cube = cube_to_list()
    params = {'cubestring': cube}
    URL = URL_prefix + curr_endpoint

    try:
        # Replace httpx with aiohttp
        async with aiohttp.ClientSession() as session:
            # Sending the GET request with parameters
            async with session.get(URL, params=params) as response:
                if response.status == 200:
                    # Ensure JSON response has the expected structure
                    response_data = await response.json()
                    result_text = response_data.get('result', None)

                    if result_text:
                        # Update the UI with the result
                        move_sequence = result_text
                        player_cube.decode_state_lett(cube_to_list())

                        player = create_player()
                        initial_content.controls.clear()
                        initial_content.controls.append(player)
                        moves_container = ft.Row(wrap=True, spacing=5)
                        for letter in move_sequence:
                            text_container = ft.Container(
                                content=ft.Text(
                                    value=letter,
                                    size=20,
                                    color="white",
                                    weight=ft.FontWeight.BOLD,
                                    text_align="center",
                                ),
                                width=30,
                                height=30,
                                bgcolor="transparent",
                                alignment=ft.alignment.center,
                                border_radius=5,
                                animate=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
                            )
                            text_elements.append(text_container)
                            moves_container.controls.append(text_container)
                        update_colors(0)
                        initial_content.controls.append(moves_container)

                        page.update()
                    else:
                        raise ValueError("Invalid response from server: Missing 'result' field")
                else:
                    # Handling server errors (non-200 responses)
                    error_message = await response.json()  # Use async to read JSON response
                    error_message = error_message.get('error', 'An error occurred')
                    raise Exception(f"Server Error: {error_message}")

    except aiohttp.ClientConnectionError:
        # Handle connection errors
        show_error_dialog(page, "Connection Error", "Unable to connect to the server. Please check if the server is running or check your network connection.")
    except aiohttp.ClientTimeout:
        # Handle timeout errors
        show_error_dialog(page, "Timeout Error", "The request timed out. The server may be too slow or unreachable. Please try again later.")
    except aiohttp.InvalidURL:
        # Handle invalid URL errors
        show_error_dialog(page, "Invalid URL", "The server URL is invalid. Please verify the server address.")
    except Exception as e:
        # Handle other exceptions
        show_error_dialog(page, "Error", f"An error occurred: {str(e)}")


def update_colors(index):
    global current_page
    for i, text_container in enumerate(text_elements):
        if i == index:
            # Highlight the current letter
            text_container.bgcolor = "#f39c12"
            text_container.content.color = "black"
        elif i > index:
            # Letters after the current one
            text_container.bgcolor = "transparent"
            text_container.content.color = "#aaaaaa"
        else:
            # Letters before the current one
            text_container.bgcolor = "transparent"
            text_container.content.color = "white"
    current_page.update()


def show_error_dialog(page, title, message):
    """Displays an error dialog."""
    dialog = ft.AlertDialog(
        title=ft.Text(title),
        content=ft.Text(message),
        actions=[
            ft.TextButton("OK", on_click=lambda e: close_dialog(page, dialog))
        ]
    )
    page.overlay.append(dialog)
    dialog.open = True
    page.update()


def close_dialog(page, dialog):
    """Closes an error dialog."""
    dialog.open = False
    page.update()
    page.overlay.remove(dialog)

async def next_move(e, page):
    global move_index, move_sequence, is_button_locked
    if is_button_locked:  # Prevent execution if the button is locked
        return

    if move_index < len(move_sequence):
        is_button_locked = True  # Lock the button temporarily
        await play_move(page, move_sequence[move_index])
        move_index += 1
        update_colors(move_index)
        await asyncio.sleep(0.3)  # Allow 300ms delay before unlocking
        is_button_locked = False  # Unlock the button

async def prev_move(e, page):
    global move_index, move_sequence, is_button_locked
    if is_button_locked:  # Prevent execution if the button is locked
        return

    if move_index > 0:
        is_button_locked = True  # Lock the button temporarily
        move_index -= 1
        update_colors(move_index)
        prev_move = move_sequence[move_index]
        if prev_move.endswith("`"):
            inv_move = prev_move[:-1]  # Return the character without the backtick
        else:
            inv_move = prev_move + "`"  # Add a backtick to the character
        await play_move(page, inv_move)
        await asyncio.sleep(0.3)  # Allow 300ms delay before unlocking
        is_button_locked = False  # Unlock the button


async def play_sequence(e,page):
    global is_playing,move_sequence
    is_playing = True
    for m in range(len(move_sequence)):
        if is_playing:
            await next_move(e,page)
            await asyncio.sleep(0.5)
    is_playing= False

def pause_player(e):
    global is_playing
    is_playing = False

def reset_player(e,page):
    global is_playing,move_index, initial_cube
    is_playing=False
    move_index=0

    for i in range(9):
        change_color(player_cells[0][i],player_cube.cube[i])
    

def create_grid(height=3,width=3,offset_x=0,offset_y=0):
        grid_cells = []
        grid_rows = []
        for row in range(height):
            row_controls = []
            for col in range(width):
                cell = ft.Container(
                    bgcolor=ft.Colors.PURPLE,
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
        # cube_faces.append(grid_cells)
        return ft.Container(
            content=ft.Column(controls=grid_rows, alignment=ft.MainAxisAlignment.CENTER),
            width=GRID_SIZE,
            height=GRID_SIZE,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            rotate=ft.Rotate(0,ft.alignment.center) ), grid_cells

def get_color_at(index):
    position = player_cube.cube[index]

    match position:
        case "🟩":
            color = ft.Colors.GREEN
        case "🟥":
            color = ft.Colors.RED
        case "🟦": 
            color = ft.Colors.BLUE
        case "🟧":
            color = ft.Colors.ORANGE
        case "⬜":
            color = ft.Colors.WHITE
        case "🟨":
            color = ft.Colors.YELLOW
    return color

async def slide_side(page, indexes: dict, offset_x, offset_y):
    # Disable animations temporarily to set the initial offset
    for cell in indexes.keys():
        player_cells[0][cell].animate_offset = None
        player_cells[1][cell].animate_offset = None
        player_cells[0][cell].offset = ft.Offset(offset_x, offset_y)
        player_cells[1][cell].offset = ft.Offset(0, 0)
        player_cells[1][cell].bgcolor = player_cells[0][cell].bgcolor
        player_cells[0][cell].bgcolor = get_color_at(indexes[cell])
    page.update()
    
    await asyncio.sleep(0.3)  # Wait for visual update

    # Re-enable animations for the return transition
    for fcell in indexes.keys():
        player_cells[0][fcell].animate_offset = ft.animation.Animation(300)
        player_cells[1][fcell].animate_offset = ft.animation.Animation(300)
    page.update()
    
    await asyncio.sleep(0.1)

    # Reset offsets for return animation
    for fcell in indexes.keys():
        player_cells[0][fcell].offset = ft.Offset(0, 0)
        player_cells[1][fcell].offset = ft.Offset(-1 * offset_x, -1 * offset_y)
    page.update()
    await asyncio.sleep(0.3)



    
async def player_R(page):
    indexes = {
        2:47,
        5:50,
        8:53
    }
    await slide_side(page,indexes,0,3.5)
    player_cube.R()

async def player_R_prime(page):
    indexes = {
        2:38,
        5:41,
        8:44
    }
    await slide_side(page,indexes,0,-3.5)
    player_cube.R_prime()

async def player_L(page):
    indexes = {
        0:36,
        3:39,
        6:42
    }
    await slide_side(page,indexes,0,-3.5)
    player_cube.L()

async def player_L_prime(page):
    indexes = {
        0:45,
        3:48,
        6:51
    }
    await slide_side(page,indexes,0,3.5)
    player_cube.L_prime()

async def player_U(page):
    indexes = {
        0:9,
        1:10,
        2:11
    }
    await slide_side(page,indexes,3.5,0)
    player_cube.U()

async def player_U_prime(page):
    indexes = {
        0:27,
        1:28,
        2:29
    }
    await slide_side(page,indexes,-3.5,0)
    player_cube.U_prime()

async def player_D(page):
    indexes = {
        6:33,
        7:34,
        8:35
    }
    await slide_side(page,indexes,-3.5,0)
    player_cube.D()

async def player_D_prime(page):
    indexes = {
        6:15,
        7:16,
        8:17
    }
    await slide_side(page,indexes,3.5,0)
    player_cube.D_prime()

async def player_F(page):
    # for cell in range(9):
    player_container.rotate = ft.Rotate(0.5 * math.pi,ft.alignment.center)
    page.update()
    await asyncio.sleep(0.3)

    # for cell in range(9):
    player_container.animate_rotation = None
    page.update()
    player_container.rotate = ft.Rotate(0,ft.alignment.center)
    page.update()
    player_cube.F()
    for cell in range(9):
        player_cells[0][cell].bgcolor = get_color_at(cell)
    page.update()
    await asyncio.sleep(0.3)
    player_container.animate_rotation = ft.animation.Animation(300)
    page.update()


async def player_F_prime(page):

    player_container.rotate = ft.Rotate(-0.5 * math.pi,ft.alignment.center)
    page.update()
    await asyncio.sleep(0.3)
    player_container.animate_rotation = None
    page.update()
    player_container.rotate = ft.Rotate(0,ft.alignment.center)
    page.update()

    player_cube.F_prime()
    for cell in range(9):
        player_cells[0][cell].bgcolor = get_color_at(cell)
    page.update()
    await asyncio.sleep(0.3)
    player_container.animate_rotation = ft.animation.Animation(300)
    page.update()

async def player_B(page):
    for cell in range(9):
        player_cells[1][cell].bgcolor = ft.Colors.PURPLE
        player_cells[1][cell].offset = ft.Offset(0, 0)
    player_container.controls[0].animate_rotation = None
    player_container.controls[0].rotate = ft.Rotate(0.5 * math.pi, ft.alignment.center)
    page.update()
    await asyncio.sleep(0.1)

    player_container.controls[0].animate_rotation = ft.animation.Animation(300)
    page.update()
    player_container.controls[0].rotate = ft.Rotate(0, ft.alignment.center)
    await asyncio.sleep(0.3)
    page.update()
    player_cube.B()



async def player_B_prime(page):

    for cell in range(9):
        player_cells[1][cell].bgcolor = ft.Colors.PURPLE
        player_cells[1][cell].offset = ft.Offset(0, 0)
    player_container.controls[0].animate_rotation = None
    player_container.controls[0].rotate = ft.Rotate(-0.5 * math.pi, ft.alignment.center)
    page.update()
    await asyncio.sleep(0.1)

    player_container.controls[0].animate_rotation = ft.animation.Animation(300)
    page.update()
    player_container.controls[0].rotate = ft.Rotate(0, ft.alignment.center)
    await asyncio.sleep(0.3)
    page.update()
    player_cube.B()


async def play_move(page,move):
    match move:
        case "R":
            await player_R(page)
        case "R`":
            await player_R_prime(page)
        case 'L':
            await player_L(page)
        case 'L`':
            await player_L_prime(page)
        case 'U':
            await player_U(page)
        case 'U`':
            await player_U_prime(page)
        case 'D':
            await player_D(page)
        case 'D`':
            await player_D_prime(page)
        case 'F':
            await player_F(page)
        case 'F`':
            await player_F_prime(page)
        case 'B':
            await player_B(page)
        case 'B`':
            await player_B_prime(page)