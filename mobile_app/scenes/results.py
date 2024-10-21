import flet as ft
import httpx
import asyncio
import threading
from scenes.cube import cube_to_list

URL = 'http://127.0.0.1:5000/kociemba'

def get_results_page(page:ft.Page, switch_scene, go_back):
    
    initial_content = ft.Column(
        [
            ft.ProgressRing(width=32,height=32,stroke_width=2)
        ],
    )  

    # asyncio.run(test())
    threading.Thread(target=lambda: asyncio.run(send_request(page))).start()

    return initial_content

def kociemba_cube():
    input_str = cube_to_list()

    starting_indexes=[36,9,0,45,27,18]
    #Step 1 reorder faces
    new_str=''
    for i in range(6):
        start = starting_indexes[i]
        end = start+9
        print(input_str[start:end])
        new_str += input_str[start:end]

    
    # Step 2: Transform the string
    transform_dict = {'G': 'F', 'R': 'R', 'B': 'B', 'O': 'L', 'W': 'U', 'Y': 'D'}
    transformed_str = ''.join([transform_dict[char] for char in new_str])
    
    return transformed_str



async def send_request(page):
    cube = kociemba_cube()
    print(cube)
    params={'cubestring':cube}

    async with httpx.AsyncClient() as client:
        response = await client.get(URL, params=params)

    result_text = response.json().get('result', 'No result found')
    
    text = ft.Text(result_text)
    

    page.add(text)

    page.update()

# async def test():
#     await asyncio.sleep(3)
#     print('test')