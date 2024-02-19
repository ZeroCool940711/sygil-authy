# import time

import random

import pyotp
from nicegui import app, color, icon, ui

from sygil_authy.utils import (
    add_account,
    first_run,
    get_options,
    # update_account,
    # delete_account,
    search_accounts,
    set_icon,
)

app.native.window_args["resizable"] = False

ui.query(".nicegui-content").classes("p-0")


def nav_bar():
    with ui.page_sticky("end"):
        # with ui.row():  # .style(
        # "width: 100%; align-items: center; height: 20%; align-self: end;"
        # ui.Style(alignment=ui.alignment.end)
        # ):
        ui.separator().style("width: 100%").tailwind.gap("0").padding("0")
        token = ui.button(
            "Tokens", icon=icon.LOCK, on_click=lambda e: ui.open("/")
        ).style("width: 33%")
        requests = ui.button("Requests", icon=icon.CHECK_CIRCLE).style("width: 33%")
        settings = ui.button(
            "Settings",
            icon=icon.SETTINGS,
            on_click=lambda e: ui.open("/settings"),
        ).style("width: 33%")


@ui.page("/settings")
def settings():
    with ui.card().style("height: 585px"):
        with ui.column().style("height: 100%"):
            with ui.row().style("width: 100%").style(
                ui.Style(alignment=ui.alignment.start)
            ):
                ui.label("Settings").style("width: 100%")
                # ui.separator().style("width: 100%")

        nav_bar()


@ui.page("/add")
def add_account_page():
    with ui.card().style("height: 585px"):
        with ui.column().style("height: 100%"):
            with ui.row().style("width: 100%"):
                ui.button(
                    icon=icon.ARROW_BACK, on_click=lambda e: ui.open("/")
                ).tailwind().background_color("transparent")
                ui.label("Add Account").tailwind().font_size("2xl").align_self("center")
            with ui.scroll_area().style("height: 80%"):
                # ui.separator().style("width: 100%")
                with ui.column().style("width: 100%"):
                    ui.label(
                        """
                        You can add Authenticator accounts such as Gmail, Facebook,
                        Dropbox and many more websites with Sygil Authy by entering
                        the code provided by the service in which you want to enable
                        2FA in the input field bellow and clicking the 'Add Account' button.
                        On the next page, you will be able to customize the account by
                        adding an alias, icon, and more.
                        """
                    )
                    ui.label("Enter Code given by the website.").tailwind().text_color(
                        "red-500"
                    ).font_size("lg").align_self("center")

                    with ui.row().style("width: 100%"):
                        secret_input = ui.input(
                            label="Enter Code.",
                            placeholder="i.e: DIDZ C3PY R62G LMVK XGEP NTYM VSOI 72YN UQYR HNP7 BIMV NWAM WKJN B4JC 7AHM AEXO B5IV YPEN ON46 AKGS QTFS Y234 U6XB LWOV CDAH RZI",
                            on_change=lambda e: button.element.set_visibility(
                                True if len(e.value) > 10 else False
                            ),
                        ).style("width: 100%")

                    button = (
                        ui.button(
                            "Add Account",
                            on_click=lambda secret=secret_input: ui.open(
                                f"/account/{'New Account'}-{secret_input.value}/edit"
                            ),
                        )
                        .tailwind()
                        .background_color(color.GREEN)
                        .text_color(color.WHITE)
                        .align_self("center")
                    )

                    button.element.set_visibility(False)

            nav_bar()


