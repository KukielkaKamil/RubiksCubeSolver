import flet as ft


algorithm_endpoints = {
    "Algorytm Kociemby": "/kociemba",
    "LBL": "/lbl",
    "Machine Learning": "/ml"
}

def get_algorithm_page(page:ft.Page, switch_scene, go_back):
    algorithm = ""
    def set_algorithm(e):
        nonlocal algorithm
        algorithm_name = algorithm_chooser.value
        algorithm = algorithm_endpoints[algorithm_name]
    
    algorithm_chooser = ft.Dropdown(
        options=[
            ft.dropdown.Option("Algorytm Kociemby"),
            ft.dropdown.Option("LBL"),
            ft.dropdown.Option("Machine Learning")
        ],
        hint_text="Wybierz",
        border_color=ft.Colors.AMBER_100,
        on_change=set_algorithm,
    )

    def select_algorithm(e,algorithm):
        print(algorithm)
        if algorithm_chooser.value == None:
            dialog = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text("You must select an algorithm to continue."),
                actions=[
                    ft.TextButton("OK", on_click=lambda e: close_dialog(dialog))
                ]
            )
            page.overlay.append(dialog)
            dialog.open = True
            page.update()
        else:
            switch_scene(e,"results",algorithm)

    def close_dialog(dialog):
                dialog.open = False
                page.update()
                page.overlay.remove(dialog)
    
    content = ft.Column(
        [
            ft.Text("Wybierz algorytm",text_align=ft.TextAlign.CENTER,size=24),
            algorithm_chooser,
            ft.FilledButton("Ułóż",on_click=lambda e :select_algorithm(e,algorithm))
        ]
    )

    return content

