import ctypes
import os

from whoosh import index
from whoosh.fields import Schema
from whoosh.qparser import QueryParser

import sygil_authy

from .config.db.Model import Account, Options

if not os.path.exists("db"):
    os.mkdir("db")

module_name = sygil_authy

APP_ID = f"sygil_authy.Sygil-Dev.version.{module_name.__version__}"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)


def set_icon(icon_path: str = "src/sygil_authy/assets/icon.ico") -> None:
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


def first_run() -> bool:
    """
    Checks if the index 'options' exists in the 'db' database. If the index does not exist,
    it sets the default configuration by calling the 'set_default_config()' function and
    returns True. Otherwise, it returns False.

    Returns:
        bool: True if the index 'options' does not exist and the default configuration is set,
              False otherwise.
    """
    if not check_if_index_exists("db", "options") or not check_if_index_exists(
        "db", "accounts"
    ):
        set_default_config()
        make_account_index()
        return True
    else:
        return False


def create_index(schema: Schema, indexname: str) -> index.Index:
    """
    Create an index using the specified schema and index name.

    Args:
        schema (Schema): The schema to be used for the index.
        indexname (str): The name of the index.

    Returns:
        Index: The created index.

    Raises:
        OSError: If there is an error creating the index.

    Example:
        >>> schema = Schema(id=ID(stored=True), name=TEXT(stored=True))
        >>> index = create_index(schema, "my_index")
    """
    ix = index.create_in("db", schema=schema, indexname=indexname)
    return ix


def open_index(dirname: str, indexname: str, schema: Schema) -> index.Index:
    """
    Opens an index in the specified directory with the given name and schema.

    Args:
        dirname (str): The directory path where the index is located.
        indexname (str): The name of the index to be opened.
        schema (Schema): The schema object defining the index structure.

    Returns:
        Index: The opened index object.

    Raises:
        OSError: If the index directory or file cannot be accessed.
        index.EmptyIndexError: If the index is empty or does not exist.
        index.IndexVersionError: If the index version is incompatible.

    Example:
        >>> schema = Schema(title=TEXT(stored=True), content=TEXT)
        >>> ix = open_index('/path/to/index', 'my_index', schema)
    """
    ix = index.open_dir(dirname=dirname, indexname=indexname, schema=schema)
    return ix


def check_if_index_exists(dirname: str, indexname: str) -> bool:
    """
    Check if an index exists in a directory.

    Args:
        dirname (str): The directory path.
        indexname (str): The name of the index.

    Returns:
        bool: True if the index exists, False otherwise.
    """
    return index.exists_in(dirname, indexname=indexname)


def make_account_index() -> index.Index:
    """
    Creates and returns an instance of the index.Index class for managing accounts.

    This function initializes an index for storing and retrieving account objects.
    It uses the create_index function from the index module to create the index.

    Returns:
        index.Index: An instance of the index.Index class.
    """
    if check_if_index_exists("db", "accounts"):
        ix = index.open_dir("db", indexname="accounts", schema=Account)
    else:
        ix = create_index(Account(), "accounts")
    return ix


def add_account(account: dict) -> None:
    """
    Add an account to the database index.

    This function adds a new account to the database index. If the index already exists,
    it opens the existing index. Otherwise, it creates a new index.

    Parameters:
    - account (dict): A dictionary representing the account to be added. The dictionary
      should contain the necessary fields for the account.

    Returns:
    - None

    Example usage:
    ```
    account = {
        "username": "john_doe",
        "email": "john@example.com",
        "website": "example.com",
    }
    add_account(account)
    ```

    Note:
        - The function assumes that the necessary imports and index-related functions are available.
        - The function assumes that the index schema is defined as `Account`.
    """
    if check_if_index_exists("db", "accounts"):
        ix = index.open_dir("db", indexname="accounts", schema=Account)
    else:
        ix = make_account_index()

    writer = ix.writer()
    writer.add_document(**account)
    writer.commit(merge=True, optimize=True)


def delete_account(account_id: int) -> None:
    """
    Delete an account from the database.

    Args:
        account_id (int): The ID of the account to be deleted.

    Returns:
        None

    Raises:
        None

    Notes:
        This function deletes an account from the database by performing the following steps:
        1. Open the index directory named "db" with the schema defined as Account.
        2. Create a writer object to perform write operations on the index.
        3. Delete the account with the specified account_id by using the "delete_by_term" method of the writer.
        4. Commit the changes made by the writer to the index, merging and optimizing the index.

    Example:
        delete_account(123)  # Delete the account with ID 123 from the database.
    """
    ix = index.open_dir("db", indexname="accounts", schema=Account)
    writer = ix.writer()
    writer.delete_by_term("id", account_id)
    writer.commit(merge=True, optimize=True)


def update_account(account: dict) -> None:
    ix = index.open_dir("db", indexname="accounts", schema=Account)
    writer = ix.writer()
    writer.update_document(**account)
    writer.commit(merge=True, optimize=True)


def search_accounts_by_name(name: str) -> list:
    ix = index.open_dir("db", indexname="accounts", schema=Account)

    print(name)

    qp = QueryParser("name", schema=ix.schema)
    q = qp.parse(name)

    searcher = ix.searcher()
    results = searcher.search(q)

    # print(results)

    return list(results)


def get_all_accounts(last_version=True):
    ix = index.open_dir("db", indexname="accounts", schema=Account)

    with ix.searcher() as searcher:
        results = searcher.documents()

        return list(results)


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
