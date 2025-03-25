import flet as ft

def main(page: ft.Page):
    page.title = "LOGIN PAGE"
    page.window_width = 400
    page.window_height = 600
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    opcion_drop = ft.Dropdown(
        label="Selecciona opcion",
        options=[
            ft.dropdown.Option("Control Usuarios", "Control Usuarios"),
            ft.dropdown.Option("Copia Seguridad", "Copia Seguridad"),
        ]
    )

    def mostrar_opcion():
        ft.Column([
            opcion_drop,
        ], alignment="center")
        page.update()

if __name__ == "__main__":
    ft.app(target=main)