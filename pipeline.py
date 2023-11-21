import openai

import requests
import urllib.parse
from datetime import datetime

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

import googlemaps

import numpy as np
import json

import yaml

with open('API_config.yaml', 'r') as config_file:
    config_data = yaml.safe_load(config_file)

# Access the API keys as needed
openai.api_key = config_data['openai']['api_key']
GOOGLE_API_KEY = config_data['google']['api_key']

def extract_data(input_text, verbose = False):
    # Create a prompt to extract information without labels
    prompt = f"""Extract the source address, destination addresses, and the number of vehicles from the following text:\n\n{input_text}.
                    Your output should be a Python dictionary respecting the following structure and including all keys ['addresses', 'depot', 'num_vehicles', 'datetime']:
                    - addresses: list of strings of addresses, the first one being the starting point, the warehouse.
                    - depot: int, indicating the position of the warehouse in the address list, must be 0.
                    - num_vehicles: int, number of vehicles available.
                    - vehicle_capacities: List of int representing the maximum capacity for each vehicule, put capacity of 1000 if not specified in the text.
                    - demands: list of int representing the size of each order (first element should be 0 as it is the warehouse). If not specified, put size 1 for each order.
                    - shift_length: int representing the maximum length of the shift delivery in seconds. If not specified, put 28800 sec.
                    - datetime: Tuple following the following format to be interpreted by ast.literal_eval: (datetime.now().year, datetime.now().month, datetime.now().day + 1, 9, 0). Representing the delivery date mentionned, today or tomorrow, and exact time or or period of the day mentionned (morning -> 9, 0 or afternoon -> 14, 0) as well. Use datetime.now() as the reference for today's date.
                    Ensure that the output contains only the Python dictionary to be interpreted using ast.literal_eval.
                """

    # Call the GPT-3 API to get the response
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo", #"gpt-4",
        messages=[{"role": "system", "content": "You are a helpful assistant, you can only answer python dictionnary."},
                {"role": "user", "content": prompt},
                ],
        max_tokens=3000,
        temperature=0.8
    )

    # Extract information from the response
    response_text = response.choices[0].message.content

    if verbose:
        print(response_text)
    try:
        #response_text = response_text.replace("null","None") # fixing typo of chatgpt
        data = eval(response_text)

        # Check if all required keys are present
        required_keys = ['addresses', 'depot', 'num_vehicles', 'vehicle_capacities', 'demands', 'shift_length',  'datetime']
        if any(key not in data for key in required_keys):
            raise ValueError("Missing required keys in the extracted data.")

        # Check if all values have been captured
        if any(value == None for key, value in data.items()):
            raise ValueError("Missing some values in the extracted data.")

    except (ValueError, SyntaxError): # Try again
        print("ChatGPT did not output what was expected.")
        data = extract_data(input_text)

    return data

