import asyncio

def FreqLimiter(limit: int, interval: float):
    sema = asyncio.Semaphore(limit)
    def decorator(func):
        async def wrapper(*args, **kwargs):
            await sema.acquire()
            asyncio.get_running_loop().call_later(interval, sema.release)
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def RunningLimiter(limit: int):
    sema = asyncio.Semaphore(limit)
    def decorator(func):
        async def wrapper(*args, **kwargs):
            await sema.acquire()
            try:
                return await func(*args, **kwargs)
            finally:
                sema.release()
        return wrapper
    return decorator