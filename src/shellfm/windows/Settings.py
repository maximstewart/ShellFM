# System import
from os import path


# Lib imports


# Apoplication imports



class Settings:
    logger            = None
    ABS_THUMBS_PTH    = None   # Used for thumbnail generation and is set by passing in
    REMUX_FOLDER      = None   # Used for Remuxed files and is set by passing in
    FFMPG_THUMBNLR    = None   # Used for thumbnail generator binary and is set by passing in
    HIDE_HIDDEN_FILES = True
    lock_folder       = True
    go_past_home      = False

    subpath           = "/LazyShare"  # modify 'home' folder path
    locked_folders    = "Synced Backup::::venv::::flasks".split("::::")
    mplayer_options   = "-quiet -really-quiet -xy 1600 -geometry 50%:50%".split()
    music_app         = "/opt/deadbeef/bin/deadbeef"
    media_app         = "mpv"
    image_app         = "mirage"
    office_app        = "libreoffice"
    pdf_app           = "evince"
    text_app          = "leafpad"
    file_manager_app  = "spacefm"
    remux_folder_max_disk_usage = "8589934592"


    fvideos = ('.mkv', '.avi', '.flv', '.mov', '.m4v', '.mpg', '.wmv', '.mpeg', '.mp4', '.webm')
    foffice = ('.doc', '.docx', '.xls', '.xlsx', '.xlt', '.xltx', '.xlm', '.ppt', 'pptx', '.pps', '.ppsx', '.odt', '.rtf')
    fimages = ('.png', '.jpg', '.jpeg', '.gif', '.ico', '.tga')
    ftext   = ('.txt', '.text', '.sh', '.cfg', '.conf')
    fmusic  = ('.psf', '.mp3', '.ogg', '.flac', '.m4a')
    fpdf    = ('.pdf')
