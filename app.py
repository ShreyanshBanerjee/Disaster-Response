import flet as ft

from data.helpers import *
from graph_algo import *

def main(page: ft.Page):
    page.title = "AI'm Prepared"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    solver = None
    nearest = []
    path = []
    def update_address(e: ft.Event[ft.Button]):
        nonlocal solver
        solver = PathSolver(street_box.value, city_box.value, state_box.value)

        nonlocal nearest
        nearest = solver.find_nearest_shelter()
        
        shelter_loc.options = []
        shelter_loc.enabled = True
        shelter_loc.visible = True
        select_shelter_text.visible = True
        gen_path_button.visible = True
        for item in nearest:
            shelter_loc.options.append(ft.dropdown.Option(f"{item[0]} - Total Capacity: {int(item[3])}"))
    
    def gen_path():
        
        loadingText.visible=True
        loadingText.value = "Please wait; Constructing optimal path..."
        end_pt = [i for i in nearest if f"{i[0]} - Total Capacity: {int(i[3])}" == shelter_loc.value][0]
        
        nonlocal solver
        solver.build_network()

        path = solver.solve((end_pt[5], end_pt[4]))
        print(path)

        loadingText.value = "Complete!"
        page.update()


    page.bgcolor = "lightgrey"
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
                    value="Build a plan for rapid natural disaster response in minutes.",
                    style=ft.TextStyle(
                        size=20,
                    )
                ),
                ft.Divider(),
                ft.Text(
                    value="Enter your current address:",
                    style=ft.TextStyle(
                        size=25
                    )
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls = [
                        street_box := ft.TextField(value="", hint_text="Address"),
                        city_box := ft.TextField(value="", hint_text="City"),
                        state_box := ft.TextField(value="", hint_text="State"),
                        ft.Button(content="Next", on_click=update_address)
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls = [
                        select_shelter_text := ft.Text(
                            value="Select a shelter: ",
                            visible=False,
                            style=ft.TextStyle(
                                size=25
                            ),
                        ),
                        shelter_loc := ft.Dropdown(
                            label="Nearby Shelters",
                            visible=False,
                            text_align=ft.TextAlign.CENTER,
                            options=[
                                ft.dropdown.Option("---")
                            ],
                        )
                    ],
                ),
                gen_path_button := ft.Button(content="Generate Path", on_click=gen_path, visible=False),
                loadingText := ft.Text(value="", style=ft.TextStyle(size=25))
            ]
        )
    )

ft.run(main)
