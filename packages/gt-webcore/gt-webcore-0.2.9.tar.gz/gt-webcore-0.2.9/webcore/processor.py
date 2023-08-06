# -*- coding: utf-8 -*-

import asyncio
import threading
import time
import functools
import concurrent

class Processor:
    def __init__(self, pool_size=None):
        self._loop = None
        self._pool_size = pool_size
        self._thread = threading.Thread(target=self._run)

    def post_callback(self, callback, *args):
        return self._loop.run_in_executor(self._pool, callback, *args)

    def post_coroutine(self, coro, *args):
        return asyncio.run_coroutine_threadsafe(coro, self._loop)

    def start(self):
        self._thread.start()

        '''
        线程刚刚启动时，需要等待_loop初始化完成再返回，避免过早投递任务过来导致错误
        '''
        while self._loop is None:
            time.sleep(0.001)

    def stop(self):
        self._loop.call_soon_threadsafe(self._do_stop)
        self._thread.join()

    def _do_stop(self):
        self._pool.shutdown()
        self._loop.stop()

    def _run(self):
        self._pool = concurrent.futures.ThreadPoolExecutor(self._pool_size)
        self._loop = asyncio.new_event_loop()
        self._loop.run_forever()

def task(processor):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            processor.post_callback(functools.partial(func, *args, **kwargs))
        return wrapper
    return decorator

def coroutine(processor):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return processor.post_coroutine(func(*args, **kwargs))
        return wrapper
    return decorator
