import flet as ft



def get_algorithm_page(page:ft.Page, switch_scene, go_back):
    algorithm = ""
    def set_algorithm(e):
        nonlocal algorithm
        algorithm = algorithm_chooser.value
    def get_algorithm():
        return algorithm
    algorithm_chooser = ft.Dropdown(
        options=[
            ft.dropdown.Option("Algorytm Kociemby"),
            ft.dropdown.Option("Algorytm Korfa"),
            ft.dropdown.Option("LBL"),
            ft.dropdown.Option("CUSTOM LBL"),
            ft.dropdown.Option("Machine Learning")
        ],
        hint_text="Wybierz",
        border_color=ft.colors.AMBER_100,
        on_change=set_algorithm,
    )
    content = ft.Column(
        [
            ft.Text("Wybierz algorytm",text_align=ft.TextAlign.CENTER,size=24),
            algorithm_chooser,
            ft.FilledButton("Ułóż",on_click=lambda e :switch_scene(e,"results"))
        ]
    )

    return content

