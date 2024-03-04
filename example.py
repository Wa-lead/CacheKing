import pandas as pd
import numpy as np
from itertools import combinations
from CacheKing import CacheKing


def calculate_distance(point_a, point_b):
    return np.sqrt((point_b[0] - point_a[0])**2 + (point_b[1] - point_a[1])**2)

def shortest_path(point_a, point_b, obstacles_hash):
    # Convert hash back to obstacles list
    path_distance = calculate_distance(point_a, point_b)
    for obstacle in obstacles:
        detour_distance = calculate_distance(point_a, obstacle) + calculate_distance(obstacle, point_b)
        path_distance = min(path_distance, detour_distance)
    return path_distance


with CacheKing():
    data = {
        'location_id': range(1, 101),  # 100 locations
        'x_coord': np.random.rand(100) * 100,
        'y_coord': np.random.rand(100) * 100,
    }
    locations_df = pd.DataFrame(data)

    obstacles = [(20, 30), (50, 60), (70, 80)]

    # Calculate shortest paths between all pairs of locations
    pairs = combinations(locations_df['location_id'], 2)
    results = []

    for pair in pairs:
        loc_a = locations_df.loc[locations_df['location_id'] == pair[0], ['x_coord', 'y_coord']].iloc[0]
        loc_b = locations_df.loc[locations_df['location_id'] == pair[1], ['x_coord', 'y_coord']].iloc[0]
        distance = shortest_path(tuple(loc_a), tuple(loc_b), obstacles)
        results.append({'pair': pair, 'distance': distance})

    # Convert results to a DataFrame
    results_df = pd.DataFrame(results)

    print(results_df.head())
