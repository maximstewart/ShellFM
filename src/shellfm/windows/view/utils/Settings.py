# System import
import os
from os import path

# Lib imports


# Apoplication imports



class Settings:
    logger            = None
    lock_folder       = False
    go_past_home      = True

    GTK_ORIENTATION   = 1      # HORIZONTAL (0) VERTICAL (1)
    ABS_THUMBS_PTH    = None   # Used for thumbnail generation and is set by passing in
    REMUX_FOLDER      = None   # Used for Remuxed files and is set by passing in
    FFMPG_THUMBNLR    = None   # Used for thumbnail generator binary and is set by passing in
    HIDE_HIDDEN_FILES = True

    USER_HOME         = path.expanduser('~')
    CONFIG_PATH       = USER_HOME     + "/.config/pyfm"
    DEFAULT_ICONS     = CONFIG_PATH   + "/icons"
    DEFAULT_ICON      = DEFAULT_ICONS + "/text.png"
    FFMPG_THUMBNLR    = CONFIG_PATH   + "/ffmpegthumbnailer"   # Thumbnail generator binary
    REMUX_FOLDER      = USER_HOME     + "/.remuxs"             # Remuxed files folder

    STEAM_BASE_URL    = "https://steamcdn-a.akamaihd.net/steam/apps/"
    ICON_DIRS         = ["/usr/share/pixmaps", "/usr/share/icons", USER_HOME + "/.icons" ,]
    BASE_THUMBS_PTH   = USER_HOME       + "/.thumbnails"       # Used for thumbnail generation
    ABS_THUMBS_PTH    = BASE_THUMBS_PTH + "/normal"            # Used for thumbnail generation
    STEAM_ICONS_PTH   = BASE_THUMBS_PTH + "/steam_icons"
    CONTAINER_ICON_WH = [128, 128]
    VIDEO_ICON_WH     = [256, 128]
    SYS_ICON_WH       = [56, 56]

    subpath           = "/Desktop"  # modify 'home' folder path
    # subpath           = "/Desktop"  # modify 'home' folder path
    locked_folders    = "venv::::flasks".split("::::")
    mplayer_options   = "-quiet -really-quiet -xy 1600 -geometry 50%:50%".split()
    music_app         = "/opt/deadbeef/bin/deadbeef"
    media_app         = "mpv"
    image_app         = "mirage"
    office_app        = "libreoffice"
    pdf_app           = "evince"
    text_app          = "leafpad"
    file_manager_app  = "spacefm"
    remux_folder_max_disk_usage = "8589934592"

    # Filters
    fvideos = ('.mkv', '.avi', '.flv', '.mov', '.m4v', '.mpg', '.wmv', '.mpeg', '.mp4', '.webm')
    foffice = ('.doc', '.docx', '.xls', '.xlsx', '.xlt', '.xltx', '.xlm', '.ppt', 'pptx', '.pps', '.ppsx', '.odt', '.rtf')
    fimages = ('.png', '.jpg', '.jpeg', '.gif', '.ico', '.tga')
    ftext   = ('.txt', '.text', '.sh', '.cfg', '.conf')
    fmusic  = ('.psf', '.mp3', '.ogg', '.flac', '.m4a')
    fpdf    = ('.pdf')


    # Dire structure check
    if path.isdir(REMUX_FOLDER) == False:
        os.mkdir(REMUX_FOLDER)

    if path.isdir(BASE_THUMBS_PTH) == False:
        os.mkdir(BASE_THUMBS_PTH)

    if path.isdir(ABS_THUMBS_PTH) == False:
        os.mkdir(ABS_THUMBS_PTH)

    if path.isdir(STEAM_ICONS_PTH) == False:
        os.mkdir(STEAM_ICONS_PTH)
