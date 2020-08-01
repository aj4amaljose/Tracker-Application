"""
General Utilities
"""
import os


def delete_file_if_exists(filename):
    """
    Delete file if file exists in the path

    :param filename: File path
    """
    is_deleted = False
    try:
        if os.path.exists(filename):
            os.remove(filename)
            is_deleted = True
    except:
        is_deleted = True
    finally:
        return is_deleted
