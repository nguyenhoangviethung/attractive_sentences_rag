import hashlib

class Utilities:
    def hash_filename(filename):
        return hashlib.md5(filename.encode('utf-8')).hexdigest()
