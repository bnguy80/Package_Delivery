import requests
import csv
from pathlib import Path


# current_directory = Path(__file__).parent
# print(f"Current directory is: {current_directory}") # Debug line

class FuelTracker:
    __FUEL_PRICE_CACHE = None  # To make sure the fuel price is only fetched once

    def __init__(self, truck_id, truck_name, time_tracker):
        # Consumption rate of each truck
        self.__MPG = 18.0
        # Fuel price per gallon fetched from API
        if FuelTracker.__FUEL_PRICE_CACHE is None:
            FuelTracker.__FUEL_PRICE_CACHE = self.fetch_fuel_price()
        self.__FUEL_PRICE = FuelTracker.__FUEL_PRICE_CACHE
        self.__TRAVEL_COST = 0
        self.total_fuel_used = 0
        # Track fuel usage, each truck has 30 gallons of fuel capacity
        self.track_fuel_current_level = {truck_id: 30}
        # Initialize full tank
        self.__id = truck_id
        self.__name = truck_name
        self.__time_tracker = time_tracker

    @classmethod
    def fetch_fuel_price(cls):
        fuel_price = cls.fetch_fuel_price_csv()

        if fuel_price is None:
            cls.fetch_fuel_price_data()
            fuel_price = cls.fetch_fuel_price_csv()
        return fuel_price

    @classmethod
    def fetch_fuel_price_csv(cls):
        current_directory = Path(__file__).parent
        csv_file_path = current_directory / 'utah_gas_prices.csv'
        with open(csv_file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                return float(row['gasoline'])  # Working correctly 9/1/2023
        return None

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
        # print("Utah data:", utah_data) # Debug line
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

    def _calculate_fuel_used(self, miles_traveled):
        fuel_used = miles_traveled / self.__MPG
        self.total_fuel_used += fuel_used
        return fuel_used

    def calculate_travel_cost(self):
        cost = self.__FUEL_PRICE * self.total_fuel_used
        return cost

    def update_fuel_level(self):
        miles_traveled = self.__time_tracker.get_miles_traveled()
        fuel_used = self._calculate_fuel_used(miles_traveled)
        self.track_fuel_current_level[self.__id] -= fuel_used
        if self.track_fuel_current_level[self.__id] < 0:
            print("Fuel level is empty!")
            self.track_fuel_current_level[self.__id] = 0
        self.__TRAVEL_COST = self.calculate_travel_cost()

    def print_fuel_level(self):
        print(f"{self.__name} FUEL_LEVEL:", self.track_fuel_current_level[self.__id], "gallons")
        print()

    def print_fuel_used(self):
        print(f"{self.__name} FUEL_USED:", self.total_fuel_used, "gallons")
        print()

    def print_fuel_price(self):
        print(f"{self.__name} FUEL_PRICE:", self.__FUEL_PRICE)

    def print_travel_cost(self):
        print(f"{self.__name} TRAVEL_COST:", "$", int(self.__TRAVEL_COST), "dollars")
