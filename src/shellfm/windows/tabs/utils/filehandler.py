# Python imports
import os
import shutil

# Lib imports

# Application imports




class FileHandler:
    def create_file(self, nFile, type):
        try:
            if type == "dir":
                os.mkdir(nFile)
            elif type == "file":
                open(nFile, 'a').close()
        except Exception as e:
            print("An error occured creating the file/dir:")
            print(repr(e))
            return False

        return True

    def update_file(self, oFile, nFile):
        try:
            print(f"Renaming:  {oFile}  -->  {nFile}")
            os.rename(oFile, nFile)
        except Exception as e:
            print("An error occured renaming the file:")
            print(repr(e))
            return False

        return True

    def delete_file(self, to_delete_file):
        try:
            print(f"Deleting:  {to_delete_file}")
            if os.path.exists(to_delete_file):
                if os.path.isfile(to_delete_file):
                    os.remove(to_delete_file)
                elif os.path.isdir(to_delete_file):
                    shutil.rmtree(to_delete_file)
                else:
                    print("An error occured deleting the file:")
                    return False
            else:
                print("The folder/file does not exist")
                return False
        except Exception as e:
            print("An error occured deleting the file:")
            print(repr(e))
            return False

        return True

    def move_file(self, fFile, tFile):
        try:
            print(f"Moving:  {fFile}  -->  {tFile}")
            if os.path.exists(fFile) and not os.path.exists(tFile):
                if not tFile.endswith("/"):
                    tFile += "/"

                shutil.move(fFile, tFile)
            else:
                print("The folder/file does not exist")
                return False
        except Exception as e:
            print("An error occured moving the file:")
            print(repr(e))
            return False

        return True

    def copy_file(self, fFile, tFile, symlinks = False, ignore = None):
        try:
            if os.path.isdir(fFile):
                shutil.copytree(fFile, tFile, symlinks, ignore)
            else:
                shutil.copy2(fFile, tFile)
        except Exception as e:
            print("An error occured copying the file:")
            print(repr(e))
            return False

        return True
