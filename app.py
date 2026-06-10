import flet as ft
import flet_map as ftmap

from data.helpers import *
from graph_algo import *
from risk_ai.predict import *

def main(page: ft.Page):
    page.title = "WAIfinder"
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

        c_risk = predict(solver.lat, solver.lon)
        advice_mapping = {
            "Safe": "SAFE zone",
            "Low": "LOW-RISK zone. Remain cautious, as situations can escalate any second",
            "Medium": "MEDIUM-RISK zone. We highly recommend traveling to a nearby shelter",
            "High": "HIGH-RISK zone. Leave your current area immediately!"
        }
        risk_level_text.value = f"You are currently in a {advice_mapping[c_risk]}."
        risk_level_text.visible=True
    
    def gen_path(e):
        nonlocal solver, path

        end_pt = next(
            (i for i in nearest
            if f"{i[0]} - Total Capacity: {int(i[3])}" == shelter_loc.value),
            None
        )
        if not end_pt:
            return

        solver.build_network()
        path = solver.solve((end_pt[4], end_pt[5]))

        coords = [
            ftmap.MapLatitudeLongitude(
                solver.backward_mapping[i][0],
                solver.backward_mapping[i][1]
            )
            for i in path
        ]

        polyline = ftmap.PolylineMarker(
            coordinates=coords,
            color=ft.Colors.BLUE,
            border_stroke_width=10,
        )

 
        heatmap_grid = []
        for key, value in cache.items():
            heatmap_grid.append(
                ftmap.PolygonMarker(
                    coordinates=[
                        ftmap.MapLatitudeLongitude(key[0]-0.005,key[1]-0.005),
                        ftmap.MapLatitudeLongitude(key[0]-0.005,key[1]+0.005),
                        ftmap.MapLatitudeLongitude(key[0]+0.005,key[1]+0.005),
                        ftmap.MapLatitudeLongitude(key[0]+0.005,key[1]-0.005)
                    ],
                    color=ft.Colors.with_opacity(
                        0.1,
                        {"Safe": ft.Colors.BLUE, "Low": ft.Colors.PURPLE, "Medium": ft.Colors.PINK, "High": ft.Colors.RED}[value],
                    ),
                    border_stroke_width=1
                )
            )

        map_view.layers = [
            ftmap.TileLayer(
                url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                user_agent_package_name="com.aimready.app",
            ),
            ftmap.PolygonLayer(
                polygons=heatmap_grid
            ),               
            ftmap.PolylineLayer(polylines=[polyline]),

        ]

        map_view.visible = True
        map_view.expand = True
        map_view.initial_center = ftmap.MapLatitudeLongitude(solver.lat, solver.lon)

        page.update()

        print(cache)


    page.bgcolor = "lightgrey"
    page.add(
        ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls = [
                ft.Text(
                    value = "WAIfinder",
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
                risk_level_text := ft.Text(
                    value="",
                    visible = False,
                    style=ft.TextStyle(
                        size=25
                    )
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
                map_view := ftmap.Map(
                    visible=False,
                    initial_center=ftmap.MapLatitudeLongitude(0,0),
                    initial_zoom=15,
                    layers = [
                        ftmap.TileLayer(
                            url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                            user_agent_package_name="com.aimready.app",
                        ),
                        ftmap.PolylineLayer(
                            polylines=[
                                polyline := None
                            ]
                        ),
                    ]
                ),
            ]
        )
    )

ft.run(main)
