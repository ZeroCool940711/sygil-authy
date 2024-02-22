import datetime
import random
import sys

import pyotp
from loguru import logger
from nicegui import app, color, icon, ui

from sygil_authy.utils import (
    # add_account,
    delete_account,
    first_run,
    get_all_accounts,
    get_options,
    search_accounts_by_name,
    set_icon,
    update_account,
)

app.native.window_args["resizable"] = False

ui.query(".nicegui-content").classes("p-0")


# @logger.catch
def nav_bar():
    with ui.page_sticky("end"):
        # with ui.row():  # .style(
        # "width: 100%; align-items: center; height: 20%; align-self: end;"
        # ui.Style(alignment=ui.alignment.end)
        # ):
        ui.separator().style("width: 100%").tailwind.gap("0").padding("0")
        ui.button("Accounts", icon=icon.LOCK, on_click=lambda e: ui.open("/")).style(
            "width: 33%"
        )
        ui.button("Requests", icon=icon.CHECK_CIRCLE).style("width: 33%")
        ui.button(
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
# @logger.catch
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
                                f"/account/{'New Account'}/edit?secret={secret_input.value}&otp_type=TOTP"
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
    # try:
    update_account(account_info_dict)

    # add_account(account_info_dict)
    ui.open(f"/account/{account_info_dict['name']}")


@ui.page("/account/{name}/edit")
def account_info(
    secret, name: str = "New Account", otp_type: str = "TOTP", password: str = ""
):
    try:
        account_info_dict = dict(search_accounts_by_name(name)[0])
    except IndexError:
        account_info_dict = dict(search_accounts_by_name(name))

    try:
        _ = account_info_dict["type"]
        _ = account_info_dict["counter"]
        _ = account_info_dict["is_active"]
        _ = account_info_dict["is_password_protected"]
    except KeyError:
        account_info_dict["type"] = otp_type
        account_info_dict["counter"] = 30
        account_info_dict["is_active"] = True
        account_info_dict["is_password_protected"] = False

    account_info_dict["secret"] = secret
    account_info_dict["password"] = password
    account_info_dict["last_used"] = None

    logger.debug(f"Account Info Dict: {account_info_dict}")

    with ui.card().style("height: 585px"):
        with ui.column().style("height: 100%"):
            with ui.row().style("width: 100%").classes("flex justify-between"):
                ui.button(
                    icon=icon.ARROW_BACK, on_click=lambda e: ui.back()
                ).tailwind().background_color(color.TRANSPARENT)

                ui.label().bind_text_from(
                    account_info_dict, "name", backward=lambda n: f"Edit: {n}"
                ).tailwind().font_size("2xl").align_self("center").align_self("end")

                ui.button(
                    "Save",
                    on_click=lambda: save_account_and_open(
                        account_info_dict["name"], account_info_dict
                    ),
                ).tailwind().background_color(color.GREEN)

            with ui.scroll_area().style("height: 80%"):
                with ui.column().style("width: 100%"):
                    ui.input(
                        label="Account Name",
                        value=name,
                        on_change=lambda e: account_info_dict.update(name=e.value),
                    ).style("width: 100%").bind_value(account_info_dict, "name")

                    ui.input(
                        label="Alias",
                        on_change=lambda e: account_info_dict.update(alias=e.value),
                    ).style("width: 100%").bind_value(account_info_dict, "alias")

                    ui.input(
                        label="Icon",
                        on_change=lambda e: account_info_dict.update(icon=e.value),
                    ).style("width: 100%").bind_value(account_info_dict, "icon")

                    ui.input(
                        label="Website",
                        on_change=lambda e: account_info_dict.update(website=e.value),
                    ).style("width: 100%").bind_value(account_info_dict, "website")

                    ui.input(
                        label="Issuer",
                        on_change=lambda e: account_info_dict.update(issuer=e.value),
                    ).style("width: 100%").bind_value(account_info_dict, "issuer")

                    ui.input(
                        label="Label",
                        on_change=lambda e: account_info_dict.update(label=e.value),
                    ).style("width: 100%").bind_value(account_info_dict, "label")

                    ui.input(
                        label="Username",
                        on_change=lambda e: account_info_dict.update(username=e.value),
                    ).style("width: 100%").bind_value(account_info_dict, "username")

                    with ui.row().style("width: 100%; gap: 0;").classes(
                        "flex justify-between"
                    ):
                        ui.number(
                            label="Digits",
                            value=6,
                            placeholder=6,
                            precision=0,
                            step=1,
                            min=6,
                            max=8,
                            on_change=lambda e: account_info_dict.update(
                                digits=e.value
                            ),
                        ).style("width: 20%").bind_value(account_info_dict, "digits")

                        ui.select(
                            options=["sha1", "sha256", "sha512"],
                            label="Algorithm",
                            value="sha1",
                            on_change=lambda e: account_info_dict.update(
                                algorithm=e.value
                            ),
                        ).style("width: 40%").bind_value(account_info_dict, "algorithm")

                        ui.select(
                            options=["TOTP", "HOTP"],
                            value=account_info_dict["type"],
                            label="Type",
                            on_change=lambda e: account_info_dict.update(type=e.value),
                        ).style("width: 40%").bind_value(account_info_dict, "type")

                        ui.number(
                            label="Counter",
                            value=account_info_dict["counter"],
                            step=1,
                            placeholder=30,
                            precision=0,
                            on_change=lambda e: account_info_dict.update(
                                counter=e.value
                            ),
                        ).style("width: 100%").bind_value(account_info_dict, "counter")

                    ui.checkbox(
                        "Active",
                        value=account_info_dict["is_active"],
                        on_change=lambda e: account_info_dict.update(is_active=e.value),
                    ).style("width: 100%").bind_value(account_info_dict, "is_active")

                    ui.checkbox(
                        "Password Protected",
                        value=account_info_dict["is_password_protected"],
                        on_change=lambda e: account_info_dict.update(
                            is_password_protected=e.value
                        ),
                    ).style("width: 100%").bind_value(
                        account_info_dict, "is_password_protected"
                    )

                    ui.button(
                        "Delete Account",
                        on_click=lambda info=account_info_dict: delete_dialogue(
                            info
                        ).open(),
                    ).tooltip("This action is irreversible!").tailwind.background_color(
                        color.RED
                    )

            nav_bar()


@logger.catch
@ui.page("/account/delete")
def delete_account_page(secret):
    logger.debug(secret)
    delete_account(secret)
    ui.open("/")


@logger.catch
def delete_dialogue(account_info_dict: dict):
    with ui.dialog() as d:
        with ui.card():
            ui.label("Are you sure you want to delete this account?")
            with ui.row().style("alig-content: center; "):
                ui.button(
                    "Yes",
                    on_click=lambda e: ui.open(
                        f"/account/delete?secret={account_info_dict['secret']}"
                    ),
                ).tailwind.background_color(color.RED)
                ui.button("No", on_click=lambda e: d.close()).tailwind.background_color(
                    color.GREEN
                )

    return d


def copy_to_clipboard(text: str):
    ui.copy_to_clipboard(text)
    ui.notify(f"Copied {text} to clipboard", color=color.GREEN)


@ui.page("/account/{name}")
##@logger.catch
def account(name: str):
    logger.debug(f"Name: {name}")

    try:
        account_information = search_accounts_by_name(name)[0]
    except IndexError:
        account_information = search_accounts_by_name(name)

    logger.debug(f"Account Information: {account_information}")

    with ui.card().style("height: 585px"):
        with ui.column().style("height: 100%"):
            with ui.row().style("width: 100%;").classes("flex justify-between"):
                ui.button(
                    icon=icon.ARROW_BACK, on_click=lambda e: ui.back()
                ).tailwind().background_color(color.TRANSPARENT)
                ui.label(account_information["name"]).tailwind().font_size("2xl")
                ui.button(
                    icon=icon.EDIT,
                    on_click=lambda name=account_information["name"]: ui.open(
                        f"/account/{account_information['name']}/edit?secret={account_information['secret']}&otp_type={account_information['type']}"
                    ),
                ).tailwind().background_color(color.TRANSPARENT)

            with ui.scroll_area().style("height: 80%").classes("flex justify-center"):
                if account_information:
                    with ui.row().style("width: 100%;").classes("flex justify-center"):
                        ui.space()
                        if account_information["icon"]:
                            ui.icon(
                                icon=account_information["icon"]
                            ).tailwind().font_size("6xl")
                        else:
                            ui.icon(icon.KEY).style(
                                "border-radius: 50%; border: 2px solid grey;"
                            ).tailwind().font_size("6xl")
                        ui.space()

                    ui.label(account_information["name"]).tailwind().font_size("2xl")

                    with ui.row().style("width: 100%;").classes("flex justify-center"):
                        if account_information["type"] == "TOTP":
                            totp = pyotp.TOTP(
                                account_information["secret"],
                                digits=account_information["digits"],
                                interval=account_information["counter"],
                                name=account_information["name"],
                                issuer=account_information["issuer"],
                            )

                            totp.timecode(datetime.datetime.now(datetime.timezone.utc))

                            otp = {
                                "value": totp.now(),
                                "progress_value": int(
                                    totp.interval
                                    - datetime.datetime.now(
                                        datetime.timezone.utc
                                    ).timestamp()
                                )
                                % totp.interval,
                            }

                            ui.label(otp["value"]).on(
                                "click",
                                lambda e: copy_to_clipboard(otp["value"]),
                            ).bind_text(otp, "value").style(
                                "cursor: pointer; font-size: 5rem;"
                            )

                            ui.timer(
                                1,
                                lambda: [
                                    otp.update(
                                        progress_value=otp["progress_value"] - 1
                                        if otp["progress_value"] > 0
                                        else account_information["counter"] - 1,
                                    ),
                                    otp.update(value=totp.now()),
                                ],
                            )

                    with ui.row().style("width: 100%;").classes("flex justify-center"):
                        ui.label("Expires in:").tailwind().font_size("lg").align_self(
                            "center"
                        )
                        ui.circular_progress(
                            value=otp["progress_value"],
                            max=account_information["counter"],
                            reverse=True,
                            rounded=True,
                        ).bind_value_from(
                            otp,
                            "progress_value",
                        )

                        ui.label("Seconds").tailwind().font_size("lg").align_self(
                            "center"
                        )

                    with ui.row().style("width: 100%;").classes("flex justify-center"):
                        ui.space()
                        ui.button(
                            icon=icon.COPY_ALL,
                            on_click=lambda e: copy_to_clipboard(
                                totp.at(otp["progress_value"])
                            ),
                        ).tailwind().background_color(color.GREEN)

            # add our nav bar
            nav_bar()


@ui.page("/")
# @logger.catch
def main():
    def search(query):
        """Search as you type."""

        # global running_query
        # if running_query:
        #    running_query.cancel()  # cancel the previous query; happens when you type fast
        # search_field.classes("mt-2", remove="mt-24")  # move the search field up

        results_area.clear()
        # store the http coroutine in a task so we can cancel it later if needed
        response = search_accounts_by_name(query)

        logger.debug(response)
        # logger.debug(f"Search Field: {search_field.value}")

        info["results"] = response
        if search_field.value != "":
            with results_area:
                logger.debug(response)

                for account in info["results"]:
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
                                    color=random.choice(list(vars(color).values())),
                                )
                            with ui.item_section():
                                ui.item_label(account["name"]).tailwind().font_size(
                                    "lg"
                                )

        else:
            if info["accounts"]:
                with results_area:
                    # logger.debug(info["accounts"])
                    for account in info["accounts"]:
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
                                        color=random.choice(list(vars(color).values())),
                                    )
                                with ui.item_section():
                                    ui.item_label(account["name"]).tailwind().font_size(
                                        "lg"
                                    )
            else:
                with results_area:
                    ui.label("No accounts found").style("width: 100%")
                    ui.button(
                        "Add Account",
                        icon=icon.ADD,
                        on_click=lambda e: ui.open("/add"),
                    ).style("width: 100%")

    info = {}
    all_accounts = get_all_accounts()
    info["accounts"] = all_accounts
    info["results"] = []

    with ui.card().style("height: 585px"):
        with ui.column().style("height: 100%"):
            with ui.row().style("width: 100%").style(
                ui.Style(alignment=ui.alignment.start)
            ):
                search_field = ui.input(
                    value="",
                    placeholder="Search",
                    on_change=lambda e: search(e.value),
                ).style("width: 80%; height: 20%")

                ui.button(
                    color=color.SECONDARY,
                    icon=icon.ADD,
                    on_click=lambda e: ui.open("/add"),
                ).style(f"width: 10%; {ui.Style(alignment=ui.alignment.center)}")

            if isinstance(info["results"], list) and info["results"] != []:
                results_area = ui.scroll_area().style("height: 80%")

            else:
                if info["accounts"]:
                    with ui.scroll_area().style("height: 80%") as results_area:
                        # logger.debug(info["accounts"])
                        for account in info["accounts"]:
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
                                            # color=random.choice(
                                            #     list(vars(color).values())
                                            # ),
                                        )
                                    with ui.item_section():
                                        ui.item_label(
                                            account["name"]
                                        ).tailwind().font_size("lg")
                else:
                    with ui.scroll_area().style("height: 80%") as results_area:
                        ui.label("No accounts found").style("width: 100%")
                        ui.button(
                            "Add Account",
                            icon=icon.ADD,
                            on_click=lambda e: ui.open("/add"),
                        ).style("width: 100%")

            nav_bar()


if __name__ in {"__main__", "__mp_main__"}:
    # we need to first remove the default logger and then add a new one for the levels to work
    logger.remove()
    logger.add(sys.stderr, level="DEBUG")

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
