import flet as ft
import httpx
import asyncio
import threading
from scenes.cube import cube_to_list
from helperFunctions.RubiksCube import RubiksCube as rb
from scenes.cube import CELL_SIZE, GRID_SIZE
import random
import math


initial_content = ft.Column()
player_cells=[]

player_cube = rb()

URL = 'http://127.0.0.1:5000/kociemba'

def get_results_page(page:ft.Page, switch_scene, go_back):
    
    initial_content.controls.append(ft.ProgressRing(width=32,height=32,stroke_width=2))

    # asyncio.run(test())
    threading.Thread(target=lambda: asyncio.run(send_request(page))).start()

    return initial_content


    
def change_color(cell:ft.Container,color_symbol):

    match color_symbol:
        case "🟩":
            color = ft.colors.GREEN
        case "🟥":
            color = ft.colors.RED
        case "🟦": 
            color = ft.colors.BLUE
        case "🟧":
            color = ft.colors.ORANGE
        case "⬜":
            color = ft.colors.WHITE
        case "🟨":
            color = ft.colors.YELLOW

    cell.bgcolor = color

player_container = ft.Container()
def create_player():
    global player_container
    bg_grid, bg_cells = create_grid()
    front_grid, front_cells = create_grid()

    # vertical_strip, vstrp_cels = create_grid(1,3,3.5,0)
    # horizontal_strip, hstrp_cels = create_grid(3,1,0,3.5)
    for i in range(9):
        change_color(front_cells[i],player_cube.cube[i])


    grid_stack = ft.Stack(
        controls=[bg_grid, front_grid],
        animate_rotation = ft.animation.Animation(300)
    )
    player_container = grid_stack
    player_cells.append(front_cells)
    player_cells.append(bg_cells)
    # player_cells.append(vstrp_cels)
    # player_cells.append(hstrp_cels)
    return ft.Container(grid_stack, width=GRID_SIZE, height=GRID_SIZE)



async def send_request(page):
    cube = cube_to_list()
    params={'cubestring':cube}

    async with httpx.AsyncClient() as client:
        response = await client.get(URL, params=params)

    if response.status_code == 200:
        result_text = response.json().get('result', 'No result found')
        player_cube.decode_state_lett(cube_to_list())
        text = ft.Text(result_text)
        player = create_player()
        initial_content.controls.clear()
        initial_content.controls.append(text)
        initial_content.controls.append(player)
        page.update()
        await asyncio.sleep(1)
        
        # posible_moves = ['R','R`','L','L`','U','U`','D','D`']
        # moves_to_do = random.choices(posible_moves,k=5)


        # for move in moves_to_do:
        #     await play_move(page,move)
        await player_U(page)
        await player_D(page)
        await player_F(page)
        await player_R(page)
        await player_B(page)


        
        page.update()


def create_grid(height=3,width=3,offset_x=0,offset_y=0):
        grid_cells = []
        grid_rows = []
        for row in range(height):
            row_controls = []
            for col in range(width):
                cell = ft.Container(
                    bgcolor=ft.colors.BLACK,
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
            color = ft.colors.GREEN
        case "🟥":
            color = ft.colors.RED
        case "🟦": 
            color = ft.colors.BLUE
        case "🟧":
            color = ft.colors.ORANGE
        case "⬜":
            color = ft.colors.WHITE
        case "🟨":
            color = ft.colors.YELLOW
    return color

async def slide_side(page,indexes:dict,offset_x,offset_y):
    for cell in indexes.keys():
        player_cells[0][cell].animate_offset = None
        player_cells[1][cell].animate_offset = None
        player_cells[0][cell].offset = ft.Offset(offset_x,offset_y)
        player_cells[1][cell].offset = ft.Offset(0,0)
        player_cells[1][cell].bgcolor=player_cells[0][cell].bgcolor
        player_cells[0][cell].bgcolor = get_color_at(indexes[cell])
    page.update()
    await asyncio.sleep(0.3)
    for fcell in indexes.keys():
        player_cells[0][fcell].animate_offset = ft.animation.Animation(300)
        player_cells[1][fcell].animate_offset = ft.animation.Animation(300)
    page.update()
    await asyncio.sleep(0.1)
    for fcell in indexes.keys():
        player_cells[0][fcell].offset = ft.Offset(0,0)
        player_cells[1][fcell].offset = ft.Offset(-1 * offset_x,-1 * offset_y)
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
    for cell in range(9):
        player_container.rotate = ft.Rotate(0.5 * math.pi,ft.alignment.center)
    page.update()
    await asyncio.sleep(0.3)

    for cell in range(9):
        player_container.animate_rotation = None
        player_container.rotate = ft.Rotate(0,ft.alignment.center)
    page.update()
    player_cube.F()

    for cell in range(9):
        player_cells[0][cell].bgcolor = get_color_at(cell)
        # player_container.animate_rotation = ft.animation.Animation(300)

async def player_F_prime(page):
    for cell in range(9):
        player_container.rotate = ft.Rotate(-0.5 * math.pi,ft.alignment.center)
    page.update()
    await asyncio.sleep(0.3)

    for cell in range(9):
        player_container.animate_rotation = None
        player_container.rotate = ft.Rotate(0,ft.alignment.center)
    page.update()
    player_cube.F()

    for cell in range(9):
        player_cells[0][cell].bgcolor = get_color_at(cell)

async def player_B(page):
    for cell in range(9):
        player_container.controls[0].animate_rotation = ft.animation.Animation(300)
        player_cells[1][cell].offset = ft.Offset(0,0)
    page.update()
    await asyncio.sleep(0.1)

    for cell in range(9):
        player_cells[1][cell].bgcolor = ft.colors.BLACK
        player_container.controls[0].rotate = ft.Rotate(-0.5 * math.pi,ft.alignment.center)
    page.update()
    await asyncio.sleep(0.3)

    player_container.controls[0].animate_rotation = None
    player_container.controls[0].rotate = ft.Rotate(0,ft.alignment.center)
    page.update()
    player_cube.B()

async def player_B_prime(page):
    for cell in range(9):
        player_container.controls[0].animate_rotation = ft.animation.Animation(300)
        player_cells[1][cell].offset = ft.Offset(0,0)
    page.update()
    await asyncio.sleep(0.1)

    for cell in range(9):
        player_cells[1][cell].bgcolor = ft.colors.BLACK
        player_container.controls[0].rotate = ft.Rotate(0.5 * math.pi,ft.alignment.center)
    page.update()
    await asyncio.sleep(0.3)

    player_container.controls[0].animate_rotation = None
    player_container.controls[0].rotate = ft.Rotate(0,ft.alignment.center)
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

# async def test():
#     await asyncio.sleep(3)
#     print('test')