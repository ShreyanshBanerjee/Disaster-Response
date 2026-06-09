import flet as ft

def main(page: ft.Page):
    page.title = "AI'm Ready"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.add(
        ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls = [
                ft.Text(
                    value = "AI'm Ready",                        
                    style=ft.TextStyle(
                        size=40,
                        weight=ft.FontWeight.BOLD,
                        color = ft.Colors.BLUE_600
                    ),
                ),
                ft.Text(
                    value = "Build a plan for rapid natural disaster response.",
                    style=ft.TextStyle(
                        size=20,
                    )
                )
            ]
        )
    )

ft.run(main)
