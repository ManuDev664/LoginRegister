import flet as ft
import subprocess

from MatarProceso import mostrar_procesos
from UserPanel import show_user_panel

def mostrar_cron_tab(page: ft.Page, user_data: dict, volver_a_login, mostrar_user_panel,mostrar_procesos):
    page.clean()

    ruta_origen = ft.TextField(label="Ruta de origen")
    ruta_destino = ft.TextField(label="Ruta de destino")
    frecuencia_minutos = ft.TextField(label="Frecuencia en minutos")

    def ejecutar_backup(e):
        origen = ruta_origen.value
        destino = ruta_destino.value
        frecuencia = frecuencia_minutos.value
        if origen and destino and frecuencia:
            subprocess.run(["bash", "backup.sh", origen, destino, frecuencia])
            # Aquí decides si quieres mostrar algún mensaje o volver automáticamente
            # Por ejemplo volvemos al panel de usuario:
            mostrar_user_panel(page, user_data, volver_a_login, mostrar_cron_tab)

    def volver_a_user_panel(e):
        mostrar_user_panel(page, user_data, volver_a_login, mostrar_cron_tab, mostrar_procesos)

    page.add(
        ft.Column([
            ft.Text("Configurar Backup", size=20, weight="bold", color="blue"),
            ruta_origen,
            ruta_destino,
            frecuencia_minutos,
            ft.ElevatedButton("Ejecutar Backup", on_click=ejecutar_backup, bgcolor="green", color="white"),
            ft.ElevatedButton("Volver al Panel de Usuario", on_click=volver_a_user_panel,
                              bgcolor="gray", color="white")
        ], alignment="center")
    )
    page.update()
