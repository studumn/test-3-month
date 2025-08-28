import flet as ft
from flet import Icons
from db.main_db import init_db, get_tasks, add_task_db, update_task_db, delete_task_db

def main(page: ft.Page):
    page.title = "Список покупок"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_maximized = True
    page.padding = 20

    # Инициализация базы
    init_db()

    task_list = ft.Column(spacing=10)

    # ----------------- Функции -----------------
    def load_tasks():
        task_list.controls.clear()
        for task_id, task_text, completed in get_tasks():
            task_list.controls.append(create_task_row(task_id, task_text, completed))
        page.update()

    def create_task_row(task_id, task_text, completed):
        task_field = ft.TextField(
            value=task_text,
            expand=True,
            dense=True,
            read_only=True,
            text_align=ft.TextAlign.LEFT
        )

        task_checkbox = ft.Checkbox(
            value=bool(completed),
            on_change=lambda e: toggle_task(task_id, e.control.value)
        )

        def enable_edit(e):
            task_field.read_only = False
            page.update()

        def save_edit(e):
            update_task_db(task_id, new_task=task_field.value)
            task_field.read_only = True
            load_tasks()

        row = ft.Row(
            controls=[
                task_checkbox,
                task_field,
                ft.IconButton(Icons.EDIT, icon_color="yellow", on_click=enable_edit),
                ft.IconButton(Icons.SAVE, icon_color="green", on_click=save_edit),
                ft.IconButton(Icons.DELETE, icon_color="red", on_click=lambda e: delete_task(task_id))
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        return row

    def add_task(e):
        task_text = task_input.value.strip()
        if task_text != "":
            add_task_db(task_text)
            task_input.value = ""
            load_tasks()

    def delete_task(task_id):
        delete_task_db(task_id)
        load_tasks()

    def toggle_task(task_id, is_completed):
        update_task_db(task_id, completed=is_completed)
        load_tasks()

    # ----------------- UI -----------------
    task_input = ft.TextField(
        hint_text="Введите товар",
        expand=True,
        dense=True,
        on_submit=add_task
    )
    add_button = ft.ElevatedButton("Добавить", on_click=add_task)

    page.add(
        ft.Column([
            ft.Row([task_input, add_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            task_list
        ])
    )

    load_tasks()

ft.app(target=main)