def generate_visualization_map(warehouse_address, delivery_addresses, routes, addresses):
    gmaps = googlemaps.Client(key=GOOGLE_API_KEY)

    # Get the coordinates for the warehouse address
    warehouse_location = gmaps.geocode(warehouse_address)[0]['geometry']['location']

    # Create a map centered around the warehouse
    map_center = warehouse_location

    # Convert routes to coordinate to follow
    def get_route_coordinate(gmaps, route):
        def get_route_coordinates_step(gmaps, origin, destination):
            directions_result = gmaps.directions(origin, destination, mode="driving")
            route = directions_result[0]['legs'][0]['steps']

            # Extracting coordinates from each step of the route
            coordinates = [[step['start_location']['lat'], step['start_location']['lng']] for step in route]
            # Adding the destination coordinates
            coordinates.append([route[-1]['end_location']['lat'], route[-1]['end_location']['lng']])

            return coordinates

        origin_idx, *waypoints, destination_idx = route
        origin = addresses[origin_idx]
        destination = addresses[destination_idx]

        # Get real route coordinates from Google Maps Directions API
        route_coordinates = []
        for j in range(len(waypoints)):
            waypoint = addresses[waypoints[j]]
            route_coordinates += get_route_coordinates_step(gmaps, origin, waypoint)
            origin = waypoint  # Update the origin for the next leg of the route

        route_coordinates += get_route_coordinates_step(gmaps, origin, destination)

        return route_coordinates

    routes_by_coord = []
    for route in routes:
        routes_by_coord.append(get_route_coordinate(gmaps, route))

    colors = ['red', 'blue', 'purple', 'orange', 'yellow', 'pink', 'cyan', 'brown', 'gray', 'olive', 'lime']
    hex_colors = ['#FF0000', '#0000FF', '#800080', '#FFA500', '#FFFF00', '#FFC0CB', '#00FFFF', '#A52A2A', '#808080', '#808000', '#00FF00']

    # Generate the HTML for the map
    html_content = f"""
    <html>
    <head>
      <title>My Toronto Map</title>
      <script async defer src="https://maps.googleapis.com/maps/api/js?key={GOOGLE_API_KEY}&callback=initMap"></script>
      <script>
        function initMap() {{
          var map = new google.maps.Map(document.getElementById('map'), {{
            zoom: 12,
            center: {map_center},
            styles: [
              {{
                featureType: 'poi',
                elementType: 'labels',
                stylers: [{{
                  visibility: 'off'
                }}]
              }},
              {{
                featureType: 'transit',
                elementType: 'labels',
                stylers: [{{
                  visibility: 'off'
                }}]
              }}
            ]
          }});

          var warehouseLocation = new google.maps.Marker({{
            map: map,
            position: {warehouse_location},
            title: 'Warehouse',
            icon: 'http://maps.gstatic.com/mapfiles/ms2/micons/homegardenbusiness.png'
          }});

          var deliveryAddresses = {delivery_addresses};

          deliveryAddresses.forEach(function(address) {{
            var geocoder = new google.maps.Geocoder();
            geocoder.geocode({{'address': address}}, function(results, status) {{
              if (status === 'OK') {{
                var marker = new google.maps.Marker({{
                  map: map,
                  position: results[0].geometry.location,
                  title: address
                }});
              }} else {{
                console.error('Geocode was not successful for the following reason: ' + status);
              }}
            }});
          }});
        
          var colors = ['#FF0000', '#0000FF', '#800080', '#FFA500', '#FFFF00', '#FFC0CB', '#00FFFF', '#A52A2A', '#808080', '#808000', '#00FF00'];
          var routes = {routes_by_coord};
          routes.forEach(function(route,index) {{
            var routePath = [];
            route.forEach(function(point) {{
              var latLng = new google.maps.LatLng(point[0], point[1]);
              routePath.push(latLng);
            }});

            var routePolyline = new google.maps.Polyline({{
              clickable: false,
              geodesic: true,
              strokeColor: colors[index % 5],
              strokeOpacity: 1.000000,
              strokeWeight: 5,
              map: map,
              path: routePath
            }});
          }});
        }}
        // Ensure initMap is called after the Google Maps API script is fully loaded
        window.onload = initMap;
      </script>
    </head>
    <body>
      <div id="map" style="height: 400px;"></div>
    </body>
    </html>
    """

    return html_content

def compute_cost_matrix(addresses, time_of_the_day=None, cost_type='Time'):
    # Calculate the desired departure time
    if time_of_the_day == None or time_of_the_day[0] < 2023: # If unspecified, default is tomorrow morning
        desired_departure_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day + 1, 9, 0)
    else:
        date_list = eval(str(time_of_the_day))
        desired_departure_time = datetime(*date_list)

    departure_time_unix = int(desired_departure_time.timestamp())

    assert desired_departure_time > datetime.now(), "Departure time must be in the future"

    # Split addresses into chunks of 10 addresses each
    address_chunks = [addresses[i:i+10] for i in range(0, len(addresses), 10)]

    # Initialize empty matrices to accumulate results
    cost_matrix = np.zeros((len(addresses), len(addresses)))

    # Create a URL for the Google Distance Matrix API request
    base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'

    # Iterate through address chunks and make requests
    for k, chunk1 in enumerate(address_chunks):
        for l, chunk2 in enumerate(address_chunks):
            # Construct URL for the current chunk
            origins_chunk = '|'.join(urllib.parse.quote(address) for address in chunk1)
            destinations_chunk = '|'.join(urllib.parse.quote(address) for address in chunk2)
            url_chunk = f'{base_url}origins={origins_chunk}&destinations={destinations_chunk}&departure_time={departure_time_unix}&mode=driving&key={GOOGLE_API_KEY}'

            # Send the HTTP GET request to the Google Distance Matrix API for the current chunk
            response = requests.get(url_chunk)

            # Check the html response status and API status
            assert response.status_code == 200, f"Request failed with status code: {response.status_code}"
            data = response.json()
            assert data['status'] == 'OK', f"Request failed with status: {data['status']}"

            # Extract the distance or duration values from the API response
            for i, row in enumerate(data['rows']):
                for j, element in enumerate(row['elements']):
                    assert element['status'] == 'OK', f"Computation of route between {chunk1[i]} and {chunk2[j]} failed with status {element['status']}"
                    cost_matrix[10*k + i, 10*l + j] = element['distance']['value'] if cost_type == "Distance" else element['duration_in_traffic']['value'] #Store de distance or Time

    return cost_matrix.astype(int)

