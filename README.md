# **Package Delivery Program**

**Overview:**

The Package Delivery Program simulates the delivery of packages throughout a city
using various algorithms to determine the most efficient routes.
The system optimizes delivery based on distance, time,
and other constraints such as delivery deadlines and special instructions.

**Features:**

Dynamic Route Optimization: The program uses algorithms like Nearest Neighbor, Dijkstra's Shortest Path, and Two-Opt to determine the best route for package delivery.

Real-Time Fuel Price Updates (not present in UI currently): Integrates with an API to fetch current fuel prices,
allowing the route optimization to also consider fuel costs.

Visual Route Tracking: Utilizes matplotlib to provide a visual representation of the truck's route,
showing the progression of deliveries in real-time.

Time Tracking: Monitors the time taken for each delivery,
ensuring that packages with specific delivery deadlines are prioritized.

Efficient Data Structures: Employs hash maps for O(1)
average time complexity in package lookups and insertions and a graph to perform efficient package delivery operations

**Directory Structure:**

algorithms/: Contains various algorithms used for route optimization.

datastructures/: Includes core data structures like graphs and hash maps.

delivery/: Core logic for package delivery, including truck routing and logistics like fuel tracking.

gui/: (not implemented currently) Graphical user interface components.

visualization/: Scripts for visualizing truck routes.

**Prerequisites:**

Python 3.11

Required Python packages as listed in requirements.txt.


**Installation & Setup:**

1. Clone the repository or download the project zip.
2. Navigate to the project directory: cd\path_to_Package_Delivery_Program_New
3. Activate virtual environment: venv\Scripts\activate
4. Install the required packages: pip install -r requirements.txt

**Running the Program:**

From the project directory: python main.py

**Contributing:**

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

