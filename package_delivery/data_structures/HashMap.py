import csv


# Individual packages with their delivery relevant information to be represented as HashMap entries
# Will be the values in key_value pair to enter into Hash Map
class HashMapEntry:

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
        return f'<{self.package_id} {self.address} {self.city} {self.state} {self.zipcode} {self.delivery_deadline} {self.mass} {self.special_notes}>'


class HashMap:

    def __init__(self, initial_size=10):
        # Initialize HashMap with empty buckets entries i.e. list
        self.map = []
        for i in range(initial_size):
            self.map.append([])

    # Hash function to generate bucket index of Hash Map, direct hashing package_id
    def _get_hash(self, key):
        bucket = key % len(self.map)
        return bucket

    # Insert new packages into hash Map
    def insert_package(self, key, value):
        bucket = self._get_hash(key)  # Get bucket
        bucket_list = self.map[bucket]  # Get bucket list where item will go
        key_value = [key, value]  # Key-entry pair

        # showing 10 empty buckets, followed by 30 filled buckets, not inserting into firstly into emtpy ones
        # print(bucket)

        # Showing ['int', <HashTable.HashTableEntry object at 0000>], 7/14/23 not anymore, changed class name to
        # HashMap7/15/23 print(key_value)

        if bucket_list is None:
            bucket_list = [key_value]
            self.map = bucket_list
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
        bucket = self._get_hash(key)
        bucket_list = self.map[bucket]

        if bucket_list is not None:
            for key_value_pair in bucket_list:
                if key_value_pair[0] == key:
                    return key_value_pair[1].address
            return None

    def get_key_from_address(self, address):
        for bucket in self.map:
            for key_value_pair in bucket:
                if key_value_pair[1].address == address:
                    return key_value_pair[0]
        return None

    def get_hashmap(self):
        return self.map

    def get_packages(self):
        hashmap = self.get_hashmap()
        return hashmap

    def print_get_all_packages(self):
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

    # To update value in key-value pair if changed
    def update_value(self, key, value):
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

    # Find key-value pair to delete
    def delete_key_value(self, key):
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


# Load Hash Map object with the values from csv file
def load_hash_map(fileName):
    """
    Load data from a CSV file into a hash map.

    Args:
        fileName (str): The name of the CSV file.

    Returns:
        HashMap: The hash map containing the loaded data.
    """
    insert_into_hash_map = HashMap()
    try:
        with open(fileName) as csv_file:
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

                    # Key to directly hash
                    key = package_id

                    # HashMapEntry object
                    value = HashMapEntry(package_id, address, city, state, zipcode, delivery_deadline, mass, special_notes)
                    insert_into_hash_map.insert_package(key, value)
                except Exception as e:
                    print(f"Error occurred while processing package: {e}")
    except Exception as e:
        print(f"Error occurred while loading hash map: {e}")

    return insert_into_hash_map


# Get full list of values printed, testing purposes for functions editing list
def get_hash_map_all():
    for i in range(1, 41):
        print(package_hashmap.get_value_from_key(i))


# Check if all packages exist in HashMap object for testing purposes
def check_all_packages(hashmap, total_packages=40):
    for package_id in range(1, total_packages + 1):
        if hashmap.get_value_from_key(package_id) is None:
            return False
    return True


# Hash Map object instance to insert into HashMap
package_hashmap = load_hash_map(r'C:\Users\brand\IdeaProjects\Package_Delivery_Program_New\package_delivery'
                                r'\data_structures\WGUPS Package File Formatted.csv')


# print(sorted(package_hashmap.get_packages(), key=lambda x: x[0], reverse=True))

# all_packages_exist = check_all_packages(package_hashmap)
# print("ALL_PACKAGES_EXIST: ", all_packages_exist)
# get_hash_map_all() # Print HashMap correctly 7/19/23

# print(package_hashmap) # Printing HashMap object 7/19/23

# print(package_hashmap.get_address_from_key(40)) # Printing addresses from key correctly 7/19/23

# print(package_hashmap.get_key_from_address('4300 S 1300 E')) # Printing package_id from address correctly 7/19/23
# Print the current working directory
