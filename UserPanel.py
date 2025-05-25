import flet as ft
from UsersBBDD import eliminar_usuario

# Ahora recibimos 'volver_a_login' como parámetro
def show_user_panel(page: ft.Page, user_data: dict, volver_a_login):
    page.clean()

    # Mostrar datos del usuario
    info_usuario = ft.Column([
        ft.Text(f"👤 Usuario: {user_data['username']}", size=18),
        ft.Text(f"📧 Email: {user_data['email']}", size=18),
        ft.Text(f"🔑 Rol: {user_data['rol']}", size=18),
        ft.Text(f"🗓️ Fecha de Registro: {user_data['fechaRegistro']}", size=18),
        ft.Text(f"🕒 Último Login: {user_data['ultimo_login']}", size=18),
    ])

    mensaje_resultado = ft.Text(color="green", size=16)
    mensaje_error = ft.Text(color="red", size=16)

    # Campo para ingresar ID del usuario a eliminar
    id_input = ft.TextField(label="ID del usuario a eliminar", width=200)

    # Cuadro de confirmación
    confirm_dialog = ft.AlertDialog(modal=True)
    page.dialog = confirm_dialog

    # Usamos la función pasada como parámetro
    def cerrar_sesion(e):
        volver_a_login(page)

    def eliminar_usuario(e):
        user_id_str = id_input.value.strip()

        if not user_id_str.isdigit():
            mensaje_error.value = "⚠️ El ID debe ser un número válido."
            mensaje_resultado.value = ""
            page.update()
            return

        user_id = int(user_id_str)

        def confirmar_accion(ev):
            confirm_dialog.open = False
            print(f"Intentando eliminar usuario con ID {user_id}")  # Depuración
            if eliminar_usuario(user_id):  # Llamada correcta aquí
                print("Eliminado correctamente")  # Depuración
                mensaje_resultado.value = f"✅ Usuario con ID {user_id} eliminado correctamente."
                mensaje_error.value = ""
            else:
                print("No se encontró usuario")  # Depuración
                mensaje_resultado.value = ""
                mensaje_error.value = f"❌ No se encontró ningún usuario con ID {user_id}."
            page.update()

        def cancelar_accion(ev):
            confirm_dialog.open = False
            page.update()

        confirm_dialog.title = ft.Text("Confirmación de Eliminación")
        confirm_dialog.content = ft.Text(f"¿Estás seguro de eliminar el usuario con ID {user_id}?")
        confirm_dialog.actions = [
            ft.TextButton("Cancelar", on_click=cancelar_accion),
            ft.ElevatedButton("Confirmar", on_click=confirmar_accion)
        ]
        confirm_dialog.open = True
        page.update()

    # Botón cerrar sesión
    cerrar_sesion_btn = ft.ElevatedButton("Cerrar sesión", on_click=cerrar_sesion)

    # Elementos base
    contenido = [ft.Text("Panel de Usuario", size=26, weight="bold"), info_usuario, cerrar_sesion_btn]

    # Funciones extra si es ADMIN
    if user_data["rol"].upper() == "ADMIN":
        contenido.append(ft.Divider())
        contenido.append(ft.Text("🔐 Funciones de Administrador", size=22, weight="bold"))
        contenido.append(id_input)
        contenido.append(ft.ElevatedButton("Eliminar usuario por ID", on_click=eliminar_usuario))
        contenido.append(mensaje_resultado)
        contenido.append(mensaje_error)

    page.add(*contenido)
