from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
import folium

#print("OR-Tools Installed Successfully")

import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist

# Load optimizer results
df = pd.read_csv("optimizer_results.csv")

# Select top 10 unique ATMs
top_atms = (
    df.sort_values("Priority_Rank")
      .drop_duplicates(subset="ATM_ID")
      .head(10)
      .reset_index(drop=True)
)

# Generate coordinates
np.random.seed(42)

top_atms["Latitude"] = np.random.uniform(18.40, 18.80, len(top_atms))
top_atms["Longitude"] = np.random.uniform(73.70, 74.10, len(top_atms))

# Create distance matrix
coordinates = top_atms[["Latitude", "Longitude"]].values

distance_matrix = cdist(
    coordinates,
    coordinates,
    metric="euclidean"
)

# Convert to integer distances
distance_matrix = (distance_matrix * 1000).astype(int)

print(distance_matrix)

from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

# Create routing index manager
manager = pywrapcp.RoutingIndexManager(
    len(distance_matrix),  # number of locations
    1,                     # number of vehicles
    0                      # depot (starting point)
)

# Create Routing Model
routing = pywrapcp.RoutingModel(manager)

# Distance callback
def distance_callback(from_index, to_index):
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)
    return distance_matrix[from_node][to_node]

transit_callback_index = routing.RegisterTransitCallback(
    distance_callback
)

routing.SetArcCostEvaluatorOfAllVehicles(
    transit_callback_index
)

# Search parameters
search_parameters = pywrapcp.DefaultRoutingSearchParameters()

search_parameters.first_solution_strategy = (
    routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
)

# Solve
solution = routing.SolveWithParameters(search_parameters)

if solution:
    print("\nOptimal ATM Replenishment Route:\n")

    index = routing.Start(0)

    route = []
    total_distance = 0

    while not routing.IsEnd(index):

        node = manager.IndexToNode(index)
        route.append(top_atms.iloc[node]["ATM_ID"])

        previous_index = index
        index = solution.Value(routing.NextVar(index))

        total_distance += routing.GetArcCostForVehicle(
            previous_index,
            index,
            0
        )

    print(" -> ".join(route))

    print(f"\nTotal Distance: {total_distance} units")

else:
    print("No solution found.")
    
    import folium

# Create map
m = folium.Map(
    location=[
        top_atms["Latitude"].mean(),
        top_atms["Longitude"].mean()
    ],
    zoom_start=10
)

# Add ATM markers
for _, row in top_atms.iterrows():

    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=f"{row['ATM_ID']}",
        tooltip=row["ATM_ID"]
    ).add_to(m)

# Draw optimized route
route_coordinates = []

for atm in route:

    row = top_atms[top_atms["ATM_ID"] == atm].iloc[0]

    route_coordinates.append(
        [row["Latitude"], row["Longitude"]]
    )

folium.PolyLine(
    route_coordinates,
    weight=5,
    color="red",
    opacity=0.8
).add_to(m)

# Save map
m.save("atm_route_map.html")

print("Route map saved successfully!")

top_atms.to_csv("route_optimized_atms.csv", index=False)

print(f"Total Route Distance: {total_distance}")

with open("route_distance.txt", "w") as f:
    f.write(str(total_distance))