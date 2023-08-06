import os


def get_filenames_in_folder(path: str) -> list:
    """Given a folder path, get a list of filenames in that folder."""
    file_list = []
    for filename in os.listdir(path):
        if os.path.isfile(os.path.join(path, filename)):
            if filename not in file_list:
                file_list.append(filename)
    file_list.sort()
    return file_list
