"""
This is a file for checking online image size
Which is copy from internet
"""
import urllib.request
from PIL import ImageFile


def getsizes(uri):
    """get file size *and* image size (None if not known)"""
    file = urllib.request.urlopen(uri)
    size = file.headers.get("content-length")
    if size:
        size = int(size)
    p = ImageFile.Parser()
    while True:
        data = file.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            # return size, p.image.size
            return size, p.image.size[0], p.image.size[1]
    file.close()
    return size, 0, 0
    # return 0, 0
1537905
