import locale

__version__ = "0.1.0"

def get_os_language():
    """Returns the ISO language code of the OS."""
    lang, _ = locale.getlocale()
    return lang[0:2]
