# Python Imports
import os, subprocess, threading, hashlib
from os.path import isfile, join

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
    def create_icon(self, dir, file):
        full_path = dir + "/" + file
        return self.get_icon_image(dir, file, full_path)

    def get_icon_image(self, dir, file, full_path):
        try:
            thumbnl = None

            # Video icon
            if file.lower().endswith(self.fvideos):
                thumbnl = self.create_thumbnail(dir, file)
                # thumbnl = Gtk.Image.new_from_file(self.DEFAULT_ICONS + "/video.png")
            # Image Icon
            elif file.lower().endswith(self.fimages):
                thumbnl = self.create_scaled_image(full_path, self.VIDEO_ICON_WH)
            # .desktop file parsing
            elif full_path.lower().endswith( ('.desktop',) ):
                thumbnl = self.parse_desktop_files(full_path)
            # System icons
            else:
                thumbnl = self.get_system_thumbnail(full_path, self.SYS_ICON_WH[0])

            if thumbnl == None: # If no icon whatsoever, return internal default
                thumbnl = Gtk.Image.new_from_file(self.DEFAULT_ICON)

            return thumbnl
        except Exception as e:
            print("Icon generation issue:")
            print( repr(e) )
            return Gtk.Image.new_from_file(self.DEFAULT_ICON)

    def create_thumbnail(self, dir, file):
        full_path = dir + "/" + file
        try:
            file_hash    = hashlib.sha256(str.encode(full_path)).hexdigest()
            hash_img_pth = self.ABS_THUMBS_PTH + "/" + file_hash + ".jpg"
            if isfile(hash_img_pth) == False:
                self.generate_video_thumbnail(full_path, hash_img_pth)

            thumbnl = self.create_scaled_image(hash_img_pth, self.VIDEO_ICON_WH)
            if thumbnl == None: # If no icon whatsoever, return internal default
                thumbnl = Gtk.Image.new_from_file(self.DEFAULT_ICONS + "/video.png")

            return thumbnl
        except Exception as e:
            print("Thumbnail generation issue:")
            print( repr(e) )
            return Gtk.Image.new_from_file(self.DEFAULT_ICONS + "/video.png")

    def parse_desktop_files(self, full_path):
        try:
            xdgObj      = DesktopEntry(full_path)
            icon        = xdgObj.getIcon()
            alt_icon_path = ""

            if "steam" in icon:
                name         = xdgObj.getName()
                file_hash    = hashlib.sha256(str.encode(name)).hexdigest()
                hash_img_pth = self.STEAM_ICONS_PTH + "/" + file_hash + ".jpg"

                if isfile(hash_img_pth) == True:
                    # Use video sizes since headers are bigger
                    return self.create_scaled_image(hash_img_pth, self.VIDEO_ICON_WH)

                exec_str  = xdgObj.getExec()
                parts     = exec_str.split("steam://rungameid/")
                id        = parts[len(parts) - 1]
                imageLink = self.STEAM_BASE_URL + id + "/header.jpg"
                proc      = subprocess.Popen(["wget", "-O", hash_img_pth, imageLink])
                proc.wait()

                # Use video thumbnail sizes since headers are bigger
                return self.create_scaled_image(hash_img_pth, self.VIDEO_ICON_WH)
            elif os.path.exists(icon):
                return self.create_scaled_image(icon, self.SYS_ICON_WH)
            else:
                alt_icon_path = ""

                for dir in self.ICON_DIRS:
                    alt_icon_path = self.traverse_icons_folder(dir, icon)
                    if alt_icon_path is not "":
                        break

                return self.create_scaled_image(alt_icon_path, self.SYS_ICON_WH)
        except Exception as e:
            print(self.DEFAULT_ICON)
            print(".desktop icon generation issue:")
            print( repr(e) )
            return None


    def traverse_icons_folder(self, path, icon):
        alt_icon_path = ""

        for (dirpath, dirnames, filenames) in os.walk(path):
            for file in filenames:
                appNM = "application-x-" + icon
                if icon in file or appNM in file:
                    alt_icon_path = dirpath + "/" + file
                    break

        return alt_icon_path


    def get_system_thumbnail(self, filename, size):
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


    def generate_video_thumbnail(self, full_path, hash_img_pth):
        try:
            proc = subprocess.Popen([self.FFMPG_THUMBNLR, "-t", "65%", "-s", "300", "-c", "jpg", "-i", full_path, "-o", hash_img_pth])
            proc.wait()
        except Exception as e:
            self.logger.debug(repr(e))
            self.ffprobe_generate_video_thumbnail(full_path, hash_img_pth)


    def ffprobe_generate_video_thumbnail(self, full_path, hash_img_pth):
        proc = None
        try:
            # Stream duration
            command  = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=duration", "-of", "default=noprint_wrappers=1:nokey=1", full_path]
            data     = subprocess.run(command, stdout=subprocess.PIPE)
            duration = data.stdout.decode('utf-8')

            # Format (container) duration
            if "N/A" in duration:
                command  = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", full_path]
                data     = subprocess.run(command , stdout=subprocess.PIPE)
                duration = data.stdout.decode('utf-8')

            # Stream duration type: image2
            if "N/A" in duration:
                command  = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-f", "image2", "-show_entries", "stream=duration", "-of", "default=noprint_wrappers=1:nokey=1", full_path]
                data     = subprocess.run(command, stdout=subprocess.PIPE)
                duration = data.stdout.decode('utf-8')

            # Format (container) duration type: image2
            if "N/A" in duration:
                command  = ["ffprobe", "-v", "error", "-f", "image2", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", full_path]
                data     = subprocess.run(command , stdout=subprocess.PIPE)
                duration = data.stdout.decode('utf-8')

            # Get frame roughly 35% through video
            grabTime = str( int( float( duration.split(".")[0] ) * 0.35) )
            command  = ["ffmpeg", "-ss", grabTime, "-an", "-i", full_path, "-s", "320x180", "-vframes", "1", hash_img_pth]
            proc     = subprocess.Popen(command, stdout=subprocess.PIPE)
            proc.wait()
        except Exception as e:
            print("Video thumbnail generation issue in thread:")
            print( repr(e) )
            self.logger.debug(repr(e))


    def create_scaled_image(self, path, wxh):
        try:
            pixbuf         = Gtk.Image.new_from_file(path).get_pixbuf()
            scaled_pixbuf = pixbuf.scale_simple(wxh[0], wxh[1], 2)  # 2 = BILINEAR and is best by default
            return Gtk.Image.new_from_pixbuf(scaled_pixbuf)
        except Exception as e:
            print("Image Scaling Issue:")
            print( repr(e) )
            return None

    def create_from_file(self, path):
        try:
            return Gtk.Image.new_from_file(path)
        except Exception as e:
            print("Image from file Issue:")
            print( repr(e) )
            return None

    def return_generic_icon(self):
        return Gtk.Image.new_from_file(self.DEFAULT_ICON)
