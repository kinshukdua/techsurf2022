import math

def convert_size(size_bytes: int) -> str:
   """
   A function to convert bytes to human readable values (MBs, GBs, etc.)
   """    
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

def get_size(fobj: object) -> int:
    """
    A function to get the size of a file in bytes
    """
    if fobj.content_length:
        return fobj.content_length
    try:
        pos = fobj.tell()
        fobj.seek(0, 2)  #seek to end
        size = fobj.tell()
        fobj.seek(pos)  # back to original position
        return size
    except (AttributeError, IOError):
        pass
    # in-memory file object that doesn't support seeking or tell
    return 0  #assume small enough