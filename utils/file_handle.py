import os


def remove_file(file_field):
    if file_field:
        if os.path.isfile(file_field.path):
            os.remove(file_field.path)
