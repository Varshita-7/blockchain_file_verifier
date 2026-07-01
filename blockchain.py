import json
import hashlib
import os
from datetime import datetime

class Block:

    def __init__(
        self,
        index,
        filename,
        file_hash,
        previous_hash,
        timestamp=None,
        block_hash=None
    ):

        self.index = index
        self.filename = filename
        self.file_hash = file_hash
        self.previous_hash = previous_hash

        self.timestamp = (
            timestamp
            if timestamp
            else datetime.now().isoformat()
        )

        self.block_hash = (
            block_hash
            if block_hash
            else self.calculate_hash()
        )

    def calculate_hash(self):

        data = (
            str(self.index)
            + self.filename
            + self.file_hash
            + self.previous_hash
            + self.timestamp
        )

        return hashlib.sha256(
            data.encode()
        ).hexdigest()

    def to_dict(self):

        return {
            "index": self.index,
            "filename": self.filename,
            "file_hash": self.file_hash,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "block_hash": self.block_hash
        }


class Blockchain:

    def __init__(self, username):

        os.makedirs(
            "blockchain_data",
            exist_ok=True
        )

        self.file = (
            f"blockchain_data/"
            f"{username}_chain.json"
        )

        if os.path.exists(self.file):

            with open(self.file, "r") as f:
                data = json.load(f)

            self.chain = [
                Block(**block)
                for block in data
            ]

        else:

            self.chain = [
                self.create_genesis()
            ]

            self.save()

    def create_genesis(self):

        return Block(
            0,
            "Genesis",
            "Genesis",
            "0"
        )

    def add_block(
        self,
        filename,
        file_hash
    ):

        previous = self.chain[-1]

        block = Block(
            len(self.chain),
            filename,
            file_hash,
            previous.block_hash
        )

        self.chain.append(block)

        self.save()

    def save(self):

        with open(self.file, "w") as f:

            json.dump(
                [
                    block.to_dict()
                    for block
                    in self.chain
                ],
                f,
                indent=4
            )