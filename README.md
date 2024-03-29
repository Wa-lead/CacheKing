
# CacheKing: Analysis Tool for Computational Efficiency

CacheKing serves as an insightful analysis tool that illuminates the potential efficiencies to be gained through intelligent caching in Python applications. Rather than being a direct utility for caching, CacheKing is designed to help developers identify opportunities for optimization in computational tasks. By highlighting repetitive and expensive function calls that can benefit from caching, it provides a foundation for enhancing performance in data processing, scientific calculations, and algorithmic analysis.

## Concept

The core idea behind CacheKing is to analyze the execution patterns of your code, particularly focusing on functions that are called multiple times with the same arguments. CacheKing tracks these calls and simulates the impact of caching on reducing computation time and resource usage. This analysis helps in making informed decisions about implementing caching mechanisms in performance-critical sections of your projects.

## Installation

As an analysis tool, CacheKing is integrated into your Python projects for the purpose of performance evaluation. Ensure Python 3.6 or later is installed for compatibility.

```
pip install git+https://github.com/wa-lead/CacheKing.git
```

## Usage

To utilize CacheKing for analysis, wrap the sections of code where you suspect caching could bring performance improvements. Here's an example showing how to analyze potential caching benefits in a pathfinding scenario:

```python
from CacheKing import CacheKing

[DEFINE YOUR PROGRAM HERE]

with CacheKing():
	[YOUR MAIN SCRIPT]
```
#

## Example: Pathfinding Analysis

Consider a scenario where you're calculating the shortest paths between points, factoring in obstacles. Such computations are often repeated with identical inputs, making them ideal candidates for caching.

##### Example.py:

```python

import pandas as pd
import numpy as np
from functools import lru_cache
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
	'location_id': range(1, 101), # 100 locations
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

	results_df = pd.DataFrame(results)
	print(results_df.head())
```

##### `CacheKing` Anslysis Output:

```
+--------------------+-------+------------+--------------+----------------------+----------------+
|      Function      | Calls | Cache Hits | Cache Misses | Total Time (seconds) | Recommendation |
+--------------------+-------+------------+--------------+----------------------+----------------+
| calculate_distance | 34650 |   29106    |     5544     |        0.0124        |      High      |
|   shortest_path    |  4950 |     0      |     4950     |        0.1279        |      Low       |
+--------------------+-------+------------+--------------+----------------------+----------------+

Caching Recommendations:
calculate_distance: Could benefit from caching
shortest_path: Unlikely to benefit significantly from caching

```


The included sample script demonstrates CacheKing's application in analyzing the efficiency of caching in a simulated pathfinding task among 100 locations. By reviewing the analysis report generated by CacheKing, you can identify which calculations are prime targets for caching, guiding your optimization efforts.

## Insightful Reporting

CacheKing offers detailed reports on function call patterns, highlighting:

- Repetitive calls with identical inputs
- Potential time savings through caching
- Recommendations on caching strategies based on call frequency and computational expense
