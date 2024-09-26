import flet as ft


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    logo = ft.Image(f"/logo.png", width=200, height= 200,fit=ft.ImageFit.CONTAIN)
    algorithm_chooser = ft.Dropdown(
        options=[
            "Algorytm Kociemby",
            "Algorytm Korfa"
        ]
    )
    page.add(
        ft.ResponsiveRow(
            [logo],
            ft.Text("Wybierz algorytm"),
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )
    page.add(ft.SafeArea(ft.Text("Hello, Flet!")))


ft.app(main)
