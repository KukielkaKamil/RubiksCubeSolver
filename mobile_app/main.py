import flet as ft
from math import pi
import asyncio
from scenes.settings import get_page
from scenes.cube import get_cube_page
from scenes.algorithm_selection import get_algorithm_page
from scenes.results import get_results_page




def main(page: ft.Page):
    scene_stack = []

    def switch_scene(e, scene_name):
        # Push current scene to stack before switching
        if scene_stack:
            current_scene = scene_stack[-1]
            if current_scene != scene_name:  # Avoid duplicates if it's the same scene
                scene_stack.append(scene_name)
        else:
            scene_stack.append(scene_name)

        load_scene(scene_name)

    # Function to go back to the previous scene
    def go_back(e):
        if len(scene_stack) > 1:
            scene_stack.pop()  # Remove current scene
            previous_scene = scene_stack[-1]  # Load the previous scene
            load_scene(previous_scene)
        else:
            print("No previous scene")
        

    def load_scene(scene_name):
        page.controls.clear()  # Clear the current scene
        if scene_name == "main_scene":
            page.appbar=None
            page.add(main_content)
        if scene_name == "settings":
            page.add(get_page(page, switch_scene, go_back))  # Load Scene 1
        if scene_name == 'cube':
            page.add(get_cube_page(page, switch_scene, go_back))
        if scene_name == 'algorithm':
            page.add(get_algorithm_page(page,switch_scene,go_back))
        if scene_name == 'results':
            page.add(get_results_page(page,switch_scene,go_back))
        page.update()

    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.ALWAYS

    logo = ft.Image(f"/logo.png", width=200, height= 200,fit=ft.ImageFit.CONTAIN)


    
    main_content= ft.Column(
        [
            ft.ResponsiveRow(
            [logo],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
            ft.SafeArea(ft.Text("Hello, Flet!")),
            ft.FilledButton("Rozpocznie",on_click = lambda e: switch_scene(e, "cube")),
            ft.FilledButton("Ustawienia",on_click = lambda e: switch_scene(e, "settings")),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    page.add(main_content)

    scene_stack.append("main_scene")



ft.app(main)