@ui.page("/account/{name}-{secret}/edit")
def account_info(name: str = "New Account", secret=None):
    with ui.card().style("height: 585px"):
        with ui.column().style("height: 100%"):
            with ui.row().style("width: 100%").classes("flex justify-between"):
                ui.button(
                    icon=icon.ARROW_BACK, on_click=lambda e: ui.open(f"/account/{name}")
                ).tailwind().background_color(color.TRANSPARENT)
                ui.label(f"Edit {name}").tailwind().font_size("2xl").align_self(
                    "center"
                ).align_self("end")
                ui.button("Save").tailwind().background_color(color.GREEN)

            with ui.scroll_area().style("height: 80%"):
                with ui.column().style("width: 100%"):
                    with ui.row().style("width: 100%"):
                        ui.label("Account Name").tailwind().font_size("lg")
                        account_name = ui.input(label="Account Name", value=name).style(
                            "width: 100%"
                        )

                    with ui.row().style("width: 100%"):
                        ui.label("Alias").tailwind().font_size("lg")
                        alias = ui.input(label="Alias").style("width: 100%")

                    with ui.row().style("width: 100%"):
                        ui.label("Icon").tailwind().font_size("lg")
                        account_icon = ui.input(label="Icon").style("width: 100%")

                    with ui.row().style("width: 100%"):
                        ui.label("Issuer").tailwind().font_size("lg")
                        issuer = ui.input(label="Issuer").style("width: 100%")

                    with ui.row().style("width: 100%"):
                        ui.label("Label").tailwind().font_size("lg")
                        label = ui.input(label="Label").style("width: 100%")

                    with ui.row().style("width: 100%"):
                        ui.label("Algorithm").tailwind().font_size("lg")
                        algorithm = ui.input(label="Algorithm").style("width: 100%")

                    with ui.row().style("width: 100%"):
                        ui.label("Digits").tailwind().font_size("lg")
                        digits = ui.input(label="Digits").style("width: 100%")

                    with ui.row().style("width: 100%"):
                        ui.label("Type").tailwind().font_size("lg")
                        type = ui.input(label="Type").style("width: 100%")

                    with ui.row().style("width: 100%"):
                        ui.label("Website").tailwind().font_size("lg")
                        website = ui.input(label="Website").style("width: 100%")

                    with ui.row().style("width: 100%"):
                        ui.label("Counter").tailwind().font_size("lg")
                        counter = ui.input(label="Counter").style("width: 100%")

                    with ui.row().style("width: 100%"):
                        ui.label("Username").tailwind().font_size("lg")
                        username = ui.input(label="Username").style("width: 100%")

            nav_bar()


@ui.page("/account/{name}")
def account(name: str):
    with ui.card().style("height: 585px"):
        with ui.column().style("height: 100%"):
            with ui.row().style("width: 100%;").classes("flex justify-between"):
                ui.button(
                    icon=icon.ARROW_BACK, on_click=lambda e: ui.open("/")
                ).tailwind().background_color(color.TRANSPARENT)
                ui.label(name).tailwind().font_size("2xl")
                ui.button(
                    icon=icon.EDIT,
                    on_click=lambda name=name: ui.open(f"/account/{name}-{None}/edit"),
                ).tailwind().background_color(color.TRANSPARENT)

            with ui.scroll_area().style("height: 80%"):
                ui.label("TODO").tailwind().font_size("2xl")

            nav_bar()


def copy_to_clipboard(text):
    ui.run_javascript(f"navigator.clipboard.writeText({text})")
    ui.notify(f"Copied {text}")


@ui.page("/")
def main():
    with ui.card().style("height: 585px"):
        with ui.column().style("height: 100%"):
            with ui.row().style("width: 100%").style(
                ui.Style(alignment=ui.alignment.start)
            ):
                search_bar = ui.input(
                    placeholder="Search",
                    # on_change=lambda e: search_accounts({"name": e.value}),
                ).style("width: 80%; height: 20%")
                add = ui.button(
                    color=color.SECONDARY,
                    # on_click=lambda: search_bar.set_value(None),
                    icon=icon.ADD,
                    on_click=lambda e: ui.open("/add"),
                ).style(f"width: 10%; {ui.Style(alignment=ui.alignment.center)}")

            with ui.scroll_area().style("height: 80%"):
                for i in range(10):
                    account_name = f"Account {i}"

                    with ui.list().props("bordered separator").style(
                        "width: 100%; align-items: end; padding: 0; margin: 0; gap: 0;"
                    ):
                        with ui.item(
                            on_click=lambda name=account_name: ui.open(
                                f"/account/{name}"
                            )
                        ):
                            with ui.item_section().props("avatar"):
                                ui.icon(
                                    icon.KEY,
                                    color=random.choice(list(vars(color).values())),
                                )
                            with ui.item_section():
                                account_name = (
                                    ui.item_label(account_name)
                                    .tailwind()
                                    .font_size("lg")
                                )

            nav_bar()


if __name__ in {"__main__", "__mp_main__"}:
    first_run()
    set_icon()

    options = get_options()

    ui.run(
        port=5000,
        title=options["app_title"],
        dark=True if options["theme_mode"] == "dark" else False,
        reload=True,
        native=True,
        window_size=(430, 660),
        # on_air=True,
    )
