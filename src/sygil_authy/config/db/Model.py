from whoosh.fields import BOOLEAN, ID, NUMERIC, TEXT, SchemaClass


class Options(SchemaClass):
    id = ID(stored=True, unique=True)
    app_title = TEXT(stored=True)
    theme_mode = TEXT(stored=True)
    language = TEXT(stored=True)
    show_nav_bar_updates = BOOLEAN(stored=True)
    show_nav_bar_history = BOOLEAN(stored=True)
    show_nav_bar_labels = BOOLEAN(stored=True)
    expand_search_filters = BOOLEAN(stored=True)
    recommendations_in_overflow_menu = BOOLEAN(stored=True)
    merge_in_overflow_menu = BOOLEAN(stored=True)
    per_category_sorting = BOOLEAN(stored=True)
    automatic_updates_interval = NUMERIC(stored=True)
    automatically_refresh_metadata = BOOLEAN(stored=True)
    show_unread_count_in_update_button = BOOLEAN(stored=True)
