# System import
import os, subprocess, threading


# Lib imports


# Apoplication imports


class Launcher:
    def openFilelocally(self, file):
        lowerName = file.lower()
        command   = []

        if lowerName.endswith(self.fvideos):
            command = [self.media_app]

            if "mplayer" in self.media_app:
                command += self.mplayer_options

            command += [file]
        elif lowerName.endswith(self.fimages):
            command = [self.image_app, file]
        elif lowerName.endswith(self.fmusic):
            command = [self.music_app, file]
        elif lowerName.endswith(self.foffice):
            command = [self.office_app, file]
        elif lowerName.endswith(self.ftext):
            command = [self.text_app, file]
        elif lowerName.endswith(self.fpdf):
            command = [self.pdf_app, file]
        else:
            command = [self.file_manager_app, file]

            self.logger.debug(command)
        DEVNULL = open(os.devnull, 'w')
        subprocess.Popen(command, start_new_session=True, stdout=DEVNULL, stderr=DEVNULL, close_fds=True)


    def remuxVideo(self, hash, file):
        remux_vid_pth = self.REMUX_FOLDER + "/" + hash + ".mp4"
        self.logger.debug(remux_vid_pth)

        if not os.path.isfile(remux_vid_pth):
            self.check_remux_space()

            command = ["ffmpeg", "-i", file, "-hide_banner", "-movflags", "+faststart"]
            if file.endswith("mkv"):
                command += ["-codec", "copy", "-strict", "-2"]
            if file.endswith("avi"):
                command += ["-c:v", "libx264", "-crf", "21", "-c:a", "aac", "-b:a", "192k", "-ac", "2"]
            if file.endswith("wmv"):
                command += ["-c:v", "libx264", "-crf", "23", "-c:a", "aac", "-strict", "-2", "-q:a", "100"]
            if file.endswith("f4v") or file.endswith("flv"):
                command += ["-vcodec", "copy"]

            command += [remux_vid_pth]
            try:
                proc = subprocess.Popen(command)
                proc.wait()
            except Exception as e:
                self.logger.debug(message)
                self.logger.debug(e)
                return False

        return True


    def generate_video_thumbnail(self, fullPath, hashImgPth):
        try:
            proc = subprocess.Popen([self.FFMPG_THUMBNLR, "-t", "65%", "-s", "300", "-c", "jpg", "-i", fullPath, "-o", hashImgPth])
            proc.wait()
        except Exception as e:
            self.logger.debug(repr(e))
            self.ffprobe_generate_video_thumbnail(fullPath, hashImgPth)


    def generate_video_thumbnail(self, fullPath, hashImgPth):
        proc = None
        try:
            # Stream duration
            command  = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=duration", "-of", "default=noprint_wrappers=1:nokey=1", fullPath]
            data     = subprocess.run(command, stdout=subprocess.PIPE)
            duration = data.stdout.decode('utf-8')

            # Format (container) duration
            if "N/A" in duration:
                command  = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", fullPath]
                data     = subprocess.run(command , stdout=subprocess.PIPE)
                duration = data.stdout.decode('utf-8')

            # Stream duration type: image2
            if "N/A" in duration:
                command  = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-f", "image2", "-show_entries", "stream=duration", "-of", "default=noprint_wrappers=1:nokey=1", fullPath]
                data     = subprocess.run(command, stdout=subprocess.PIPE)
                duration = data.stdout.decode('utf-8')

            # Format (container) duration type: image2
            if "N/A" in duration:
                command  = ["ffprobe", "-v", "error", "-f", "image2", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", fullPath]
                data     = subprocess.run(command , stdout=subprocess.PIPE)
                duration = data.stdout.decode('utf-8')

            # Get frame roughly 35% through video
            grabTime = str( int( float( duration.split(".")[0] ) * 0.35) )
            command  = ["ffmpeg", "-ss", grabTime, "-an", "-i", fullPath, "-s", "320x180", "-vframes", "1", hashImgPth]
            proc     = subprocess.Popen(command, stdout=subprocess.PIPE)
            proc.wait()
        except Exception as e:
            print("Video thumbnail generation issue in thread:")
            print( repr(e) )
            self.logger.debug(repr(e))


    def check_remux_space(self):
        limit = self.remux_folder_max_disk_usage
        try:
            limit = int(limit)
        except Exception as e:
            self.logger.debug(e)
            return

        usage = self.getRemuxFolderUsage(self.REMUX_FOLDER)
        if usage > limit:
            files = os.listdir(self.REMUX_FOLDER)
            for file in files:
                fp = os.path.join(self.REMUX_FOLDER, file)
                os.unlink(fp)


    def getRemuxFolderUsage(self, start_path = "."):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp): # Skip if it is symbolic link
                    total_size += os.path.getsize(fp)

        return total_size
