import flet as ft

    
def get_page(page:ft.Page, switch_scene, go_back):
    
        page.appbar = ft.AppBar(
            leading=ft.IconButton(ft.icons.ARROW_BACK,on_click=go_back)
        )

        content = ft.SafeArea(ft.Text("Settings tab"))
        
        return content
    
    