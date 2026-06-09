import flet as ft

from data import *

def main(page: ft.Page):
    page.title = "AI'm Prepared"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def handle_button_click(e: ft.Event[ft.Button]):
        loc = convert_address_to_latlong(street_box.value, city_box.value, state_box.value)
        message.value = (
            f"Point: ({loc[0]}, {loc[1]})"
        )

    page.add(
        ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls = [
                ft.Text(
                    value = "AI'm Prepared",                        
                    style=ft.TextStyle(
                        size=40,
                        weight=ft.FontWeight.BOLD,
                        color = ft.Colors.BLUE_600
                    ),
                ),
                ft.Text(
                    value="Build a plan for rapid natural disaster response in seconds.",
                    style=ft.TextStyle(
                        size=15,
                    )
                ),
                ft.Divider(),
                ft.Text(
                    value="Enter your approximate current address:",
                    style=ft.TextStyle(
                        size=20
                    )
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls = [
                        street_box := ft.TextField(value="Street"),
                        city_box := ft.TextField(value="City"),
                        state_box := ft.TextField(value="State"),
                        ft.Button(content="Go", on_click=handle_button_click)
                    ]
                ),
                message := ft.Text(
                    value="Location",
                    style=ft.TextStyle(
                        size=20
                    )
                )
            ]
        )
    )

ft.run(main)
