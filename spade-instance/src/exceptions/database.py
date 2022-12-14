from __future__ import annotations


class CollectionDoesNotExistException(Exception):
    def __init__(self, collection_name: str):
        super().__init__(f"Collection {collection_name} does not exist")
