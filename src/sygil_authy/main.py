# import time

import random

import pyotp
from nicegui import app, color, icon, ui

from sygil_authy.utils import (
    add_account,
    first_run,
    get_all_accounts,
    get_options,
    # update_account,
    # delete_account,
    search_accounts_by_name,
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
                    icon=icon.ARROW_BACK, on_click=lambda e: ui.back()
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
                        2FA in the input field bellow and clicking the 'Add Account'
                        button that will show after you type the code for your website.
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
                                f"/account/{'New Account'}/edit?secret={secret_input.value}"
                            ),
                        )
                        .tailwind()
                        .background_color(color.GREEN)
                        .text_color(color.WHITE)
                        .align_self("center")
                    )

                    button.element.set_visibility(False)

            nav_bar()


def save_account_and_open(name: str, account_info_dict: dict):
    add_account(account_info_dict)
    ui.open(f"/account/{name}")


@ui.page("/account/{name}/edit")
def account_info(name: str = "New Account", secret=None):
    print(name)
    with ui.card().style("height: 585px"):
        with ui.column().style("height: 100%"):
            with ui.row().style("width: 100%").classes("flex justify-between"):
                ui.button(
                    icon=icon.ARROW_BACK, on_click=lambda e: ui.back()
                ).tailwind().background_color(color.TRANSPARENT)
                ui.label(f"Edit {name}").tailwind().font_size("2xl").align_self(
                    "center"
                ).align_self("end")
                ui.button(
                    "Save",
                    on_click=lambda e: save_account_and_open(
                        account_name.value, account_info_dict
                    ),
                ).tailwind().background_color(color.GREEN)

            with ui.scroll_area().style("height: 80%"):
                with ui.column().style("width: 100%"):
                    account_name = ui.input(label="Account Name", value=name).style(
                        "width: 100%"
                    )

                    alias = ui.input(label="Alias").style("width: 100%")
                    account_icon = ui.input(label="Icon").style("width: 100%")
                    website = ui.input(label="Website").style("width: 100%")
                    issuer = ui.input(label="Issuer").style("width: 100%")
                    label = ui.input(label="Label").style("width: 100%")
                    with ui.row().style("width: 100%; gap: 0;").classes(
                        "flex justify-between"
                    ):
                        digits = ui.number(
                            label="Digits",
                            value=6,
                            placeholder=6,
                            precision=0,
                            step=1,
                            min=6,
                            max=8,
                            # validation={
                            #     "Value must be between 6-8!": lambda value: value
                            #     is not None
                            #     and (value < 6 or value > 8)
                            # },
                        ).style("width: 20%")
                        algorithm = ui.select(
                            options=["sha1", "sha256", "sha512"],
                            label="Algorithm",
                            value="sha1",
                        ).style("width: 40%")
                        type = ui.select(
                            options=["TOTP", "HOTP"], value="TOTP", label="Type"
                        ).style("width: 40%")

                        counter = ui.number(
                            label="Counter",
                            value=30,
                            step=1,
                            placeholder=30,
                            precision=0,
                        ).style("width: 100%")

                    ui.label("Last Used").tailwind().font_size("lg").width("100%")
                    last_used = ui.date(value=None, mask="MM-DD-YYYY").style(
                        "width: 100%"
                    )
                    is_active = ui.checkbox("Active", value=True).style("width: 100%")
                    is_password_protected = ui.checkbox(
                        "Password Protected", value=False
                    ).style("width: 100%")

                    delete_button = (
                        ui.button(
                            "Delete Account",
                            on_click=lambda d: delete_dialogue(name).open(),
                        )
                        .tooltip("This action is irreversible!")
                        .tailwind.background_color(color.RED)
                    )

                    account_info_dict = {
                        "name": account_name.value,
                        "alias": alias.value,
                        "icon": account_icon.value,
                        "issuer": issuer.value,
                        "label": label.value,
                        "algorithm": algorithm.value,
                        "digits": digits.value,
                        "type": type.value,
                        "website": website.value,
                        "counter": counter.value,
                        "last_used": last_used.value,
                        "is_active": is_active.value,
                        "is_password_protected": is_password_protected.value,
                    }

            nav_bar()


def delete_dialogue(name: str):
    with ui.dialog() as d:
        with ui.card():
            ui.label("Are you sure you want to delete this account?")
            with ui.row().style("alig-content: center; "):
                ui.button(
                    "Yes", on_click=lambda e: ui.open(f"/account/{name}/delete")
                ).tailwind.background_color(color.RED)
                ui.button("No", on_click=lambda e: d.close()).tailwind.background_color(
                    color.GREEN
                )

    return d


@ui.page("/account/{name}")
def account(name: str):
    print(name)
    try:
        account_information = search_accounts_by_name(name)[0]
    except IndexError:
        account_information = search_accounts_by_name(name)

    print(account_information)

    with ui.card().style("height: 585px"):
        with ui.column().style("height: 100%"):
            with ui.row().style("width: 100%;").classes("flex justify-between"):
                ui.button(
                    icon=icon.ARROW_BACK, on_click=lambda e: ui.back()
                ).tailwind().background_color(color.TRANSPARENT)
                ui.label(name).tailwind().font_size("2xl")
                ui.button(
                    icon=icon.EDIT,
                    on_click=lambda name=name: ui.open(f"/account/{name}-{None}/edit"),
                ).tailwind().background_color(color.TRANSPARENT)

            with ui.scroll_area().style("height: 80%"):
                if account_information:
                    ui.label(account_information["name"]).tailwind().font_size("2xl")

            nav_bar()


@ui.page("/")
def main():
    with ui.card().style("height: 585px"):
        with ui.column().style("height: 100%"):
            with ui.row().style("width: 100%").style(
                ui.Style(alignment=ui.alignment.start)
            ):
                search_bar = ui.input(
                    placeholder="Search",
                    on_change=lambda e: search_accounts_by_name(e.value),
                ).style("width: 80%; height: 20%")

                add = ui.button(
                    color=color.SECONDARY,
                    # on_click=lambda: search_bar.set_value(None),
                    icon=icon.ADD,
                    on_click=lambda e: ui.open("/add"),
                ).style(f"width: 10%; {ui.Style(alignment=ui.alignment.center)}")

            with ui.scroll_area().style("height: 80%").bind_visibility_from(search_bar):
                # for i in range(10):
                if search_bar.value or get_all_accounts():
                    for account in (
                        search_accounts_by_name(search_bar.value) or get_all_accounts()
                    ):
                        if account:
                            with ui.list().props("bordered separator").style(
                                "width: 100%; align-items: end; padding: 0; margin: 0; gap: 0;"
                            ):
                                with ui.item(
                                    on_click=lambda name=account["name"]: ui.open(
                                        f"/account/{name}"
                                    )
                                ):
                                    with ui.item_section().props("avatar"):
                                        ui.icon(
                                            icon.KEY,
                                            color=random.choice(
                                                list(vars(color).values())
                                            ),
                                        )
                                    with ui.item_section():
                                        account_name = (
                                            ui.item_label(account["name"])
                                            .tailwind()
                                            .font_size("lg")
                                        )
                else:
                    ui.label("No accounts found!").style("width: 100%")

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
