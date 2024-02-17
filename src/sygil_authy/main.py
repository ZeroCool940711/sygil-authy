import time

import pyotp
from nicegui import app, color, icon, ui

from sygil_authy.utils import set_icon

app.native.window_args["resizable"] = False

set_icon()

totp = pyotp.TOTP(
    "DIDZC3PYR62GLMVKXGEPNTYMVSOI72YNUQYRHNP7BIMVNWAMWKJNB4JC7AHMAEXOB5IVYPENON46AKGSQTFSY234U6XBLWOVCDAHRZI"
)

ui.query(".nicegui-content").classes("p-0")


@ui.page("/")
def main():
    # ui.label(totp.now())  # => '492039'
    with ui.card().style("height: 585px"):
        with ui.column().style("height: 100%"):
            with ui.row().style("width: 100%").style(
                ui.Style(alignment=ui.alignment.start)
            ):
                search_bar = ui.input(placeholder="Search").style(
                    "width: 80%; height: 20%"
                )
                add = ui.button(
                    color=color.SECONDARY,
                    # on_click=lambda: search_bar.set_value(None),
                    icon=icon.ADD,
                ).style(f"width: 10%; {ui.Style(alignment=ui.alignment.center)}")

            with ui.scroll_area().style("height: 80%"):
                with ui.column():
                    for i in range(10):
                        with ui.row().style("width: 100%"):
                            ui.label(f"Account {i}").style(
                                ui.Style(alignment=ui.alignment.center)
                            )
                            ui.button("Copy", icon=icon.COPY_ALL).style(
                                ui.Style(alignment=ui.alignment.center)
                            )
                # ui.label("Nothing here yet...").style("align-self: center;")
            # with ui.scroll_area().style("height: 80%"):

            with ui.row().style(
                # "width: 100%; align-items: center; height: 20%; align-self: end;"
                ui.Style(alignment=ui.alignment.end)
            ):
                token = ui.button("Tokens", icon=icon.LOCK).style("width: 30%")
                requests = ui.button("Requests", icon=icon.CHECK_CIRCLE).style(
                    "width: 30%"
                )
                settings = ui.button("Settings", icon=icon.SETTINGS).style("width: 30%")


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        port=5000,
        title="Sygil Authy",
        dark=True,
        reload=True,
        native=True,
        window_size=(430, 660),
        # on_air=True,
    )