def print_CVRP_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print("Optimal routes computed by the CVRP solver:\n")
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        plan_output = f"Route for vehicle {vehicle_id}:\n"
        route_duration = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data["demands"][node_index]
            plan_output += f"{node_index} -> "
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_duration += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
        plan_output += f"{manager.IndexToNode(index)}\n"
        hour = route_duration // 3600
        min = route_duration // 60 - hour * 60
        plan_output += f"Estimated duration of the route: {hour}h{min}\n"
        plan_output += f"Load of the route: {route_load}\n"
        print(plan_output)

def extract_routes(data, manager, routing, solution):
    """Extracts routes from the solution and returns a list of positions for each vehicle."""
    routes = []

    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        route = []
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route.append(node_index)
            index = solution.Value(routing.NextVar(index))

        # Add the warehouse as the final step in the route
        warehouse_index = data["depot"]
        route.append(warehouse_index)
        routes.append(route)

    return routes

def CVRP_solver(data, verbose = False):
    """Solve the CVRP problem."""

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["cost_matrix"]), data["num_vehicles"], data["depot"]
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["cost_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data["demands"][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data["vehicle_capacities"],  # vehicle maximum capacities
        True,  # start cumul to zero
        "Capacity",
    )

    # Add Duration constraint.
    dimension_name = "Duration"
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        data["shift_length"],  # vehicle maximum travel time
        True,  # start cumul to zero
        dimension_name,
    )

    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    #distance_dimension.SetGlobalSpanCostCoefficient(1)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_parameters.time_limit.FromSeconds(1)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    assert solution, "The solver did not find a feasible solution."

    if verbose:
        print_CVRP_solution(data, manager, routing, solution)

    routes = extract_routes(data, manager, routing, solution)
    return routes

def generate_google_maps_directions_link(addresses, departure_time = None):
    """
    Note that maps limits the display of 9 waypoints.
    """
    if len(addresses) < 2:
        return "At least two addresses are required for directions."

    # Encode the addresses for the URL
    encoded_addresses = [urllib.parse.quote(address) for address in addresses]

    # Create the Google Maps directions link
    directions_base_link = "https://www.google.com/maps/dir/?api=1"
    link = directions_base_link + f"&origin={encoded_addresses[0]}" + f"&destination={encoded_addresses[-1]}"
    if len(addresses) > 2:
        points = "|".join(encoded_addresses[1:-1])
        link = link + f"&waypoints={points}"

    # Add start date/time if provided
    if departure_time:
        # Convert start_time to a UNIX timestamp
        timestamp = int(departure_time.timestamp())
        link = link + f"&travelmode=driving&departure_time={timestamp}"

    return link

def compute_metrics(data, optimal_routes):

    def duration_route(data, route):
        time = 0
        for i in range(len(route)-1):
            time+=data["cost_matrix"][route[i]][route[i+1]]
        return time

    def load_route(data, route):
        load = 0
        for c in route:
            load+=data["demands"][c]
        return load

    results = []

    for route in optimal_routes:
        info = dict()
        info['route'] = route
        info['route_with_address'] = [data['addresses'][c] for c in route]
        info['duration'] = duration_route(data, route)
        info['load'] = load_route(data, route)
        info['link'] = generate_google_maps_directions_link(info['route_with_address']) 
        results.append(info)

    return sorted(results, key=lambda x: x['load'], reverse = True)

def run(input):
    """
    Main pipeline that takes the input from the client and return the optimized routes
    """
    # Step 1: Extract relevant data from the prompt using GenAI
    data = extract_data(input)

    # Step 2: Compute time matrix
    data["cost_matrix"] = compute_cost_matrix(data["addresses"], data["datetime"])

    # Step 3: Find the optimized routes using Google OR-tools
    optimal_routes = CVRP_solver(data, verbose = True)

    # Step 4: Generate results with maps directions
    results = compute_metrics(data, optimal_routes)

    return data, results