import types
import functools
from collections import defaultdict
import time
from .utils import make_hashable  # Assuming this utility function is correctly implemented
import types
import functools
import time
from collections import defaultdict
from prettytable import PrettyTable

def CacheKingDecorator(cls):
    class WrappedClass:
        def __init__(self, *args, **kwargs):
            self._instance = cls(*args, **kwargs)
            self._cache = defaultdict(dict)
            self._stats = defaultdict(lambda: {'hits': 0, 'misses': 0, 'total_time': 0, 'calls': 0})

        def __getattribute__(self, name):
            # Bypass for internal attributes
            if name.startswith('_'):
                return object.__getattribute__(self, name)

            attr = object.__getattribute__(self, '_instance').__getattribute__(name)
            if isinstance(attr, types.MethodType):
                # Use functools.partial to ensure 'method' and 'method_name' are correctly passed to 'cache_method'
                cache_method = object.__getattribute__(self, 'cache_method')
                return functools.partial(cache_method, attr, name)
            else:
                return attr

        def cache_method(self, method, method_name, *args, **kwargs):
            # Record the start time for performance measurement
            start = time.time()

            try:
                # Attempt to create a hashable key for caching
                key = make_hashable((args, frozenset(kwargs.items())))
            except TypeError:
                # If arguments cannot be made hashable, execute the method without caching
                result = method(*args, **kwargs)
                self._stats[method_name]['calls'] += 1
                return result

            if key in self._cache[method_name]:
                # Cache hit
                result = self._cache[method_name][key]
                self._stats[method_name]['hits'] += 1
            else:
                # Cache miss: call the method and store the result in cache
                result = method(*args, **kwargs)
                self._cache[method_name][key] = result
                self._stats[method_name]['misses'] += 1

            # Update performance statistics
            elapsed_time = time.time() - start
            self._stats[method_name]['calls'] += 1
            self._stats[method_name]['total_time'] += elapsed_time

            return result

        def report(self):
            table = PrettyTable()
            table.field_names = ["Method", "Calls", "Cache Hits", "Cache Misses", "Total Time (seconds)"]
            for method, stats in self._stats.items():
                table.add_row([method, stats['calls'], stats['hits'], stats['misses'], f"{stats['total_time']:.4f}"])
            print(table)

    return WrappedClass



git remote add origin https://github.com/wa-lead/CacheKing.git
