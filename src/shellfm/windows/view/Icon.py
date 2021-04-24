# Python Imports
import os, subprocess, hashlib, threading
from os.path import isdir, isfile, join


# Gtk imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk
from gi.repository import Gio
from xdg.DesktopEntry import DesktopEntry


# Application imports




def threaded(fn):
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper

class Icon:
    def __init__(self):
        self.SCRIPT_PTH        = os.path.dirname(os.path.realpath(__file__)) + "/"
        self.INTERNAL_ICON_PTH = self.SCRIPT_PTH + "./utils/icons/text.png"


    def createIcon(self, dir, file):
        fullPath = dir + "/" + file
        return self.getIconImage(file, fullPath)

    def createThumbnail(self, dir, file):
        fullPath = dir + "/" + file
        try:
            fileHash   = hashlib.sha256(str.encode(fullPath)).hexdigest()
            hashImgPth = self.get_home() + "/.thumbnails/normal/" + fileHash + ".png"

            thumbnl = self.createScaledImage(hashImgPth, self.viIconWH)
            if thumbnl == None: # If no icon whatsoever, return internal default
                thumbnl = Gtk.Image.new_from_file(self.SCRIPT_PTH + "./utils/icons/video.png")

            return thumbnl
        except Exception as e:
            print("Thumbnail generation issue:")
            print( repr(e) )
            return Gtk.Image.new_from_file(self.SCRIPT_PTH + "./utils/icons/video.png")


    def getIconImage(self, file, fullPath):
        try:
            thumbnl = None

            # Video icon
            if file.lower().endswith(self.fvideos):
                thumbnl = Gtk.Image.new_from_file(self.SCRIPT_PTH + "./utils/icons/video.png")
            # Image Icon
            elif file.lower().endswith(self.fimages):
                thumbnl = self.createScaledImage(fullPath, self.viIconWH)
            # .desktop file parsing
            elif fullPath.lower().endswith( ('.desktop',) ):
                thumbnl = self.parseDesktopFiles(fullPath)
            # System icons
            else:
                thumbnl = self.getSystemThumbnail(fullPath, self.systemIconImageWH[0])

            if thumbnl == None: # If no icon whatsoever, return internal default
                thumbnl = Gtk.Image.new_from_file(self.INTERNAL_ICON_PTH)

            return thumbnl
        except Exception as e:
            print("Icon generation issue:")
            print( repr(e) )
            return Gtk.Image.new_from_file(self.INTERNAL_ICON_PTH)

    def parseDesktopFiles(self, fullPath):
        try:
            xdgObj      = DesktopEntry(fullPath)
            icon        = xdgObj.getIcon()
            altIconPath = ""

            if "steam" in icon:
                steamIconsDir = self.get_home() + "/.thumbnails/steam_icons/"
                name          = xdgObj.getName()
                fileHash      = hashlib.sha256(str.encode(name)).hexdigest()

                if isdir(steamIconsDir) == False:
                    os.mkdir(steamIconsDir)

                hashImgPth = steamIconsDir + fileHash + ".jpg"
                if isfile(hashImgPth) == True:
                    # Use video sizes since headers are bigger
                    return self.createScaledImage(hashImgPth, self.viIconWH)

                execStr   = xdgObj.getExec()
                parts     = execStr.split("steam://rungameid/")
                id        = parts[len(parts) - 1]
                imageLink = "https://steamcdn-a.akamaihd.net/steam/apps/" + id + "/header.jpg"
                proc      = subprocess.Popen(["wget", "-O", hashImgPth, imageLink])
                proc.wait()

                # Use video thumbnail sizes since headers are bigger
                return self.createScaledImage(hashImgPth, self.viIconWH)
            elif os.path.exists(icon):
                return self.createScaledImage(icon, self.systemIconImageWH)
            else:
                iconsDirs   = ["/usr/share/pixmaps", "/usr/share/icons", self.get_home() + "/.icons" ,]
                altIconPath = ""

                for iconsDir in iconsDirs:
                    altIconPath = self.traverseIconsFolder(iconsDir, icon)
                    if altIconPath is not "":
                        break

                return self.createScaledImage(altIconPath, self.systemIconImageWH)
        except Exception as e:
            print(".desktop icon generation issue:")
            print( repr(e) )
            return None


    def traverseIconsFolder(self, path, icon):
        altIconPath = ""

        for (dirpath, dirnames, filenames) in os.walk(path):
            for file in filenames:
                appNM = "application-x-" + icon
                if icon in file or appNM in file:
                    altIconPath = dirpath + "/" + file
                    break

        return altIconPath


    def getSystemThumbnail(self, filename, size):
        try:
            if os.path.exists(filename):
                gioFile   = Gio.File.new_for_path(filename)
                info      = gioFile.query_info('standard::icon' , 0, Gio.Cancellable())
                icon      = info.get_icon().get_names()[0]
                iconTheme = Gtk.IconTheme.get_default()
                iconData  = iconTheme.lookup_icon(icon , size , 0)
                if iconData:
                    iconPath  = iconData.get_filename()
                    return Gtk.Image.new_from_file(iconPath)  # This seems to cause a lot of core dump issues...
                else:
                    return None
            else:
                return None
        except Exception as e:
            print("system icon generation issue:")
            print( repr(e) )
            return None


    def createScaledImage(self, path, wxh):
        try:
            pixbuf       = Gtk.Image.new_from_file(path).get_pixbuf()
            scaledPixBuf = pixbuf.scale_simple(wxh[0], wxh[1], 2)  # 2 = BILINEAR and is best by default
            return Gtk.Image.new_from_pixbuf(scaledPixBuf)
        except Exception as e:
            print("Image Scaling Issue:")
            print( repr(e) )
            return None

    def createFromFile(self, path):
        try:
            return Gtk.Image.new_from_file(path)
        except Exception as e:
            print("Image from file Issue:")
            print( repr(e) )
            return None

    def returnGenericIcon(self):
        return Gtk.Image.new_from_file(self.INTERNAL_ICON_PTH)
