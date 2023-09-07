import csv
from pathlib import Path


# Individual packages with their delivery relevant information to be represented as HashMap entries
# Will be the values in key_value pair to enter into Hash Map
class HashMapEntry:
    """
    Class to represent a HashMap entry to be used in a HashMap.

    Attributes:
        package_id (int): The ID of the package.
        address (str): The address of the package.
        city (str): The city of the package.
        state (str): The state of the package.
        zipcode (str): The zipcode of the package.
        delivery_deadline (str): The delivery deadline of the package.
        mass (str): The mass of the package.
        special_notes (str): Any special notes for the package.
    """

    def __init__(self, package_id, address, city, state, zipcode, delivery_deadline, mass, special_notes):
        """
        Initialize a package object.

        Args:
            package_id (int): The ID of the package.
            address (str): The address of the package.
            city (str): The city of the package.
            state (str): The state of the package.
            zipcode (str): The zipcode of the package.
            delivery_deadline (str): The delivery deadline of the package.
            mass (str): The mass of the package.
            special_notes (str): Any special notes for the package.

        Raises:
            TypeError: If any of the arguments have an invalid type.

        Returns:
            None
        """
        if not isinstance(package_id, int):
            raise TypeError('Package ID must be an integer')
        if not isinstance(address, str):
            raise TypeError('Address must be a string')
        if not isinstance(city, str):
            raise TypeError('City must be a string')
        if not isinstance(state, str):
            raise TypeError('State must be a string')
        if not isinstance(zipcode, str):
            raise TypeError('Zipcode must be a string')
        if not isinstance(delivery_deadline, str):
            raise TypeError('Delivery deadline must be a string')
        if not isinstance(mass, str):
            raise TypeError('Mass must be a string')
        if not isinstance(special_notes, str):
            raise TypeError('Special notes must be a string')

        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.delivery_deadline = delivery_deadline
        self.mass = mass
        self.special_notes = special_notes

    # Overwrite print(HashMapEntry) otherwise it will print object reference, 7/14/23 working for now
    def __repr__(self):
        """
        Returns a string representation of the object.

        Returns:
            str: A string representation of the object.
        """
        return f'<{self.package_id} {self.address} {self.city} {self.state} {self.zipcode} {self.delivery_deadline} {self.mass} {self.special_notes}>'


