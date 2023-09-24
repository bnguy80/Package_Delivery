import csv
from pathlib import Path

import requests


# current_directory = Path(__file__).parent
# print(f"Current directory is: {current_directory}") # Debug line

class FuelTracker:
    __FUEL_PRICE_CACHE = None  # To make sure the fuel price is only fetched once

    _instance = None  # Single instance storage
    _initialized = False  # Initialization flag

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(FuelTracker, cls).__new__(cls)
        return cls._instance

    def __init__(self, truck_id):
        # Initialize the class attributes once
        if not FuelTracker._initialized:
            # Consumption rate of each truck
            self.__MPG = 18.0
            # Fuel price per gallon fetched from API
            if FuelTracker.__FUEL_PRICE_CACHE is None:
                FuelTracker.__FUEL_PRICE_CACHE = self.fetch_fuel_price()
            self.__FUEL_PRICE = FuelTracker.__FUEL_PRICE_CACHE
            self.__TRAVEL_COST = {}
            self.total_fuel_used = {}
            self.track_fuel_current_level = {}
            FuelTracker._initialized = True

        # Initialize full tank for each truck
        if truck_id not in self.__TRAVEL_COST:
            self.__TRAVEL_COST[truck_id] = 0
        if truck_id not in self.total_fuel_used:
            self.total_fuel_used[truck_id] = 0
        if truck_id not in self.track_fuel_current_level:
            self.track_fuel_current_level[truck_id] = 30

    @classmethod
    def fetch_fuel_price(cls):
        fuel_price = cls.fetch_fuel_price_csv()

        if fuel_price is None:
            cls.fetch_fuel_price_data()
            fuel_price = cls.fetch_fuel_price_csv()
        return fuel_price

    @classmethod
    def fetch_fuel_price_csv(cls):
        if cls.__FUEL_PRICE_CACHE is None:
            current_directory = Path(__file__).parent
            csv_file_path = current_directory / 'utah_gas_prices.csv'
            with open(csv_file_path, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    cls.__FUEL_PRICE_CACHE = row  # Save the data to cache
                    return float(row['gasoline'])  # Working correctly 9/1/2023
        else:
            return float(cls.__FUEL_PRICE_CACHE['gasoline'])

    @classmethod
    def fetch_fuel_price_data(cls):

        url = "https://api.collectapi.com/gasPrice/allUsaPrice"
        headers = {
            'content-type': "application/json",
            'authorization': "apikey 5xQIZnkyhWogrLXkQt27dD:61N5ZvkjpvkNVlzf8bRb5d"
        }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Failed to fetch data: {response.status_code} {response.reason}")
            return None

        data_json = response.json()

        utah_data = None

        for item in data_json['result']:
            if item['name'] == 'Utah':
                utah_data = item
                break

        # Debug line make sure API is being called
        # have rate-limit 100(?)
        print("Utah data:", utah_data)

        if utah_data:
            current_directory = Path(__file__).parent
            csv_file_path = current_directory / 'utah_gas_prices.csv'
            # Create or open a CSV file to save the Utah data
            with open(csv_file_path, 'w', newline='') as csvfile:
                fieldnames = ['name', 'gasoline', 'midGrade', 'premium', 'diesel']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                writer.writerow({
                    'name': utah_data['name'],
                    'gasoline': utah_data['gasoline'],
                    'midGrade': utah_data['midGrade'],
                    'premium': utah_data['premium'],
                    'diesel': utah_data['diesel']
                })

    def _calculate_fuel_used(self, truck_id, miles_traveled):
        fuel_used = miles_traveled / self.__MPG
        self.total_fuel_used[truck_id] += fuel_used
        return fuel_used

    def _calculate_travel_cost(self, truck_id):
        cost = self.__FUEL_PRICE * self.total_fuel_used[truck_id]
        return cost

    def update_fuel_level(self, truck_id, time_tracker):
        miles_traveled = time_tracker.get_miles_traveled()
        fuel_used = self._calculate_fuel_used(truck_id, miles_traveled)
        self.track_fuel_current_level[truck_id] -= fuel_used
        if self.track_fuel_current_level[truck_id] < 0:
            print("Fuel level is empty!")
            self.track_fuel_current_level = 0
        self.__TRAVEL_COST[truck_id] = self._calculate_travel_cost(truck_id)

    def print_fuel_level(self, truck_id):
        print(f"{truck_id} FUEL_LEVEL:", self.track_fuel_current_level[truck_id], "gallons")
        print()

    def print_fuel_used(self, truck_id):
        print(f"{truck_id} FUEL_USED:", self.total_fuel_used[truck_id], "gallons")
        print()

    def print_fuel_price(self, truck_id):
        print(f"{truck_id} FUEL_PRICE:", self.__FUEL_PRICE)

    def print_travel_cost(self, truck_id):

        print(f"{truck_id} TRAVEL_COST:", "$", int(self.__TRAVEL_COST[truck_id]), "dollars")
