from whoosh.analysis import StemmingAnalyzer
from whoosh.fields import BOOLEAN, DATETIME, ID, NUMERIC, TEXT, SchemaClass

analyzer = StemmingAnalyzer(stoplist=None)


class Options(SchemaClass):
    """
    Represents the options for the application.

    Attributes:
        id (str): The unique identifier for the options.
        app_title (str): The title of the application.
        theme_mode (str): The theme mode of the application.
        language (str): The language used in the application.
        show_nav_bar_labels (bool): Flag indicating whether to show navigation bar labels.
        expand_search_filters (bool): Flag indicating whether to expand search filters.
        per_category_sorting (bool): Flag indicating whether to enable per-category sorting.
        automatic_updates_interval (float): The interval for automatic updates.
        automatically_refresh_metadata (bool): Flag indicating whether to automatically refresh metadata.
        show_pending_requests_count (bool): Flag indicating whether to show a badge for the number of pending requests.
    """

    id = ID(stored=True, unique=True)
    app_title = TEXT(stored=True)
    theme_mode = TEXT(stored=True)
    language = TEXT(stored=True)
    show_nav_bar_labels = BOOLEAN(stored=True)
    expand_search_filters = BOOLEAN(stored=True)
    per_category_sorting = BOOLEAN(stored=True)
    automatic_updates_interval = NUMERIC(stored=True)
    automatically_refresh_metadata = BOOLEAN(stored=True)
    show_pending_requests_count = BOOLEAN(stored=True)


class Account(SchemaClass):
    """
    Represents an account in the database.

    Attributes:
        id (str): The unique identifier for the account.
        secret (str): The secret key associated with the account.
        name (str): The name of the account.
        alias (str): An alias for the account.
        icon (str): The icon associated with the account.
        issuer (str): The issuer of the account.
        label (str): The label for the account.
        algorithm (str): The algorithm used for generating the OTP.
        digits (int): The number of digits in the OTP.
        type (str): The type of the account.
        website (str): The website associated with the account.
        counter (int): The counter value for HOTP accounts.
        username (str): The username associated with the account.
        recovery_code (str): The recovery code for the account.
        backup_codes (str): The backup codes for the account.
        last_used (int): The timestamp of the last time the account was used.
        is_active (bool): Indicates if the account is active.
        is_password_protected (bool): Indicates if the account is password protected.
        password (str): The password associated with the account.
    """

    # id = ID(stored=True, unique=True)
    secret = ID(stored=True, unique=True, sortable=True)
    name = TEXT(analyzer=analyzer, stored=True, sortable=True)
    alias = TEXT(analyzer=analyzer, stored=True, sortable=True)
    icon = TEXT(stored=True, sortable=True)
    issuer = TEXT(analyzer=analyzer, stored=True, sortable=True)
    label = TEXT(analyzer=analyzer, stored=True, sortable=True)
    algorithm = TEXT(stored=True, sortable=True)
    digits = NUMERIC(stored=True, sortable=True)
    type = TEXT(analyzer=analyzer, stored=True, sortable=True)
    website = TEXT(analyzer=analyzer, stored=True, sortable=True)
    counter = NUMERIC(stored=True, sortable=True)
    username = TEXT(analyzer=analyzer, stored=True, sortable=True)
    last_used = DATETIME(stored=True, sortable=True)
    is_active = BOOLEAN(stored=True)
    is_password_protected = BOOLEAN(stored=True)
    password = TEXT(stored=True, sortable=True)
