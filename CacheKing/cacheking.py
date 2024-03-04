import types
import functools
import pickle
import time
from prettytable import PrettyTable
import importlib
import inspect
import time
import functools
from collections.abc import Callable
from .utils import make_hashable


class CacheKing:
    def __init__(self, additional_modules=None):
        """
        Initialize CacheKing with optional additional modules to cache.
        :param additional_modules: A list of module names (strings) to include in caching.
        """
        self.additional_modules = additional_modules if additional_modules is not None else []
        self.original_functions = {}
        self.cache = {}
        self.performance_stats = {}

    def __enter__(self):
        caller_module = inspect.getmodule(inspect.stack()[1][0])
        if caller_module:
            self._cache_module_functions(caller_module)

        for module_name in self.additional_modules:
            module = importlib.import_module(module_name)
            self._cache_module_functions(module)
        
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restore the original state of all modified functions
        for func_name, (module, original_func) in self.original_functions.items():
            setattr(module, func_name, original_func)
        self.report()

    def _cache_module_functions(self, module):
        """
        Cache all functions within the specified module.
        :param module: Module object to cache functions from.
        """
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, types.FunctionType) and attr.__module__ == module.__name__:
                self.original_functions[attr_name] = (module, attr)
                self.cache[attr_name] = {}
                if attr_name not in self.performance_stats:
                    self.performance_stats[attr_name] = {'hits': 0, 'misses': 0, 'total_time': 0, 'calls': 0}
                wrapped_func = self.wrap_function(attr, attr_name)
                setattr(module, attr_name, wrapped_func)

  
    def wrap_function(self, func, func_name):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Check if any argument is a custom class instance
            if any(isinstance(arg, Callable) for arg in args) or any(isinstance(v, Callable) for v in kwargs.values()):
                # Consider it a miss and directly execute the function
                result = func(*args, **kwargs)
            else:
                start = time.time()
                try:
                    # Attempt to create a hashable key. This assumes `make_hashable` is defined to handle typical data structures.
                    key = make_hashable((args, frozenset(kwargs.items())))
                    cache_hit = key in self.cache[func_name]
                except Exception:
                    self.performance_stats[func_name]['misses'] += 1
                    self.performance_stats[func_name]['calls'] += 1
                    self.performance_stats[func_name]['total_time'] += time.time() - start                    
                    return func(*args, **kwargs)
                
                if cache_hit:
                    result = self.cache[func_name][key]
                    self.performance_stats[func_name]['hits'] += 1
                else:
                    result = func(*args, **kwargs)
                    # Only cache if key creation was successful
                    if not cache_hit and key is not None:
                        self.cache[func_name][key] = result
                    self.performance_stats[func_name]['misses'] += 1
                
                elapsed_time = time.time() - start
                self.performance_stats[func_name]['calls'] += 1
                self.performance_stats[func_name]['total_time'] += elapsed_time
                
            return result
        return wrapper


    def print_colored(self, text, color):
        """Prints text in a specified color in the terminal."""
        colors = {
            "red": "\033[91m",
            "green": "\033[92m",
            "orange": "\033[93m",
            "end": "\033[0m",
        }
        print(f"{colors.get(color, '')}{text}{colors['end']}")

    def report(self):
        table = PrettyTable()
        table.field_names = ["Function", "Calls", "Cache Hits", "Cache Misses", "Total Time (seconds)", "Recommendation"]
        for func, stats in self.performance_stats.items():
            calls = stats['calls']
            hits = stats['hits']
            misses = stats['misses']
            total_time = stats['total_time']
            hit_ratio = hits / calls if calls else 0
            
            # Determine recommendation based on hit ratio
            if hit_ratio > 0.75:
                recommendation = "High"
                rec_color = "green"
            elif hit_ratio > 0.25:
                recommendation = "Medium"
                rec_color = "orange"
            else:
                recommendation = "Low"
                rec_color = "red"
            
            time_saved = total_time - (hits * total_time / max(calls, 1))
            table.add_row([func, calls, hits, misses, f"{time_saved:.4f}", recommendation])
        
        print(table)
        print("\nCaching Recommendations:")
        for func, stats in self.performance_stats.items():
            calls = stats['calls']
            hits = stats['hits']
            hit_ratio = hits / calls if calls else 0
            
            if hit_ratio > 0.75:
                recommendation = "Could benefit from caching"
                rec_color = "green"
            elif hit_ratio > 0.25:
                recommendation = "May benefit from selective caching"
                rec_color = "orange"
            else:
                recommendation = "Unlikely to benefit significantly from caching"
                rec_color = "red"
            
            self.print_colored(f"{func}: {recommendation}", rec_color)


    

if __name__ == '__main__':
    
    def fibonacci(n):
        if n <= 1:
            return n
        else:
            return fibonacci(n-1) + fibonacci(n-2)

    n = 35  

    # Without caching
    start_time = time.time()
    result = fibonacci(n)
    end_time = time.time()
    print(f"Without caching: Fibonacci({n}) = {result}, Time: {end_time - start_time} seconds")

    # With caching
    with CacheKing(additional_modules=['fib']):
        start_time = time.time()
        result = fibonacci(n)
        end_time = time.time()
        print(f"With caching: Fibonacci({n}) = {result}, Time: {end_time - start_time} seconds")

