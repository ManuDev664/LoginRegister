import flet as ft
import datetime
from UsersBBDD import get_user, insert_user, update_last_login
from UserPanel import show_user_panel

# Función principal: Login y Registro
def show_login(page: ft.Page):
    page.clean()
    page.title = "Login y Registro"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.window_width = 500
    page.window_height = 600

    login_email_or_username = ft.TextField(label="Nombre de usuario o Email")
    login_password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True)
    login_msg = ft.Text(value="", color="red")

    def ir_a_registro(e):
        page.clean()
        mostrar_registro()

    def login(e):
        user = get_user(login_email_or_username.value.strip(), login_password.value.strip())
        if user:
            update_last_login(user[0])
            user_data = {
                "id": user[0],
                "nombre": user[1],
                "apellidos": user[2],
                "email": user[3],
                "username": user[4],
                "password": user[5],
                "fechaNacimiento": user[6],
                "estado": user[7],
                "fechaRegistro": user[8],
                "rol": user[9],
                "ultimo_login": user[10]
            }
            show_user_panel(page, user_data, show_login)
        else:
            login_msg.value = "Credenciales incorrectas"
            page.update()

    btn_login = ft.ElevatedButton(text="Iniciar sesión", on_click=login)

    login_view = ft.Column([
        ft.Text("Iniciar Sesión", size=30, weight="bold"),
        login_email_or_username,
        login_password,
        login_msg,
        btn_login,
        ft.TextButton("\u00bfNo tienes cuenta? Regístrate aquí", on_click=ir_a_registro)
    ])

    page.add(login_view)

    # REGISTRO
    def mostrar_registro():
        nombre = ft.TextField(label="Nombre")
        apellidos = ft.TextField(label="Apellidos")
        username = ft.TextField(label="Nombre de usuario")
        email = ft.TextField(label="Email")
        password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True)
        fecha_nacimiento_input = ft.TextField(label="Fecha de nacimiento (YYYY-MM-DD)", read_only=True)

        registro_msg = ft.Text(value="", color="red")

        fecha_nacimiento_picker = ft.DatePicker(
            on_change=lambda e: (
                setattr(fecha_nacimiento_input, "value", fecha_nacimiento_picker.value.date().isoformat()),
                fecha_nacimiento_input.update()
            ),
            first_date=datetime.date(1900, 1, 1),
            last_date=datetime.date.today()
        )
        page.overlay.append(fecha_nacimiento_picker)

        def abrir_datepicker():
            fecha_nacimiento_picker.open = True
            page.update()

        date_btn = ft.ElevatedButton("Seleccionar fecha de nacimiento", on_click=lambda e: abrir_datepicker())

        def registrar_usuario(e):
            if not all([
                nombre.value.strip(),
                apellidos.value.strip(),
                username.value.strip(),
                email.value.strip(),
                password.value.strip(),
                fecha_nacimiento_input.value.strip()
            ]):
                registro_msg.value = "Todos los campos son obligatorios"
            else:
                try:
                    fecha_valida = datetime.datetime.strptime(fecha_nacimiento_input.value.strip(), "%Y-%m-%d").date()
                    insert_user(nombre.value.strip(), apellidos.value.strip(), username.value.strip(), email.value.strip(), password.value.strip(), fecha_valida)
                    page.clean()
                    page.add(ft.Text("Registro exitoso. Ahora puedes iniciar sesión."))
                    show_login(page)
                    return
                except ValueError:
                    registro_msg.value = "Formato de fecha inválido (debe ser YYYY-MM-DD)"
            page.update()

        btn_registro = ft.ElevatedButton("Registrar", on_click=registrar_usuario)

        page.add(ft.Column([
            ft.Text("Registro de Usuario", size=30, weight="bold"),
            nombre,
            apellidos,
            username,
            email,
            password,
            fecha_nacimiento_input,
            date_btn,
            registro_msg,
            btn_registro,
            ft.TextButton("\u00bfYa tienes cuenta? Inicia sesión", on_click=lambda e: show_login(page))
        ]))


# Función de arranque
def main(page: ft.Page):
    show_login(page)

# Lanzar la app
if __name__ == "__main__":
    ft.app(target=main)