class HashMap:
    """
    Class to represent a HashMap to store package information.

    Attributes:
        map (list): A list of buckets.
    """

    def __init__(self, initial_size=10):
        """
        Initialize a HashMap.

        Parameters:
            initial_size (int): The initial size of the HashMap.
        """
        # Initialize HashMap with empty buckets entries i.e. list
        self.map = []
        for i in range(initial_size):
            self.map.append([])

    # Hash function to generate bucket index of Hash Map, direct hashing package_id
    def _get_hash(self, key):
        """
        Calculate the hash value for the given key.

        Parameters:
            key (int): The key for which the hash value needs to be calculated.

        Returns:
            int: The calculated hash value.
        """
        bucket = key % len(self.map)
        return bucket

    # Insert new packages into hash Map
    def _insert_package(self, key, value):
        """
        Inserts a key-value pair into the hash table.

        Parameters:
            key (int): The key to be inserted into the hash table.
            value (HashMapEntry): The corresponding value to be inserted.

        Returns:
            bool: True if the insertion was successful, False otherwise.
        """
        bucket = self._get_hash(key)  # Get bucket
        bucket_list = self.map[bucket]  # Get a bucket list where item will go
        key_value = [key, value]  # Key-entry pair

        # showing 10 empty buckets, followed by 30 filled buckets, not inserting into firstly into emtpy ones
        # print(bucket)

        # Showing ['int', <HashTable.HashTableEntry object at 0000>], 7/14/23 not anymore, changed class name to
        # HashMap7/15/23 print(key_value)

        if bucket_list is None:
            bucket_list = [key_value]
            # self.map = bucket_list
            return True
        # If not, insert the item to the end of the bucket list.
        else:
            for pair in bucket_list:
                if pair[0] == key:
                    pair[1] = value
                    return True
            bucket_list.append(key_value)
            return True

    # Get value in key-value pair data from packaged_id of Hash Map
    def get_value_from_key(self, key):
        """
        Given a key, this function retrieves the corresponding value from the hash map.

        Parameters:
            key (int): The key to search for in the hash map.

        Returns:
            HashMapEntry: The value associated with the given key, or None if the key is not found.
        """
        bucket = self._get_hash(key)
        bucket_list = self.map[bucket]

        if bucket_list is not None:
            # print(bucket_list)
            # enumerate bucket list does not work 7/14/23
            for pair in bucket_list:
                if pair[0] == key:
                    return pair[1]
            return None

    def get_address_from_key(self, key):
        """
        Retrieves the address associated with a given key from the hash map.

        Args:
            key (int): The key to search for in the hash map.

        Returns:
            Union[str, None]: The address associated with the key, or None if the key is not found.
        """
        bucket = self._get_hash(key)
        bucket_list = self.map[bucket]

        if bucket_list is not None:
            for key_value_pair in bucket_list:
                if key_value_pair[0] == key:
                    return key_value_pair[1].address
            return None

    def get_key_from_address(self, address):
        """
        Returns the key associated with the given address in the map.

        Parameters:
            address (str): The address to search for in the map.

        Returns:
            int: The key associated with the given address, or None if the address is not found.
        """
        for bucket in self.map:
            for key_value_pair in bucket:
                if key_value_pair[1].address == address:
                    return key_value_pair[0]
        return None

    def get_hashmap(self):
        """
        Returns the hashmap associated with the object.
        """
        return self.map

    def get_packages(self):
        """
        Returns the hashmap associated with the object.
        """
        hashmap = self.get_hashmap()
        return hashmap

    def print_get_all_packages(self):
        """
        Prints all the packages stored in the map.
        """
        print("All Packages:")
        print("-" * 40)

        for bucket_index, bucket in enumerate(self.map):
            print(f"Bucket {bucket_index}:")
            if not bucket:
                print("No packages in this bucket")
            else:
                for package_id, package in bucket:
                    print(f"Package ID: {package_id}")
                    print(package)
                    print("-" * 20)
            print("=" * 40)

    # To update value in a key-value pair if changed
    def update_key_value_pair(self, key, value):
        """
        Updates the value of a key in the map.

        Parameters:
            key (int): The key to update the value for.
            value (HashMapEntry): The new value to update the key with.

        Returns:
            bool: True if the value was updated successfully, False otherwise.
        """
        bucket = self._get_hash(key)
        bucket_list = self.map[bucket]

        if bucket_list is not None:
            for pairs in bucket_list:
                if pairs[0] == key:  # Find the key-value pair and update if found
                    pairs[1] = value
                    print(f"Updated value: {pairs[1]}")
                    return True
        else:
            print(f"Error updating package with key: {key}")

    # Find a key-value pair to delete
    def delete_key_value_pair(self, key):
        """
        Deletes a key-value pair from the map based on the given key.

        Parameters:
            key (int): The key of the key-value pair to be deleted.

        Returns:
            bool: True if the key-value pair was successfully deleted, False otherwise.
        """
        bucket = self._get_hash(key)
        bucket_list = self.map[bucket]

        if bucket_list is None:
            return False
        for pairs in bucket_list:
            if pairs[0] == key:
                # Remove bucket_list key-value pair key is pairs[0] now inside that it is the first
                bucket_list.remove([pairs[0], pairs[1]])
                # bucket_list pairs[1] value list
                return True
        else:
            print("Error deleting key-value pair with key: " + key)

    # Load a Hash Map object with the values from csv file
    def load_hash_map(self, file_name):
        """
        Loads the contents of a CSV file into a hash map.

        Parameters:
            file_name (str): The name of the CSV file to load.

        Returns:
            None: If an error occurs while loading the hash map.
            self: The instance of the class after the CSV file is successfully loaded into the hash map.
        """
        # Get the current directory where this file is
        current_directory = Path(__file__).parent
        # Construct the full path to the CSV file
        csv_path = current_directory / file_name
        try:
            with csv_path.open('r') as csv_file:
                csv_reader = csv.reader(csv_file)

                for package in csv_reader:
                    try:
                        package_id = int(package[0])
                        address = package[1]
                        city = package[2]
                        state = package[3]
                        zipcode = package[4]
                        delivery_deadline = package[5]
                        mass = package[6]
                        special_notes = package[7]

                        # Key to direct hash
                        key = package_id

                        # HashMapEntry object
                        value = HashMapEntry(package_id, address, city, state, zipcode, delivery_deadline, mass,
                                             special_notes)
                        self._insert_package(key, value)
                    except Exception as e:
                        print(f"Error occurred while processing package: {e}")
        except Exception as e:
            print(f"Error occurred while loading hash map: {e}")
            return None

        return self

    # Print a full list of values printed, testing purposes for a function editing list
    def print_hash_map_all(self):
        """
        Prints all values from the hash map.

        This function iterates over the keys from 1 to 40 and prints the corresponding value
        from the `package_hashmap` using the `get_value_from_key` method.

        Returns:
            None
        """
        for i in range(1, 41):
            print(self.get_value_from_key(i))

    # Check if all packages exist in HashMap object for testing purposes
    def check_all_packages(self):
        """
        Checks if all packages have values assigned to them.

        Returns:
            bool: True if all packages have values assigned, False otherwise.
        """
        TOTAL_PACKAGES = 40
        for package_id in range(1, TOTAL_PACKAGES + 1):
            if self.get_value_from_key(package_id) is None:
                return False
        return True


# Create a hash map and load it with data from WGUPS Package File Formatted.csv of all packages
package_hashmap = HashMap()
package_hashmap.load_hash_map('WGUPS Package File Formatted.csv')
