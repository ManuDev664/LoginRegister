import flet as ft
import os
from crontab import CronTab

def main(page: ft.Page):
    page.title = "Copias de Seguridad Programadas"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Campos de entrada para los directorios
    src_input = ft.TextField(label="Directorio de Origen", width=400)
    dest_input = ft.TextField(label="Directorio de Destino", width=400)

    # Desplegables para hora, minuto y día
    minutes = [str(i).zfill(2) for i in range(60)]
    hours = [str(i).zfill(2) for i in range(24)]
    days = [str(i) for i in range(1, 32)]  # Días del mes

    minute_dropdown = ft.Dropdown(label="Minuto", options=[ft.dropdown.Option(i) for i in minutes])
    hour_dropdown = ft.Dropdown(label="Hora", options=[ft.dropdown.Option(i) for i in hours])
    day_dropdown = ft.Dropdown(label="Día del Mes", options=[ft.dropdown.Option(i) for i in days])

    def show_alert(page, title, message):
        """Muestra un mensaje emergente."""
        dlg = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda e: close_alert(page))],
        )
        page.dialog = dlg
        page.dialog.open = True
        page.update()

    def close_alert(page):
        """Cierra la alerta emergente."""
        page.dialog.open = False
        page.update()

    def schedule_backup(e):
        """Programa la copia de seguridad en Crontab."""
        src = src_input.value.strip()
        dest = dest_input.value.strip()
        minute = minute_dropdown.value
        hour = hour_dropdown.value
        day = day_dropdown.value

        # Validar que los campos no estén vacíos
        if not src or not dest:
            show_alert("Error", "Debes introducir ambos directorios.")
            return
        if not minute or not hour or not day:
            show_alert("Error", "Selecciona una hora válida para la copia de seguridad.")
            return
        if not os.path.exists(src):
            show_alert("Error", f"El directorio de origen '{src}' no existe.")
            return
        if not os.path.exists(dest):
            show_alert("Error", f"El directorio de destino '{dest}' no existe.")
            return

        # Comando rsync para copiar los archivos
        command = f"rsync -av {src}/ {dest}/"

        # Programar la tarea en Crontab
        cron = CronTab(user=True)
        job = cron.new(command=command, comment="Copia de Seguridad Programada")
        job.minute.on(int(minute))
        job.hour.on(int(hour))
        job.day.on(int(day))
        cron.write()

        show_alert("Éxito", f"Copia de seguridad programada para el {day} a las {hour}:{minute}.")

    btn_schedule = ft.ElevatedButton("Programar Copia de Seguridad", on_click=schedule_backup)

    page.add(src_input, dest_input, minute_dropdown, hour_dropdown, day_dropdown, btn_schedule)

ft.app(target=main)