import hashlib

def hash_file(filepath):

    sha = hashlib.sha256()

    with open(filepath, "rb") as file:

        while True:

            chunk = file.read(4096)

            if not chunk:
                break

            sha.update(chunk)

    return sha.hexdigest()