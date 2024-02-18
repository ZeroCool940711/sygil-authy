import ctypes
import os

from whoosh import index

import sygil_authy

from .config.db.Model import Account, Options

if not os.path.exists("db"):
    os.mkdir("db")

module_name = sygil_authy

APP_ID = f"sygil_authy.Sygil-Dev.version.{module_name.__version__}"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)


def set_icon(icon_path="src/sygil_authy/assets/icon.ico"):
    """
    Sets the icon of the foreground window.

    Args:
        icon_path (str, optional): The path to the icon file. Defaults to "src/sygil_authy/assets/icon.ico".

    Raises:
        FileNotFoundError: If the specified icon file is not found.

    Notes:
        - This function is specific to Windows operating system.
        - The icon file should be in .ico format.
        - The function sets both the small and big icons of the foreground window.

    Usage:
        - Call this function to set the icon of the foreground window.
        - If no icon_path is provided, it will default to "src/sygil_authy/assets/icon.ico".
    """
    user32 = ctypes.windll.user32
    hwnd = user32.GetForegroundWindow()
    ICON_SMALL = 0
    ICON_BIG = 1
    WM_SETICON = 0x0080

    LR_LOADFROMFILE = 0x00000010
    hinst = ctypes.windll.kernel32.LoadLibraryW(None)
    hicon = user32.LoadImageW(
        hinst, os.path.abspath(icon_path), 1, 0, 0, LR_LOADFROMFILE
    )

    if hicon == 0:
        raise FileNotFoundError(f"Icon file not found: {icon_path}")

    user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, hicon)
    user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, hicon)


def first_run():
    """
    Checks if the index 'options' exists in the 'db' database. If the index does not exist,
    it sets the default configuration by calling the 'set_default_config()' function and
    returns True. Otherwise, it returns False.

    Returns:
        bool: True if the index 'options' does not exist and the default configuration is set,
              False otherwise.
    """
    if not check_if_index_exists("db", "options"):
        set_default_config()
        return True
    else:
        return False


def create_index(schema, indexname):
    # Using the convenience functions
    ix = index.create_in("db", schema=schema, indexname=indexname)
    return ix


def open_index(dirname, indexname, schema):
    # Using the convenience functions
    ix = index.open_dir(dirname=dirname, indexname=indexname, schema=schema)
    return ix


def check_if_index_exists(dirname, indexname):
    return index.exists_in(dirname, indexname=indexname)


def make_account_index():
    ix = create_index(Account(), "accounts")
    return ix


def add_account(account):
    if check_if_index_exists("db", "accounts"):
        ix = index.open_dir("db", indexname="accounts", schema=Account)
    else:
        ix = make_account_index()

    writer = ix.writer()
    writer.add_document(**account)
    writer.commit(merge=True, optimize=True)


def set_default_config(reset=False):
    """
    Set default config for the app. We will use this to create the index for the first time.
    The idea is to store and access the options incrementally while keeping previous versions
    as previous/older documents in the index in case we want to revert to a previous version.
    If we want to reset everything to default, we can just delete the index and create a new one with the defaults.
    """
    defaults = {
        "app_title": "Sygil Authy",
        "theme_mode": "dark",
        "language": "en",
    }
    if reset:
        create_index(Options, "options")

    if check_if_index_exists("db", "options"):
        ix = index.open_dir("db", indexname="options", schema=Options)
    else:
        ix = create_index(Options, "options")

    writer = ix.writer()
    writer.add_document(**defaults)

    writer.commit(merge=True, optimize=True)


def get_options(dirname="db", indexname="options", last_version=True):
    """
    Retrieve options from the specified index.

    Args:
        dirname (str): The directory name where the index is located. Default is "db".
        indexname (str): The name of the index. Default is "options".
        last_version (bool): Whether to return only the last version. Default is True.

    Returns:
        result (dict or list): The options as a dictionary if last_version is True, or a list of dictionaries if last_version is False.
    """
    ix = open_index(dirname, indexname, schema=Options)
    with ix.searcher() as searcher:
        results = searcher.documents()
        if last_version:
            # return last version only
            for result in results:
                return result
        else:
            # return all versions
            return list(results)


def int_to_float(integer, multiplier=1.0):
    """Converts an integer to a float between 0.0 and 1.0, optionally multiplied by a factor.

    Args:
      integer: The integer to convert.
      multiplier: An optional factor to multiply the normalized value by (default: 1.0).

    Returns:
      A float between 0.0 and 1.0, optionally multiplied by the multiplier.
    """

    return float(integer) / float(2 ** integer.bit_length()) * multiplier


# defaults = set_default_config()
# print (first_run())
# print (get_options(last_version=True))
# print(check_if_index_exists("db", "options"))
