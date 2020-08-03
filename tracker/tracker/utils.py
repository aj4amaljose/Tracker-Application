"""
General Utilities
"""
import os
import io


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


def covert_byte_io_obj_to_string_io_obj(byte_obj):
    """
    Coverts ByteIO to StringIo
    """
    byte_obj.seek(0)
    byte_str = byte_obj.getvalue()
    text_obj = byte_str.decode('UTF-8')
    str_obj = io.StringIO(text_obj)
    return str_obj
