import flet as ft
import os
import signal

def mostrar_procesos(page, user_data, volver_a_login, show_user_panel, mostrar_cron_tab):
    page.clean()

    pid_input = ft.TextField(label="Introduce el PID del proceso a matar", width=300)
    mensaje_resultado = ft.Text("", color="green")
    mensaje_error = ft.Text("", color="red")

    def matar_proceso(e):
        pid_str = pid_input.value.strip()
        if not pid_str.isdigit():
            mensaje_error.value = "❌ El PID debe ser un número válido."
            mensaje_resultado.value = ""
            page.update()
            return

        pid = int(pid_str)
        try:
            os.kill(pid, signal.SIGKILL)
            mensaje_resultado.value = f"✅ Proceso con PID {pid} matado exitosamente."
            mensaje_error.value = ""
        except ProcessLookupError:
            mensaje_error.value = f"❌ No existe ningún proceso con PID {pid}."
            mensaje_resultado.value = ""
        except PermissionError:
            mensaje_error.value = "❌ Permiso denegado. Necesitas privilegios de administrador."
            mensaje_resultado.value = ""
        except Exception as ex:
            mensaje_error.value = f"❌ Error inesperado: {ex}"
            mensaje_resultado.value = ""
        page.update()

    def volver(e):
        show_user_panel(page, user_data, volver_a_login, mostrar_cron_tab, mostrar_procesos)

    page.add(
        ft.Column([
            ft.Text("🛑 Matar Proceso por PID", size=22, weight="bold"),
            pid_input,
            ft.ElevatedButton("Matar Proceso", on_click=matar_proceso, bgcolor="red", color="white"),
            mensaje_resultado,
            mensaje_error,
            ft.ElevatedButton("Volver al Panel", on_click=volver, bgcolor="gray", color="white"),
        ], alignment="center", spacing=20)
    )
    page.update()
