from werkzeug.contrib.cache import MemcachedCache
from functools import wraps

cache = MemcachedCache(["127.0.0.1:11211"])

def get_key(f, *args, **kwargs):
	if len(args) > 0:
		kwargs["#args"] = ",".join(map(str, args))
	sorted_keys = sorted(kwargs)
	arg_key = "&".join(["{}:{}".format(key, kwargs[key]) for key in sorted_keys])
	key = "{}.{}${}".format(f.__module__, f.__name__, arg_key).replace(" ", "~")
	return key

def memoize(timeout=120):
	def decorator(f):
		@wraps(f)
		def wrapper(*args, **kwargs):
			key = get_key(f, *args, **kwargs)
			cached_result = cache.get(key)
			if cached_result is None:
				function_result = f(*args, **kwargs)
				cache.set(key, function_result, timeout=timeout)
				return function_result
			return cached_result
		return wrapper
	return decorator