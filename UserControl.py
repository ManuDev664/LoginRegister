import flet as ft
# El módulo os permite interactuar con el sistema operativo
import os
# El módulo signal permite manejar señales en sistemas UNIX
import signal


def main(page: ft.Page):
    page.title = "Control Usuarios"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    pid_input = ft.TextField(label="Introduce el PID", keyboard_type=ft.KeyboardType.NUMBER)
    result_text = ft.Text()

    def kill_process(e):
        try:
            pid = int(pid_input.value)
            os.kill(pid, signal.SIGKILL)  # Matar el proceso en Linux
            result_text.value = f"Proceso {pid} finalizado con éxito."
            result_text.color = "green"
        except ValueError:
            result_text.value = "Introduce un número válido."
            result_text.color = "red"
        except ProcessLookupError:
            result_text.value = f"No se encontró el proceso con PID {pid}."
            result_text.color = "red"
        except PermissionError:
            result_text.value = "No tienes permisos para finalizar este proceso."
            result_text.color = "red"

        page.update()

    btn_kill = ft.ElevatedButton("Finalizar Proceso", on_click=kill_process)

    page.add(pid_input, btn_kill, result_text)

ft.app(target=main)
