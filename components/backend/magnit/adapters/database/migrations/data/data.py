import json
import pathlib

parent_dir = pathlib.Path(__file__).parent.resolve()

# paths
trailers_data = pathlib.PurePath(
    parent_dir, 'trailers_data.json'
)
trucks_data = pathlib.PurePath(
    parent_dir, 'trucks_data.json'
)
contracts_data = pathlib.PurePath(
    parent_dir, 'contracts_data.json'
)
partners_data = pathlib.PurePath(
    parent_dir, 'partners_data.json'
)
polygon_details_data = pathlib.PurePath(
    parent_dir, 'polygon_details.json'
)
permits_data = pathlib.PurePath(
    parent_dir, 'permits_data.json'
)
drivers_data = pathlib.PurePath(
    parent_dir, 'drivers_data.json'
)
visits_data = pathlib.PurePath(
    parent_dir, 'visits.json'
)

# json
trailers = json.load(open(trailers_data))
trucks = json.load(open(trucks_data))
contracts = json.load(open(contracts_data))
partners = json.load(open(partners_data))
polygon_details = json.load(open(polygon_details_data))
permits = json.load(open(permits_data))
drivers = json.load(open(drivers_data))
visits = json.load(open(visits_data))
