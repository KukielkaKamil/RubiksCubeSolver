import flet as ft

from math import pi
import asyncio

# Your scene imports
from scenes.settings import get_page
from scenes.cube import get_cube_page
from scenes.algorithm_selection import get_algorithm_page
from scenes.results import get_results_page
from scenes.camera_scan import get_scan_page


def main(page: ft.Page):
    scene_stack = []

    # ---------------------------------------------------
    # 1) Create PermissionHandler and add it to overlay
    # ---------------------------------------------------
    ph = ft.PermissionHandler()
    page.overlay.append(ph)

    def switch_scene(e, scene_name, option=""):
        # Push current scene to stack before switching
        if scene_stack:
            current_scene = scene_stack[-1]
            if current_scene != scene_name:  # Avoid duplicates if it's the same scene
                scene_stack.append(scene_name)
        else:
            scene_stack.append(scene_name)

        load_scene(scene_name, option)

    def go_back(e):
        if len(scene_stack) > 1:
            scene_stack.pop()  # Remove current scene
            previous_scene = scene_stack[-1]  # Load the previous scene
            load_scene(previous_scene)
        else:
            print("No previous scene")

    # ---------------------------------------------------
    # 2) Define a helper to check and request camera permission
    # ---------------------------------------------------
    def check_and_request_camera_permission():
        status = ph.check_permission(ft.PermissionType.CAMERA)
        if status == ft.PermissionStatus.GRANTED:
            # Already granted
            return ft.PermissionStatus.GRANTED
        else:
            # Request permission
            request_result = ph.request_permission(ft.PermissionType.CAMERA)
            return request_result

    def load_scene(scene_name, option=""):
        page.controls.clear()
        page.update()  # Clear the current scene

        if scene_name == "main_scene":
            page.appbar = None
            page.add(main_content)

        elif scene_name == "settings":
            page.add(get_page(page, switch_scene, go_back))

        elif scene_name == "cube":
            page.add(get_cube_page(page, switch_scene, go_back, option))

        elif scene_name == "algorithm":
            page.add(get_algorithm_page(page, switch_scene, go_back))

        elif scene_name == "results":
            page.add(get_results_page(page, switch_scene, go_back, option))

        elif scene_name == "scan":
            # ---------------------------------------------------
            # 3) Check / request camera permission here
            # ---------------------------------------------------
            result = check_and_request_camera_permission()

            if result == ft.PermissionStatus.GRANTED:
                # Permission is granted - we can safely add scanning page
                page.add(get_scan_page(page, switch_scene, go_back))
            elif result == ft.PermissionStatus.DENIED:
                # The user denied but not permanently. Let’s show a warning:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Camera permission denied. Please enable it to scan.")
                )
                page.snack_bar.open = True
            elif result == ft.PermissionStatus.PERMANENTLY_DENIED:
                # The user permanently denied. Offer to open settings.
                page.dialog = ft.AlertDialog(
                    title=ft.Text("Camera permission needed"),
                    content=ft.Column([
                        ft.Text("You have permanently denied camera access. Please open settings to enable it.")
                    ]),
                    actions=[
                        ft.TextButton(
                            "Open Settings",
                            on_click=lambda e: ph.open_app_settings()
                        ),
                        ft.TextButton(
                            "Cancel",
                            on_click=lambda e: (
                                setattr(page.dialog, "open", False),
                                page.update()
                            )
                        ),
                    ],
                    on_dismiss=lambda e: None,
                )
                page.dialog.open = True

        page.update()

    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.ALWAYS

    logo = ft.Image(
        "/logo.png",
        width=200,
        height=200,
        fit=ft.ImageFit.CONTAIN
    )

    main_content = ft.Column(
        [
            ft.ResponsiveRow(
                [logo],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.FilledButton(
                "Start",
                on_click=lambda e: switch_scene(e, "cube"),
                width=200,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    page.add(main_content)
    scene_stack.append("main_scene")


ft.app(main)
