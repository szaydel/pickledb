"""
Copyright Harrison Erd

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
contributors may be used to endorse or promote products derived from this
software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import os
import orjson

class pkldb:
    """
    A orjson-based key-value store with essential methods: set, get, dump,
    delete, purge, and all.
    """

    def __init__(self, location, auto_dump=False):
        """
        Initialize the pkldb object.

        Args:
            location (str): Path to the JSON file.
            auto_dump (bool): Automatically save changes to the file.
        """
        self.location = os.path.expanduser(location)
        self.auto_dump = auto_dump
        self._load()

    def _load(self):
        """
        Load data from the JSON file if it exists, or initialize an empty
        database.
        """
        if os.path.exists(self.location) and os.path.getsize(self.location) > 0:
            try:
                with open(self.location, 'rb') as f:
                    self.db = orjson.loads(f.read())
                    print("Database loaded.")
            except Exception as e:
                self.db = {}
                print(f"{e}\nDatabase failed to load. Empty database created.")
        else:
            self.db = {}

    def dump(self):
        """
        Save the database to the file using an atomic dump.

        Behavior:
            - Writes to a temporary file and replaces the
              original file only after the write is successful,
              ensuring data integrity.
        """
        temp_location = f"{self.location}.tmp"
        try:
            with open(temp_location, 'wb') as temp_file:
                temp_file.write(orjson.dumps(self.db))  # Serialize and write in one step
            os.replace(temp_location, self.location)  # Atomic replace
        except Exception as e:
            print(f"Failed to write database to disk: {e}")

    def set(self, key, value):
        """
        Add or update a key-value pair in the database.

        Args:
            key (any): The key to set. If the key is not a string, it will be
                       converted to a string.
            value (any): The value to associate with the key.

        Returns:
            bool: True if the operation succeeds.

        Behavior:
            - If the key already exists, its value will be updated.
            - If the key does not exist, it will be added to the database.
            - Automatically dumps the database to disk if `auto_dump`
              is enabled.
        """
        key = str(key) if not isinstance(key, str) else key
        self.db[key] = value
        if self.auto_dump:
            self.dump()
        return True

    def remove(self, key):
        """
        Remove a key and its value from the database.

        Args:
            key (any): The key to delete. If the key is not a string, it will
             be converted to a string.

        Returns:
            bool: True if the key was deleted, False if the key does not exist.
        """
        key = str(key) if not isinstance(key, str) else key
        if key in self.db:
            del self.db[key]
            if self.auto_dump:
                self.dump()
            return True
        return False

    def purge(self):
        """
        Clear all keys from the database.

        Returns:
            bool: True if the operation succeeds.
        """
        self.db.clear()
        if self.auto_dump:
            self.dump()
        return True

    def get(self, key):
        """
        Get the value associated with a key.

        Args:
            key (any): The key to retrieve. If the key is not a string, it will
                       be converted to a string.

        Returns:
            any: The value associated with the key, or None if the key does
            not exist.
        """
        key = str(key) if not isinstance(key, str) else key
        return self.db.get(key)

    def all(self):
        """
        Get a list of all keys in the database.

        Returns:
            list: A list of all keys.
        """
        return list(self.db.keys())
