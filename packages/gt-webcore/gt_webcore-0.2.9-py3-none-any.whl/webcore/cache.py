from . import app

import functools

def auto_cache(timeout=None, args_to_ignore=None):
  if app.cache:
    return app.cache.memoize(timeout=timeout, args_to_ignore=args_to_ignore)
  else:
    def decorator(func):
      @functools.wraps(func)
      def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

      return wrapper
    return decorator

def del_cache(f, *cargs, **ckwargs):
  def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      result = func(*args, **kwargs)

      if app.cache:
        app.cache.delete_memoized(f, *cargs, **ckwargs)
      
      return result

    return wrapper
  return decorator

def del_caches(cache_funcs):
  '''
  删除多个缓存实例
  cache_funcs 是 del_cache 函数的参数数组
  '''
  def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      result = func(*args, **kwargs)

      if app.cache:
        for param in cache_funcs:
          cargs = param.args if param.args else []
          ckwargs = param.kwargs if param.kwargs else {}
          app.cache.delete_memoized(param.f, *cargs, **ckwargs)
      
      return result

    return wrapper
  return decorator

