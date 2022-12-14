from __future__ import annotations


class CollectionDoesNotExistException(Exception):
    def __init__(self, collection_name: str):
        super().__init__(f"Collection {collection_name} does not exist")


class DatabaseNotSetException(Exception):
    def __init__(self):
        super().__init__("Database not set")


class DatabaseClientNotSetException(Exception):
    def __init__(self):
        super().__init__("Database client not set")
