import os
import shutil


def copy_files(source, destination):
    try:
        if os.path.exists(destination):
            shutil.rmtree(destination)
        os.mkdir(destination)

        for elem in os.listdir(source):
            elem_path = os.path.join(source, elem)
            destination_elem_path = os.path.join(destination, elem)
            if os.path.isfile(elem_path):
                shutil.copy2(elem_path, destination_elem_path)
            elif os.path.isdir(elem_path):
                copy_files(elem_path, destination_elem_path)
    except Exception as e:
        print('Failed to copy files. Reason: %s' % (e))
